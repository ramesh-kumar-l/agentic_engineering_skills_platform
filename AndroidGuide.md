# Android Guide (Kotlin / Java)

You have one or more existing Android projects — written in Kotlin, Java, or
a mix — built with Gradle and Android Studio, and you want to point this
platform's skills at them with the least possible setup. This guide is that
path, plus an honest, specific section on using the test-case generator
against a **legacy** Android codebase: what it actually does, what it
doesn't, and what you still have to do yourself in Android Studio.

This is a companion to [`QuickStarterGuide.md`](QuickStarterGuide.md), not a
replacement — read that one first if you want the general picture of the
whole platform. This guide only covers the Android-specific parts.

## 1. Minimum-effort install

You need Python 3.10+ and Git on the machine running these tools — nothing
Android-specific. Your Android project itself keeps using whatever JDK/
Gradle/Android Studio setup it already has; none of that is touched.

```bash
git clone <this-repository-url>
cd agentic_engineering_skills_platform
pip install -r requirements.txt
```

That one command installs the platform's only dependency (`pytest`) and is
enough to run every skill's CLI. You do **not** need to run
`pip install -e ".[dev]"` in any skill directory unless you specifically
want to run that skill's own test suite — using a skill against your Android
project doesn't require it.

No JDK, Gradle wrapper, Android SDK, emulator, or Node install is invoked by
any of these tools, ever — they read your project's files as plain text and
never build or run your app (`DEPENDENCIES.md`'s "Non-Python tooling"
section states this explicitly).

## 2. Point one skill at one of your Android repos (5 minutes)

`codebase-intelligence` is the simplest starting point — it produces a
structural map (files, imports, classes, entry points, external
dependencies) of any repo you give it, including a real Android one:

```bash
cd skills/codebase-intelligence
python -m engine.cli /path/to/your-android-app --format both --out /path/to/ci-out
```

For `.java` and `.kt` files, this uses a real (if regex-based, not a full
AST) parser — it extracts `package` declarations, `import`s, top-level
class/interface/enum/object declarations, Kotlin `fun` declarations, and
`main`-entry detection. One disclosed caveat worth knowing before you trust
the output for refactoring decisions: it does not track brace depth, so a
nested/inner class can occasionally be mis-recorded as if it were top-level
(known limitation
[L32](project-memory-bank/12-known-limitations.md) — rare, but not
structurally prevented). Treat its output as a strong hint, not ground
truth, same as this project treats it internally.

## 3. Generating test cases for a legacy Kotlin/Java project

This is the part you specifically asked about. Read this whole section
before running anything — the two caveats in step 4 change what you should
expect from the output.

### 3.1 Which tool is actually "the test case generator"

There are two different tools in this platform that produce test-related
output, and they do different jobs:

- **`skills/acceptance-test-engineer/`** turns a *written requirement* into
  Gherkin-style acceptance criteria and JSON test-case specs. It never reads
  your code — input is free text, not a repo. Useful before you write a new
  feature; not what you want for "generate tests for code that already
  exists."
- **`test_generation/`** (a Test Engineering Platform package) is the one
  you want. It produces a deterministic *test-generation plan* — which file
  to test, which testing framework to use, a source excerpt, and 1 positive
  + 4 negative test-case slots — for an agent (or you) to then write the
  actual test file from. It never authors test code itself; it decides what
  the test should cover and hands that plan to whoever writes the file.

`test_generation` doesn't run alone — it's the last planning stage of a
5-stage pipeline: `codebase-intelligence` + `regression-hunter` →
`project_intelligence` + `test_strategy` → `scenario_planner` →
`test_generation`. Each stage's output is the next stage's required input.

### 3.2 Reframe "legacy" — this is diff-driven, not whole-app coverage

Important expectation to set before you start: this pipeline decides which
**changed** files need a test, from a real `git diff`. It has no
"retroactively generate full test coverage for my entire 5-year-old app in
one shot" mode — `regression-hunter`, the pipeline's second stage,
hard-requires an actual diff and exits non-zero without one.

For a legacy project with no pending change, pick a real diff to seed it
rather than expecting whole-app output:

```bash
# a recent range of real commits in an area you actually want covered
git -C /path/to/your-android-app diff HEAD~10..HEAD

# or a feature branch against main, if one exists
git -C /path/to/your-android-app diff main..some-feature-branch
```

Start with one file or module you actually care about, not the whole app —
the pipeline scales to however much diff you feed it, and a smaller, real
diff gives you a plan you can actually review.

### 3.3 The full chain, against your Android repo

