"""Authored from examples/test-generation/synthetic-output/generation-plan-report.json's
spec for `test_generation/naming_convention.py::_classify` -- 1 positive
slot + 4 negative slots, per that plan's own naming convention
("test_*.py") and real source excerpt.

The real source excerpt showed 5 branches: two Python conventions
(test_*.py / *_test.py), two Java/Kotlin conventions (*Test.java /
*Tests.java), one Kotlin-only convention (*Spec.kt), and an implicit
`return None` fallback. All 4 negative slots below are genuinely distinct
conditions grounded in that branching -- no padding was needed to reach 4.
"""

from pathlib import Path

from test_generation.naming_convention import _classify


def test_classify_positive_recognizes_python_test_prefix_convention():
    assert _classify(Path("test_foo.py")) == "test_*.py"


def test_classify_negative_unrecognized_filename_returns_none():
    # No test_ prefix, no _test suffix, no Java/Kotlin suffix -- not a test
    # file under any known convention.
    assert _classify(Path("random.py")) is None


def test_classify_negative_java_style_suffix_with_python_extension_returns_none():
    # Stem ends with "Test" (the Java/Kotlin convention marker), but the
    # suffix check for that branch requires .java/.kt -- a .py file never
    # matches it, and it doesn't match either Python branch either.
    assert _classify(Path("FooTest.py")) is None


def test_classify_negative_python_prefix_with_wrong_extension_returns_none():
    # Stem has the Python "test_" prefix, but the branch also requires
    # suffix == ".py" -- a non-.py extension falls through to None.
    assert _classify(Path("test_foo.txt")) is None


def test_classify_negative_spec_suffix_restricted_to_kotlin_returns_none():
    # "*Spec" is only recognized when suffix == ".kt" per the real source;
    # the same stem with a .java suffix falls through to None.
    assert _classify(Path("FooSpec.java")) is None
