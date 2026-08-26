from engine.stack_trace_parser import parse_stack_frames
from engine.stats import compute_stats
from engine.symptom_scanner import scan


def test_word_count_and_flag_derived_counts():
    text = "It sometimes just stops working randomly, expected it to save but instead nothing happens."
    flags = scan(text)
    frames = parse_stack_frames(text)
    stats = compute_stats(text, flags, frames)
    assert stats.word_count == len(text.split())
    assert stats.vague_symptom_count == 1
    assert stats.stack_frame_count == 0


def test_stack_frame_count_reflects_parsed_frames():
    text = 'File "engine/report.py", line 42, in build_report'
    flags = scan(text)
    frames = parse_stack_frames(text)
    stats = compute_stats(text, flags, frames)
    assert stats.stack_frame_count == 1
