"""Real subprocess-execution tests -- not mocked. These actually invoke
pytest as a subprocess against a bundled fixture file, proving
validation_runner's pass/fail/timeout reporting reflects what a real
process actually did.
"""

from pathlib import Path

from test_validation.validation_runner import run_validation


def test_real_subprocess_reports_pass_for_a_passing_test(tmp_path):
    test_file = tmp_path / "test_always_pass.py"
    test_file.write_text("def test_ok():\n    assert True\n", encoding="utf-8")

    outcome = run_validation(test_file, repo_root=str(tmp_path), framework="pytest")

    assert outcome.passed is True
    assert outcome.exit_code == 0
    assert outcome.timed_out is False
    assert "1 passed" in outcome.stdout_excerpt


def test_real_subprocess_reports_failure_for_a_failing_test(tmp_path):
    test_file = tmp_path / "test_always_fail.py"
    test_file.write_text("def test_bad():\n    assert False\n", encoding="utf-8")

    outcome = run_validation(test_file, repo_root=str(tmp_path), framework="pytest")

    assert outcome.passed is False
    assert outcome.exit_code == 1
    assert outcome.timed_out is False
    assert "1 failed" in outcome.stdout_excerpt


def test_real_subprocess_times_out_on_a_slow_test(tmp_path):
    test_file = tmp_path / "test_slow.py"
    test_file.write_text(
        "import time\n\n\ndef test_slow():\n    time.sleep(5)\n", encoding="utf-8"
    )

    outcome = run_validation(
        test_file, repo_root=str(tmp_path), framework="pytest", timeout_seconds=1
    )

    assert outcome.timed_out is True
    assert outcome.passed is False
    assert outcome.exit_code is None


def test_unsupported_extension_returns_explicit_unsupported_outcome(tmp_path):
    test_file = tmp_path / "FooTest.java"
    test_file.write_text("", encoding="utf-8")

    outcome = run_validation(test_file, repo_root=str(tmp_path), framework="junit")

    assert outcome.passed is False
    assert outcome.command == []
    assert "no supported runner" in outcome.stderr_excerpt


def test_relative_test_file_and_repo_root_still_resolve_correctly(tmp_path, monkeypatch):
    # Regression test for a real bug found via dogfooding: run_validation
    # sets the subprocess cwd to test_file.parent, so a *relative*
    # test_file or repo_root (as a caller invoking from a different cwd,
    # e.g. "." for repo_root, would naturally pass) must still resolve to
    # the right absolute location, not silently resolve against the new
    # subprocess cwd instead.
    tests_dir = tmp_path / "generated"
    tests_dir.mkdir()
    (tests_dir / "test_ok.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    relative_test_file = Path("generated") / "test_ok.py"

    outcome = run_validation(relative_test_file, repo_root=".", framework="pytest")

    assert outcome.passed is True, outcome.stderr_excerpt
    assert outcome.exit_code == 0


def test_large_stdout_is_bounded_to_excerpt_length(tmp_path):
    # Regression test for the memory-exhaustion fix: stdout/stderr are now
    # captured to disk-backed temp files, not buffered fully in memory, and
    # only the tail excerpt is read back. pytest only echoes a passing
    # test's prints if the test fails (its "Captured stdout call" section),
    # so this test fails on purpose after printing a large amount, to
    # actually exercise a large real subprocess stdout stream.
    test_file = tmp_path / "test_noisy.py"
    test_file.write_text(
        "def test_noisy():\n"
        "    for _ in range(20000):\n"
        "        print('x' * 40)\n"
        "    assert False\n",
        encoding="utf-8",
    )

    outcome = run_validation(test_file, repo_root=str(tmp_path), framework="pytest")

    assert outcome.timed_out is False
    assert outcome.exit_code == 1
    assert len(outcome.stdout_excerpt) <= 2000


def test_timeout_does_not_crash_when_child_wrote_output_before_being_killed(tmp_path):
    # The tempfile-backed stdout/stderr redirection must not raise or hang
    # itself when reading back an excerpt from a process that was killed
    # mid-write. (pytest's own internal output capturing means the child's
    # print() never reaches the real fd before a hard kill either way, so
    # this checks robustness, not content preservation.)
    test_file = tmp_path / "test_slow_with_output.py"
    test_file.write_text(
        "import sys, time\n\n\n"
        "def test_slow():\n"
        "    print('partial output before timeout')\n"
        "    sys.stdout.flush()\n"
        "    time.sleep(5)\n",
        encoding="utf-8",
    )

    outcome = run_validation(
        test_file, repo_root=str(tmp_path), framework="pytest", timeout_seconds=1
    )

    assert outcome.timed_out is True
    assert outcome.exit_code is None
    assert isinstance(outcome.stdout_excerpt, str)
    assert isinstance(outcome.stderr_excerpt, str)


def test_pytest_process_can_import_target_repo_via_pythonpath(tmp_path):
    pkg_dir = tmp_path / "pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("", encoding="utf-8")
    (pkg_dir / "module.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")

    tests_dir = tmp_path / "generated"
    tests_dir.mkdir()
    test_file = tests_dir / "test_import.py"
    test_file.write_text(
        "from pkg.module import add\n\n\ndef test_add():\n    assert add(1, 2) == 3\n",
        encoding="utf-8",
    )

    outcome = run_validation(test_file, repo_root=str(tmp_path), framework="pytest")

    assert outcome.passed is True, outcome.stderr_excerpt
