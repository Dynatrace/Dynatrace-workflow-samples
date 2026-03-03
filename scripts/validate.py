#!/usr/bin/env python3
"""
Dynatrace Workflow Samples — CI Validation Script

Performs optimistic validation checks on workflow templates and sample files:
  1. YAML/JSON syntax validation
  2. Workflow template structure checks (schemaVersion, task name consistency,
     predecessor references, action format)
  3. Secret / credential scanning (real tokens only, not placeholders)
  4. README coverage (each sample directory should have a readme)

Design principle: NO FALSE POSITIVES. Every reported error must be a genuine
issue. Uncertain findings are emitted as warnings (non-blocking).

Usage:
    python scripts/validate.py                  # validate everything
    python scripts/validate.py samples/aws/     # validate a subdirectory
    python scripts/validate.py --changed-only   # validate git-changed files

Exit codes:
    0  – all checks passed (warnings may still be printed)
    1  – one or more errors found
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
import urllib.error
import urllib.request

# ---------------------------------------------------------------------------
# Optional: PyYAML
# ---------------------------------------------------------------------------
try:
    import yaml  # type: ignore[import-untyped]

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent

errors: list[str] = []
warnings: list[str] = []

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def rel(path: Path) -> str:
    """Return a path relative to the repo root for readable output."""
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def error(path: Path, msg: str) -> None:
    errors.append(f"ERROR  {rel(path)}: {msg}")


def warn(path: Path, msg: str) -> None:
    warnings.append(f"WARN   {rel(path)}: {msg}")


# ---------------------------------------------------------------------------
# Action / App-ID Catalog
# ---------------------------------------------------------------------------

CATALOG_PATH = Path(__file__).resolve().parent / "known_catalog.json"
DOCS_ACTIONS_URL = (
    "https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions"
)


def load_catalog() -> dict[str, Any]:
    """Load the known action catalog from *known_catalog.json*."""
    if not CATALOG_PATH.exists():
        return {"app_ids": {}, "doc_slug_to_app_id": {}}
    try:
        with open(CATALOG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"  WARN  Could not load action catalog: {exc}")
        return {"app_ids": {}, "doc_slug_to_app_id": {}}


def _fetch_url(url: str, timeout: int = 8) -> str | None:
    """Fetch a URL and return text content, or *None* on failure."""
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "DT-Workflow-CI/1.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            return resp.read().decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001 — network errors are non-fatal
        return None


def fetch_docs_connector_slugs() -> set[str]:
    """Fetch the Dynatrace docs connector listing and extract doc slugs.

    Returns slug strings like ``{'slack', 'jira', 'service-now'}``, or an
    empty set if the request fails.
    """
    html = _fetch_url(DOCS_ACTIONS_URL)
    if not html:
        return set()
    slugs: set[str] = set()
    for m in re.finditer(r'(?:/|")actions/([a-z][a-z0-9_/-]*)', html, re.I):
        slug = m.group(1).rstrip("/")
        if slug and slug not in ("overview", "index"):
            slugs.add(slug)
    return slugs


def fetch_action_ids_from_page(url: str) -> set[str]:
    """Fetch one docs page and extract ``app_id:action_name`` patterns."""
    html = _fetch_url(url)
    if not html:
        return set()
    return {
        m.group(0)
        for m in re.finditer(
            r"dynatrace\.[a-z][a-z0-9._]*:[a-z][a-z0-9_-]+", html, re.I
        )
    }


def build_catalog(
    baseline: dict[str, Any],
    *,
    offline: bool = False,
    deep: bool = False,
) -> dict[str, Any]:
    """Merge baseline catalog with runtime-discovered data.

    *offline*: skip all HTTP requests (use baseline only).
    *deep*: crawl individual connector pages (slow; ``--update-catalog``).
    """
    catalog: dict[str, Any] = {
        "app_ids": {
            k: {**v, "actions": list(v.get("actions", []))}
            for k, v in baseline.get("app_ids", {}).items()
        },
        "doc_slug_to_app_id": dict(baseline.get("doc_slug_to_app_id", {})),
    }
    if offline:
        return catalog

    slugs = fetch_docs_connector_slugs()
    if slugs:
        known_slugs = set(catalog["doc_slug_to_app_id"].keys())
        for slug in sorted(slugs - known_slugs):
            print(f"  INFO  New connector doc slug from docs: /actions/{slug}")

    if deep and slugs:
        for slug in sorted(slugs):
            url = f"{DOCS_ACTIONS_URL}/{slug}"
            for full in fetch_action_ids_from_page(url):
                if ":" not in full:
                    continue
                app_id, act = full.split(":", 1)
                if app_id not in catalog["app_ids"]:
                    catalog["app_ids"][app_id] = {
                        "description": f"Discovered from docs ({slug})",
                        "doc_slug": slug,
                        "actions": [act],
                    }
                    catalog["doc_slug_to_app_id"][slug] = app_id
                    print(f"  INFO  Discovered app: {app_id}")
                else:
                    actions = catalog["app_ids"][app_id]["actions"]
                    if act not in actions:
                        actions.append(act)
                        actions.sort()

    return catalog


def save_catalog(catalog: dict[str, Any], baseline: dict[str, Any]) -> None:
    """Write the merged catalog back to *known_catalog.json*."""
    merged = {k: v for k, v in baseline.items() if k.startswith("_")}
    merged["app_ids"] = {k: v for k, v in sorted(catalog["app_ids"].items())}
    merged["doc_slug_to_app_id"] = dict(
        sorted(catalog["doc_slug_to_app_id"].items())
    )
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  Catalog written to {CATALOG_PATH.name}")


def scan_repo_for_actions(files: list[Path]) -> set[str]:
    """Extract unique ``app_id:action`` strings from workflow files.

    Filters out connection schema references (``app:dynatrace.xxx:name.connection``)
    which share the same ``app_id:name`` pattern but are not action IDs.
    """
    found: set[str] = set()
    _action_re = re.compile(
        r"(dynatrace\.[a-z][a-z0-9._]*:[a-z][a-z0-9_-]+)", re.I
    )
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in _action_re.finditer(text):
            candidate = m.group(1)
            _, action_part = candidate.split(":", 1)
            # Skip connection schema references:
            #   schema: app:dynatrace.xxx:name.connection
            #   connection('app:dynatrace.xxx:connection', ...)
            end = m.end()
            if end < len(text) and text[end : end + 11] == ".connection":
                continue
            if action_part == "connection":
                continue
            found.add(candidate)
    return found


def validate_action_against_catalog(
    path: Path, task_key: str, action: str, catalog: dict[str, Any]
) -> None:
    """Warn if an action's app-ID or action-name is unknown."""
    if _is_jinja(str(action)) or ":" not in str(action):
        return
    app_id, action_name = str(action).split(":", 1)
    app_data = catalog.get("app_ids", {}).get(app_id)
    if app_data is None:
        warn(
            path,
            f"Task '{task_key}': unknown app ID '{app_id}' in action '{action}'",
        )
        return
    known = app_data.get("actions", [])
    if known and action_name not in known:
        display = ", ".join(sorted(known)[:8])
        warn(
            path,
            f"Task '{task_key}': action '{action_name}' not in known list for "
            f"'{app_id}' (known: {display})",
        )


