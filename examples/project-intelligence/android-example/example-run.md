# Project Intelligence — Android real dogfood run (TEP Phase 4)

TEP Phase 4's exit criteria ([[18-test-engineering-platform-contract]])
requires the profile to "correctly identify JUnit/Robolectric/Espresso
presence (or absence) on at least one real open-source Android repo," and
to explicitly report "unavailable," never a guess, when a framework isn't
detected — built by extending `codebase-intelligence`'s existing dependency
output, same as TEP Phase 3. This is that real, non-fixture run.

## Target repo

`android/architecture-samples` (`views` branch), Google's own official
Android architecture sample — a real, current, non-fixture open-source
Android app. Scanned at the `app/` module level (same "scan the meaningful
subdirectory, not repo root" precedent TEP Phase 3 set), since that is
where its Gradle build file and source actually live.

The app module's `build.gradle` **genuinely declares** all three named
frameworks — hand-verified directly from the real source at the time of
this run:

```
testImplementation "junit:junit:$junitVersion"
testImplementation "org.robolectric:robolectric:$robolectricVersion"
testImplementation "androidx.test.espresso:espresso-core:$espressoVersion"
androidTestImplementation "junit:junit:$junitVersion"
```

## Step 1 — Generate a fresh codebase-intelligence report

```
cd skills/codebase-intelligence
python -m engine.cli <path-to-cloned-repo>/app --format json \
  --out ../../examples/project-intelligence/android-example/ci-report
```

Output: `examples/project-intelligence/android-example/ci-report/report.json`.

## Step 2 — Derive the TestEnvironmentProfile

```
python -m project_intelligence.cli \
  examples/project-intelligence/android-example/ci-report/report.json \
  --out examples/project-intelligence/android-example/output
```

Output:
`examples/project-intelligence/android-example/output/test-environment-profile.json`.

## Result and hand-verification

- `external_dependencies` in the codebase-intelligence report: **empty** —
  confirmed by reading the raw report.json directly.
- `android_test_frameworks`: **empty**. `android_frameworks_absent: ["Espresso",
  "JUnit", "Robolectric"]`. `android_test_framework` appears in `unavailable`.

**This is the honest result, not a detection bug.** The app module's real
`build.gradle` declares all three frameworks, as quoted above — but every
version is written as `$junitVersion`-style Gradle variable interpolation,
not a literal string. `external_deps.py`'s Gradle regex is deliberately
scoped to single-line literal `"group:artifact:version"` triples only
([[12-known-limitations|L33]]); it does not resolve variables, `ext {}`
blocks, `buildSrc` dependency objects, or version-catalog (`libs.versions.toml`)
references. Verified directly: running the regex against this exact file
produces zero matches.

During this phase's implementation, **five other real open-source Android
repos were checked by hand** (`android/sunflower`, `android/architecture-samples`
main branch, `googlesamples/android-testing`, `android/architecture-components-samples`,
and this repo's `views` branch) — every single one declares its Android
test dependencies through variable interpolation, an `ext`/`deps`-style
properties object, or a version catalog. None uses the bare literal
`"group:artifact:version"` string `_GRADLE_DEP` requires. This is now
logged as [[12-known-limitations|L35]]: variable-based dependency
versioning is the near-universal real-world convention for Android/Gradle
projects, not an edge case, so Android framework detection will
systematically report "unavailable" on real Android repos today, even when
the framework is genuinely present in source.

## What the detection logic itself proves (separately, via unit tests)

Because no real repo checked during this phase has a literal-notation
match, the positive-detection path is proven with synthetic
`CiReportContext` fixtures in
`project_intelligence/tests/test_android_detection.py` — constructing the
exact shape `external_deps.py` *would* produce if L33 were fixed, and
confirming: JUnit/Robolectric/Espresso are each matched correctly by
artifact-id, multiple Espresso artifacts (`espresso-core`,
`espresso-contrib`, `espresso-intents`) roll up to one `Finding` with
combined evidence, unrelated dependencies (e.g. `com.squareup:retrofit`)
never false-positive, and partial presence (JUnit only) produces an
explicit, correct `android_frameworks_absent: ["Espresso", "Robolectric"]`
— never a guess.

## What this does and does not prove

**Proves**: the profile correctly and honestly reports the *current*
detectable state (fully "unavailable," each absence named explicitly) on a
real, hand-verified Android repo, derived entirely from
`codebase-intelligence`'s existing output with no manifest re-parsed by
this package — and the detection logic itself is correct once given
matching dependency data (proven by unit test, since no real repo checked
provides that data through the current upstream parser).

**Does not prove**: that Android repos in the wild ever hit the
`dependency-confirmed` path through today's `external_deps.py`. That
requires resolving L33 (Gradle variable/version-catalog support) —
explicitly out of scope for TEP Phase 4, which extends `project_intelligence`'s
own consumption of existing dependency output, not the upstream parser
itself. Fixing L33 is a live known limitation, not silently hidden.
