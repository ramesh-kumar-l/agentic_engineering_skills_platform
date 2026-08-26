from engine.models import WiringMode
from engine.workflow_registry import REGISTRY, get_template, list_templates


def test_registry_has_exactly_three_templates():
    assert set(REGISTRY) == {
        "understand-then-plan",
        "understand-then-test-plan",
        "understand-then-optimize-context",
    }


def test_every_template_starts_with_codebase_intelligence():
    for template in REGISTRY.values():
        assert template.steps[0].skill_name == "codebase-intelligence"
        assert template.steps[0].upstream_context_marker is None


def test_every_template_has_exactly_two_steps():
    for template in REGISTRY.values():
        assert len(template.steps) == 2


def test_cli_flag_steps_declare_a_flag_name():
    for template in REGISTRY.values():
        step2 = template.steps[1]
        if step2.wiring_mode == WiringMode.CLI_FLAG:
            assert step2.wiring_flag == "--ci-report"


def test_text_append_step_declares_no_flag():
    template = REGISTRY["understand-then-test-plan"]
    step2 = template.steps[1]
    assert step2.wiring_mode == WiringMode.TEXT_APPEND
    assert step2.wiring_flag is None


def test_get_template_returns_none_for_unknown_name():
    assert get_template("does-not-exist") is None


def test_list_templates_matches_registry_size():
    assert len(list_templates()) == len(REGISTRY)