# ---------------------------------------------------------------------------
# File classification
# ---------------------------------------------------------------------------

# These paths contain non-workflow YAML/JSON that should only get syntax checks.
NON_WORKFLOW_PATTERNS: list[re.Pattern[str]] = [
    # Kubernetes manifests
    re.compile(r"(role|rolebinding|serviceaccount|secret|edgeconnect|podtermination)\.ya?ml$", re.I),
    # Ansible files
    re.compile(r"(playbook|rulebook)\.ya?ml$", re.I),
    # CloudFormation templates
    re.compile(r"cloudformation", re.I),
    # Team data
    re.compile(r"example-teams\.json$", re.I),
    # GitHub templates
    re.compile(r"\.github/", re.I),
]


def is_non_workflow(path: Path) -> bool:
    """True if the file is known to NOT be a workflow template."""
    s = rel(path)
    return any(p.search(s) for p in NON_WORKFLOW_PATTERNS)


def is_workflow_template_yaml(data: Any) -> bool:
    """Heuristic: a YAML file is a workflow template if it has the expected
    top-level keys."""
    if not isinstance(data, dict):
        return False
    # Template format: metadata + workflow
    if "metadata" in data and "workflow" in data:
        return True
    return False


def is_workflow_json(data: Any) -> bool:
    """Heuristic: a JSON file is a workflow if it contains tasks + schema info."""
    if not isinstance(data, dict):
        return False
    has_tasks = "tasks" in data and isinstance(data["tasks"], dict)
    has_schema = "schemaVersion" in data or "schema_version" in data
    # Also accept files with 'tasks' and 'title' as workflow JSON even without
    # explicit schema version (some older exports).
    return has_tasks and (has_schema or "title" in data)


