from engine.stack_trace_parser import parse_stack_frames


def test_parses_python_traceback_frame():
    text = (
        'Traceback (most recent call last):\n'
        '  File "engine/report.py", line 42, in build_report\n'
        "    raise ValueError('bad input')\n"
        "ValueError: bad input"
    )
    frames = parse_stack_frames(text)
    assert len(frames) == 1
    assert frames[0].path == "engine/report.py"
    assert frames[0].line == 42
    assert frames[0].symbol == "build_report"


def test_parses_multiple_python_frames_in_order():
    text = (
        'File "engine/cli.py", line 10, in main\n'
        'File "engine/report.py", line 42, in build_report\n'
    )
    frames = parse_stack_frames(text)
    assert [f.path for f in frames] == ["engine/cli.py", "engine/report.py"]


def test_parses_generic_path_colon_line_shape():
    text = "Compile error at engine/scanner.py:88 — unexpected token"
    frames = parse_stack_frames(text)
    assert len(frames) == 1
    assert frames[0].path == "engine/scanner.py"
    assert frames[0].line == 88
    assert frames[0].symbol is None


def test_generic_frame_not_double_counted_inside_python_frame():
    text = 'File "engine/report.py", line 42, in build_report'
    frames = parse_stack_frames(text)
    assert len(frames) == 1


def test_no_frames_in_plain_text():
    assert parse_stack_frames("The button does not respond when clicked.") == []