```bash
# 1. codebase-intelligence and regression-hunter produce the two starting
#    reports the rest of the pipeline builds on
cd skills/codebase-intelligence
python -m engine.cli /path/to/your-android-app --format json --out /path/to/ci-out

cd ../regression-hunter
git -C /path/to/your-android-app diff HEAD~10..HEAD | \
  python -m engine.cli - --ci-report /path/to/ci-out/report.json --format json --out /path/to/rh-out

# 2. derive a TestEnvironmentProfile (build system, test frameworks, Android detection)
cd ../..
python -m project_intelligence.cli /path/to/ci-out/report.json --out /path/to/tep-out

# 3. decide which of the diff's changed files need a test
python -m test_strategy.cli /path/to/rh-out/report.json /path/to/tep-out/test-environment-profile.json --out /path/to/tep-out

# 4. plan candidate test scenarios for each flagged file
python -m scenario_planner.cli /path/to/tep-out/test-strategy-report.json /path/to/rh-out/report.json /path/to/ci-out/report.json --out /path/to/tep-out

# 5. produce the deterministic generation plan — this is the actual "test case" output
python -m test_generation.cli /path/to/tep-out/scenario-plan-report.json /path/to/your-android-app --out /path/to/tep-out
```

Step 5's output (`generation-plan-report.json` in `/path/to/tep-out/`) is
your test-generation plan — the file/framework/scenario slots an agent (or
you) should now write an actual `.kt`/`.java` test file from.

A real, non-synthetic run of the earlier stages against a genuine Android
codebase (Google's own `android/architecture-samples`) is already committed
at
[`examples/project-intelligence/android-example/example-run.md`](examples/project-intelligence/android-example/example-run.md)
— read it before running this against an unfamiliar repo of your own; it
shows exactly what real output looks like, including the gap described next.

### 3.4 Two things this will not do for you — read before you rely on the output

**Test-framework detection will likely say "unavailable" even when JUnit/
Espresso/Robolectric are genuinely in use.** `project_intelligence`'s
Android-framework detection depends on parsing your `build.gradle[.kts]`
for dependency declarations, and that parser only recognizes a literal,
single-line `"group:artifact:version"` string. Real Android projects almost
never declare dependencies that way — they use a version variable
(`"junit:junit:$junitVersion"`), a properties object (`deps.junit`), or a
version catalog (`libs.junit`). This was checked against six real
open-source Android repos, and every one of them triggered this gap (known
limitation
[L35](project-memory-bank/12-known-limitations.md)). **For your 3 projects:
open `build.gradle`/`build.gradle.kts`/`libs.versions.toml` yourself and
confirm which test frameworks are actually present** — don't take a
"framework unavailable" result from `project_intelligence` at face value.

**Nothing in this platform will run the `.kt`/`.java` test file once it's
written.** After step 5 produces a plan and an agent writes the actual test
file, the pipeline's final stage, `test_validation`, is the thing that would
normally execute it and record a real pass/fail. For `.java`/`.kt` files, it
explicitly does not attempt this — it returns exactly this result instead:

```
passed: false
stderr_excerpt: "no supported runner for .kt files — only Python (pytest) is executed in this version"
```

This isn't a bug to work around — `test_validation` only knows how to invoke
`pytest`; running a JVM test for real needs your project's own Gradle
wrapper, which is deliberately out of scope (a loose test file has no
`build.gradle` context of its own to build against). **You prove the
generated test actually compiles and passes yourself**, the same way you
would for any test you wrote by hand:

```bash
./gradlew test               # or: testDebugUnitTest, connectedAndroidTest
```

or by right-clicking the new test file in Android Studio and choosing Run.

### 3.5 One worked example, start to finish

```bash
# from the platform repo root, against one of your 3 Android projects:
APP=/path/to/your-android-app
OUT=/path/to/tep-out

cd skills/codebase-intelligence && python -m engine.cli "$APP" --format json --out "$OUT/ci-out" && cd ../..
cd skills/regression-hunter && git -C "$APP" diff HEAD~10..HEAD | python -m engine.cli - --ci-report "$OUT/ci-out/report.json" --format json --out "$OUT/rh-out" && cd ../..
python -m project_intelligence.cli "$OUT/ci-out/report.json" --out "$OUT"
python -m test_strategy.cli "$OUT/rh-out/report.json" "$OUT/test-environment-profile.json" --out "$OUT"
python -m scenario_planner.cli "$OUT/test-strategy-report.json" "$OUT/rh-out/report.json" "$OUT/ci-out/report.json" --out "$OUT"
python -m test_generation.cli "$OUT/scenario-plan-report.json" "$APP" --out "$OUT"

# now read $OUT/generation-plan-report.json, have an agent (or you) write the
# actual .kt/.java test file it describes into your Android project, and run
# it the normal way:
#   ./gradlew test
# or open it in Android Studio and click Run.
```

## 4. Where to read more

| You want to... | Read this |
|---|---|
| The general, non-Android quickstart | [`QuickStarterGuide.md`](QuickStarterGuide.md) |
| The full TEP pipeline diagram and package-by-package detail | [`project-memory-bank/25-tep-pipeline-overview.md`](project-memory-bank/25-tep-pipeline-overview.md) |
| The exact Gradle-parsing and nested-type limitations in full | [`project-memory-bank/12-known-limitations.md`](project-memory-bank/12-known-limitations.md) — L32, L33, L35 |
| A real dogfood run against an actual Android codebase | [`examples/project-intelligence/android-example/example-run.md`](examples/project-intelligence/android-example/example-run.md) |