# ---------------------------------------------------------------------------
# 1. YAML Syntax Validation
# ---------------------------------------------------------------------------

def validate_yaml_syntax(path: Path) -> Any | None:
    """Parse a YAML file. Returns parsed data or None on failure."""
    if not HAS_YAML:
        # Fall back: just check it loads without exception using a basic parse
        warn(path, "PyYAML not installed — skipping YAML validation")
        return None
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data
    except yaml.YAMLError as exc:
        error(path, f"Invalid YAML syntax: {exc}")
        return None
    except OSError as exc:
        error(path, f"Cannot read YAML file: {exc}")
        return None


# ---------------------------------------------------------------------------
# 2. JSON Syntax Validation
# ---------------------------------------------------------------------------

def validate_json_syntax(path: Path) -> Any | None:
    """Parse a JSON file. Returns parsed data or None on failure."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as exc:
        error(path, f"Invalid JSON syntax: {exc}")
        return None
    except UnicodeDecodeError as exc:
        error(path, f"Encoding error: {exc}")
        return None
    except OSError as exc:
        error(path, f"I/O error while reading JSON file: {exc}")
        return None


# ---------------------------------------------------------------------------
# 3. Workflow Template Structure Checks (YAML)
# ---------------------------------------------------------------------------

def validate_workflow_template(path: Path, data: dict[str, Any], catalog: dict[str, Any]) -> None:
    """Validate a YAML workflow template against known structural rules."""
    wf = data.get("workflow", {})
    if not isinstance(wf, dict):
        error(path, "'workflow' key must be a mapping")
        return

    # ── schemaVersion ──
    schema_ver = wf.get("schemaVersion")
    if schema_ver is None:
        error(path, "Missing 'workflow.schemaVersion' (must be 3)")
    elif schema_ver != 3:
        error(path, f"'workflow.schemaVersion' is {schema_ver!r}, expected 3")

    # ── title ──
    if not wf.get("title"):
        warn(path, "Missing or empty 'workflow.title'")

    # ── tasks ──
    tasks = wf.get("tasks", {})
    if not isinstance(tasks, dict):
        error(path, "'workflow.tasks' must be a mapping")
        return

    if not tasks:
        warn(path, "Workflow has no tasks defined")
        return

    task_names = set(tasks.keys())

    for key, task in tasks.items():
        if not isinstance(task, dict):
            error(path, f"Task '{key}' must be a mapping")
            continue

        # ── Task name must match key ──
        name = task.get("name")
        if name is not None and name != key:
            error(path, f"Task key '{key}' does not match its 'name' field '{name}'")

        # ── Action format ──
        action = task.get("action")
        if action and not _is_jinja(str(action)):
            # Actions follow the pattern: <app_id>:<action_name>
            if ":" not in str(action):
                error(path, f"Task '{key}': action '{action}' is missing ':' separator (expected format 'app.id:action-name')")
            elif catalog:
                validate_action_against_catalog(path, key, str(action), catalog)

        # ── Predecessors reference existing tasks ──
        preds = task.get("predecessors", [])
        if isinstance(preds, list):
            for pred in preds:
                if isinstance(pred, str) and not _is_jinja(pred) and pred not in task_names:
                    error(path, f"Task '{key}': predecessor '{pred}' does not exist in workflow tasks")

        # ── Condition states reference existing tasks ──
        conditions = task.get("conditions", {})
        if isinstance(conditions, dict):
            states = conditions.get("states", {})
            if isinstance(states, dict):
                for ref_task in states:
                    if isinstance(ref_task, str) and not _is_jinja(ref_task) and ref_task not in task_names:
                        error(path, f"Task '{key}': condition references non-existent task '{ref_task}'")

        # ── result() references should point to existing tasks ──
        _check_result_references(path, key, task, task_names)

    # ── metadata.dependencies ──
    meta = data.get("metadata", {})
    if isinstance(meta, dict):
        deps = meta.get("dependencies", {})
        if isinstance(deps, dict):
            apps = deps.get("apps", [])
            if isinstance(apps, list):
                for app in apps:
                    if isinstance(app, dict):
                        app_id = app.get("id")
                        if not app_id:
                            warn(path, "Dependency entry missing 'id'")
                        elif catalog and app_id not in catalog.get("app_ids", {}):
                            warn(path, f"Dependency app '{app_id}' not found in known catalog")


def _is_jinja(s: str) -> bool:
    """True if the string contains Jinja2 template expressions."""
    return "{{" in s or "{%" in s


def _check_result_references(
    path: Path, task_key: str, task: dict[str, Any], task_names: set[str]
) -> None:
    """Scan task input values for result('task_name') Jinja2 references and
    verify that the referenced task exists.

    Per official docs, the Run JavaScript action does NOT support Jinja2
    expressions in its ``input.script`` — result() calls there are SDK calls,
    not template expressions. We therefore exclude the script field for
    JavaScript actions to avoid false positives on SDK usage and commented-out
    code.
    """
    task_input = task.get("input", {})
    action = task.get("action", "")

    # For JavaScript actions, exclude the script field from Jinja scanning
    if isinstance(task_input, dict) and "run-javascript" in str(action):
        filtered_input = {k: v for k, v in task_input.items() if k != "script"}
        text = _deep_text(filtered_input)
    else:
        text = _deep_text(task_input)

    # Also check conditions custom field
    cond = task.get("conditions", {})
    if isinstance(cond, dict):
        custom = cond.get("custom", "")
        if isinstance(custom, str):
            text += " " + custom

    # Match result('task_name') or result("task_name")
    for m in re.finditer(r"""result\(\s*['"]([^'"]+)['"]\s*\)""", text):
        ref = m.group(1)
        # result() supports dotted access like result('task.foo') — extract task name
        ref_task = ref.split(".")[0]
        if ref_task not in task_names:
            error(path, f"Task '{task_key}': result('{ref}') references non-existent task '{ref_task}'")


def _deep_text(obj: Any) -> str:
    """Recursively extract all string values from a nested structure."""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        return " ".join(_deep_text(v) for v in obj.values())
    if isinstance(obj, list):
        return " ".join(_deep_text(v) for v in obj)
    return ""


# ---------------------------------------------------------------------------
# 4. Workflow JSON Structure Checks
# ---------------------------------------------------------------------------

def validate_workflow_json(path: Path, data: dict[str, Any], catalog: dict[str, Any]) -> None:
    """Validate a JSON workflow against known structural rules."""
    # ── schemaVersion ──
    schema_ver = data.get("schemaVersion") or data.get("schema_version")
    # Don't error if missing — older JSON exports may use "version" instead
    if schema_ver is not None and schema_ver != 3:
        warn(path, f"schemaVersion is {schema_ver!r}, expected 3")

    tasks = data.get("tasks", {})
    if not isinstance(tasks, dict):
        return

    task_names = set(tasks.keys())

    for key, task in tasks.items():
        if not isinstance(task, dict):
            continue

        # ── name must match key ──
        name = task.get("name")
        if name is not None and name != key:
            error(path, f"Task key '{key}' does not match its 'name' field '{name}'")

        # ── action format ──
        action = task.get("action")
        if action and ":" not in str(action) and not _is_jinja(str(action)):
            error(path, f"Task '{key}': action '{action}' missing ':' separator")
        elif action and catalog and ":" in str(action) and not _is_jinja(str(action)):
            validate_action_against_catalog(path, key, str(action), catalog)

        # ── predecessors ──
        preds = task.get("predecessors", [])
        if isinstance(preds, list):
            for pred in preds:
                if isinstance(pred, str) and not _is_jinja(pred) and pred not in task_names:
                    error(path, f"Task '{key}': predecessor '{pred}' does not exist")

        # ── result() references ──
        _check_result_references(path, key, task, task_names)


# ---------------------------------------------------------------------------
# 5. Secret / Credential Scanning
# ---------------------------------------------------------------------------

# Patterns that indicate REAL secrets (not placeholders).
# Each tuple: (compiled regex, human-readable description, compiled allowlist regex or None)

_SECRET_PATTERNS: list[tuple[re.Pattern[str], str, re.Pattern[str] | None]] = [
    # Dynatrace API tokens — real ones start with dt0c01., dt0s01., dt0a01., etc.
    # but NOT dt0s02.SAMPLE or placeholders
    (
        re.compile(r"\bdt0[a-z]\d{2}\.[A-Za-z0-9_-]{8,}"),
        "Possible Dynatrace API token",
        re.compile(r"dt0s02\.SAMPLE|dt0[a-z]\d{2}\.<|dt0[a-z]\d{2}\.PLACEHOLDER", re.I),
    ),
    # AWS access key IDs
    (
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "Possible AWS Access Key ID",
        None,
    ),
    # Generic private keys
    (
        re.compile(r"-----BEGIN\s+(RSA|EC|DSA|OPENSSH)?\s*PRIVATE KEY-----"),
        "Private key detected",
        None,
    ),
    # Generic Bearer tokens with actual long values (not Jinja)
    (
        re.compile(r"""(?:Authorization|authorization)['":\s]+Bearer\s+[A-Za-z0-9._~+/=-]{20,}"""),
        "Possible hardcoded Bearer token",
        re.compile(r"\{\{|\bsecret\(|<REPLACE|PLACEHOLDER", re.I),
    ),
]


