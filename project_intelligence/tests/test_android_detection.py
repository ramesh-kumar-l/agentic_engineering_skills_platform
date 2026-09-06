"""TEP Phase 4 — Android test-environment detection.

Real Android repos declare test-dependency versions via Gradle variable
interpolation or version catalogs almost universally (hand-verified against
several real open-source repos during this phase's implementation), which
`external_deps.py`'s literal-string-only Gradle regex (L33) cannot capture.
These tests prove the *detection logic* is correct once a dependency IS
captured — the real, honest end-to-end result on an actual Android repo is
demonstrated separately in examples/project-intelligence/android-example/
and documented in project-memory-bank/12-known-limitations.md L35.
"""

from project_intelligence.ci_report_loader import CiExternalDependency, CiReportContext
from project_intelligence.detect import detect_android_test_frameworks
from project_intelligence.profile_builder import build_profile
import json


def _ctx(deps) -> CiReportContext:
    return CiReportContext(
        root_path="/tmp/android-target",
        language_breakdown={"kotlin": 40, "unknown": 10},
        external_dependencies=deps,
        top_level_filenames=["build.gradle"],
    )


def test_all_three_named_frameworks_detected_when_present():
    ctx = _ctx([
        CiExternalDependency(name="junit:junit", source_file="build.gradle"),
        CiExternalDependency(name="org.robolectric:robolectric", source_file="build.gradle"),
        CiExternalDependency(name="androidx.test.espresso:espresso-core", source_file="build.gradle"),
    ])

    findings = detect_android_test_frameworks(ctx)

    assert {f.name for f in findings} == {"JUnit", "Robolectric", "Espresso"}
    assert all(f.confidence == "dependency-confirmed" for f in findings)


def test_espresso_variants_roll_up_to_one_finding_with_combined_evidence():
    ctx = _ctx([
        CiExternalDependency(name="androidx.test.espresso:espresso-core", source_file="build.gradle"),
        CiExternalDependency(name="androidx.test.espresso:espresso-contrib", source_file="build.gradle"),
        CiExternalDependency(name="androidx.test.espresso:espresso-intents", source_file="build.gradle"),
    ])

    findings = detect_android_test_frameworks(ctx)

    assert len(findings) == 1
    assert findings[0].name == "Espresso"
    assert findings[0].evidence == [
        "androidx.test.espresso:espresso-contrib",
        "androidx.test.espresso:espresso-core",
        "androidx.test.espresso:espresso-intents",
    ]


def test_robolectric_not_confused_with_unrelated_dependency():
    ctx = _ctx([CiExternalDependency(name="com.squareup:retrofit", source_file="build.gradle")])

    findings = detect_android_test_frameworks(ctx)

    assert findings == []


def test_profile_reports_partial_absence_explicitly_not_a_guess(tmp_path):
    report = {
        "root_path": "/tmp/android-target",
        "language_breakdown": {"kotlin": 40},
        "external_dependencies": [
            {"name": "junit:junit", "version": "4.13.2", "source_file": "build.gradle"},
        ],
        "files": [{"path": "build.gradle"}],
    }
    path = tmp_path / "report.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    profile = build_profile(path)

    assert [f.name for f in profile.android_test_frameworks] == ["JUnit"]
    assert profile.android_frameworks_absent == ["Espresso", "Robolectric"]
    assert "android_test_framework" not in profile.unavailable


def test_profile_marks_android_test_framework_unavailable_when_none_match(tmp_path):
    report = {
        "root_path": "/tmp/android-target",
        "language_breakdown": {"kotlin": 40},
        "external_dependencies": [],
        "files": [{"path": "build.gradle"}],
    }
    path = tmp_path / "report.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    profile = build_profile(path)

    assert profile.android_test_frameworks == []
    assert profile.android_frameworks_absent == ["Espresso", "JUnit", "Robolectric"]
    assert "android_test_framework" in profile.unavailable
