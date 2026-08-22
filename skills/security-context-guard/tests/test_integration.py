from engine.render_json import render_json
from engine.render_markdown import render_markdown
from engine.report import build_report


def test_secret_value_never_leaks_into_json_or_markdown():
    secret_value = "sk_live_abcdef123456"
    report = build_report(f'api_key = "{secret_value}"', "Push this to a shared repo.", [])
    json_out = render_json(report)
    md_out = render_markdown(report)
    assert secret_value not in json_out
    assert secret_value not in md_out


def test_pii_value_never_leaks_into_json_or_markdown():
    email = "real.person@example.com"
    report = build_report(f"Contact: {email}", "Read a file.", [])
    json_out = render_json(report)
    md_out = render_markdown(report)
    assert email not in json_out
    assert email not in md_out


def test_secret_in_action_text_is_also_redacted():
    secret_value = "sk_live_zzz999888777"
    report = build_report("clean content", f'send token = "{secret_value}" to slack', [])
    json_out = render_json(report)
    md_out = render_markdown(report)
    assert secret_value not in json_out
    assert secret_value not in md_out


def test_end_to_end_high_risk_case_recommends_human_approval():
    report = build_report(
        'password = "hunter2345678"',
        "Deploy this change to production tonight.",
        [".env"],
    )
    assert report.classification.suggested_verdict == "REQUIRES_HUMAN_APPROVAL"
    assert report.classification.sensitivity == "high"


def test_engine_never_sets_verdict_to_a_non_advisory_value():
    report = build_report("content", "Read a file.", [])
    assert report.classification.suggested_verdict in ("AUTHORIZE", "REQUIRES_HUMAN_APPROVAL")