def scan_secrets(path: Path) -> None:
    """Scan a file for potential hardcoded secrets."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    for pattern, desc, allowlist in _SECRET_PATTERNS:
        for m in pattern.finditer(text):
            matched = m.group(0)
            # Check allowlist
            if allowlist and allowlist.search(matched):
                continue
            # Extra safety: skip anything inside Jinja expressions
            # Find surrounding context
            start = max(0, m.start() - 30)
            context = text[start : m.end() + 30]
            if "{{" in context and "}}" in context:
                continue
            if "secret(" in context.lower():
                continue
            line_no = text.count("\n", 0, m.start()) + 1
            warn(path, f"{desc} at line {line_no} (secret value redacted)")


# ---------------------------------------------------------------------------
# 6. README Coverage
# ---------------------------------------------------------------------------

def check_readme_coverage(sample_dirs: set[Path]) -> None:
    """Warn if a sample directory has no README file."""
    for d in sorted(sample_dirs):
        readmes = list(d.glob("[Rr][Ee][Aa][Dd][Mm][Ee]*"))
        if not readmes:
            warn(d, "Sample directory has no README file")


# ---------------------------------------------------------------------------
# 7. Internal link validation (Markdown)
# ---------------------------------------------------------------------------

def validate_markdown_links(path: Path) -> None:
    """Check that relative links in Markdown files point to existing paths."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    # Match [text](relative/path) — skip URLs, anchors, and mailto
    for m in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", text):
        target = m.group(2).strip()
        # Skip external URLs, anchors, mailto, template vars
        if re.match(r"(https?://|mailto:|#|\{\{)", target, re.I):
            continue
        # Strip anchor from relative path
        target_path = target.split("#")[0]
        if not target_path:
            continue
        resolved = (path.parent / target_path).resolve()
        if not resolved.exists():
            warn(path, f"Broken relative link: [{m.group(1)}]({target})")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def collect_files(roots: list[Path]) -> list[Path]:
    """Collect all relevant files under the given roots."""
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            for dirpath, _dirnames, filenames in os.walk(root):
                for fn in filenames:
                    files.append(Path(dirpath) / fn)
    return sorted(set(files))


def get_changed_files() -> list[Path]:
    """Return files changed compared to the default branch (for PRs)."""
    # Try to detect the merge base with origin/main
    for base in ("origin/main", "main", "HEAD~1"):
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=ACMR", base],
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
                check=True,
            )
            paths = [REPO_ROOT / line.strip() for line in result.stdout.splitlines() if line.strip()]
            return [p for p in paths if p.exists()]
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Dynatrace Workflow samples")
    parser.add_argument("paths", nargs="*", help="Files or directories to validate (default: repo root)")
    parser.add_argument("--changed-only", action="store_true", help="Only validate git-changed files")
    parser.add_argument("--offline", action="store_true", help="Skip network requests; use baseline catalog only")
    parser.add_argument("--update-catalog", action="store_true",
                        help="Scan repo and docs, then update known_catalog.json")
    args = parser.parse_args()

    # ── Load action / app-ID catalog ──
    baseline = load_catalog()
    catalog = build_catalog(baseline, offline=args.offline, deep=args.update_catalog)

    if args.update_catalog:
        all_files = collect_files([REPO_ROOT])
        discovered = scan_repo_for_actions(all_files)
        for full_action in sorted(discovered):
            if ":" not in full_action:
                continue
            app_id, act = full_action.split(":", 1)
            if app_id not in catalog["app_ids"]:
                catalog["app_ids"][app_id] = {
                    "description": "Discovered from repo",
                    "doc_slug": None,
                    "actions": [act],
                }
                print(f"  INFO  New app from repo: {app_id}")
            else:
                actions = catalog["app_ids"][app_id]["actions"]
                if act not in actions:
                    actions.append(act)
                    actions.sort()
                    print(f"  INFO  New action from repo: {app_id}:{act}")
        save_catalog(catalog, baseline)
        print("  Catalog update complete.")
        return 0

    if args.changed_only:
        files = get_changed_files()
        if not files:
            print("No changed files detected — nothing to validate.")
            return 0
    elif args.paths:
        files = collect_files([Path(p) for p in args.paths])
    else:
        files = collect_files([REPO_ROOT])

    # Directories containing sample files (for README check)
    sample_dirs: set[Path] = set()

    yaml_extensions = {".yaml", ".yml"}
    json_extensions = {".json"}
    md_extensions = {".md"}

    for f in files:
        suffix = f.suffix.lower()

        # Track sample directories
        try:
            frel = f.resolve().relative_to(REPO_ROOT / "samples")
            # Collect the immediate subdirectory under samples/
            parts = frel.parts
            if len(parts) >= 2:
                sample_dirs.add(REPO_ROOT / "samples" / parts[0])
                # Also add nested dirs (e.g., security/threat detection/)
                if len(parts) >= 3:
                    sample_dirs.add(REPO_ROOT / "samples" / parts[0] / parts[1])
        except ValueError:
            pass

        # ── YAML files ──
        if suffix in yaml_extensions:
            data = validate_yaml_syntax(f)
            if data is None:
                continue

            if not is_non_workflow(f) and is_workflow_template_yaml(data):
                validate_workflow_template(f, data, catalog)

            scan_secrets(f)

        # ── JSON files ──
        elif suffix in json_extensions:
            data = validate_json_syntax(f)
            if data is None:
                continue

            if not is_non_workflow(f) and is_workflow_json(data):
                validate_workflow_json(f, data, catalog)

            scan_secrets(f)

        # ── Markdown files ──
        elif suffix in md_extensions:
            validate_markdown_links(f)

        # ── JavaScript files ──
        elif suffix == ".js":
            scan_secrets(f)

    # README coverage check
    if sample_dirs:
        check_readme_coverage(sample_dirs)

    # ── Report ──
    if warnings:
        print(f"\n{'='*60}")
        print(f"  WARNINGS ({len(warnings)})")
        print(f"{'='*60}")
        for w in sorted(warnings):
            print(f"  {w}")

    if errors:
        print(f"\n{'='*60}")
        print(f"  ERRORS ({len(errors)})")
        print(f"{'='*60}")
        for e in sorted(errors):
            print(f"  {e}")
        print(f"\n❌ Validation failed with {len(errors)} error(s).\n")
        return 1

    print(f"\n✅ Validation passed ({len(files)} files checked, {len(warnings)} warning(s)).\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
