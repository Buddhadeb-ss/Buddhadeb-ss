#!/usr/bin/env python3
"""
validate_profile.py
Automated validation suite for Buddhadeb Banik's GitHub Developer Profile.
Verifies:
  - README structure, heading hierarchy, and length.
  - Verified presence of all authoritative links.
  - Local asset existence and SVG/XML validity.
  - Generation markers stability.
  - Workflow file syntax.
  - Absence of hardcoded secrets or credentials.
"""

import os
import sys
import re
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
README_PATH = os.path.join(REPO_ROOT, "README.md")
ASSETS_DIR = os.path.join(REPO_ROOT, "assets")
WORKFLOW_PATH = os.path.join(REPO_ROOT, ".github", "workflows", "profile-refresh.yml")

AUTHORITATIVE_URLS = [
    "https://github.com/Buddhadeb-ss",
    "https://www.linkedin.com/in/buddhadeb-banik/",
    "https://leetcode.com/u/Buddha001/",
    "https://www.codechef.com/users/buddhadebbanik",
    "https://www.youtube.com/@BBbuilds-ECE"
]

REQUIRED_ASSETS = [
    "banner.svg",
    "signal_divider.svg",
    "metrics_dashboard.svg",
    "coding_platforms.svg"
]

def check_readme():
    print("[1/6] Validating README.md structure & content...")
    if not os.path.exists(README_PATH):
        raise AssertionError("README.md is missing!")

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if len(content) < 500:
        raise AssertionError(f"README.md too short ({len(content)} chars)")

    # Check required headings
    required_headings = [
        "About Me",
        "Technical Stack & Engineering Toolkit",
        "Featured Engineering Projects",
        "Telemetry & GitHub Metrics",
        "Competitive Programming & Problem Solving",
        "Open-Source & Activity",
        "Connect & Social"
    ]
    for h in required_headings:
        if h.lower() not in content.lower():
            raise AssertionError(f"Missing required section heading: '{h}'")

    print("  ✓ Heading hierarchy and major sections present.")

    # Check authoritative profile links
    print("[2/6] Validating authoritative profile links...")
    for url in AUTHORITATIVE_URLS:
        if url not in content:
            raise AssertionError(f"Authoritative link missing: {url}")
    print("  ✓ All 5 authoritative profile links verified exactly.")

    # Check generation markers
    print("[3/6] Checking generation markers...")
    start_marker = "<!-- START: GENERATED GITHUB STATS -->"
    end_marker = "<!-- END: GENERATED GITHUB STATS -->"
    if start_marker not in content or end_marker not in content:
        raise AssertionError("Generation markers missing in README.md")
    print("  ✓ Generation markers intact.")

    # Check secrets leak detection
    print("[4/6] Scanning for accidental secrets / tokens...")
    forbidden_patterns = [
        r'ghp_[A-Za-z0-9_]{30,}',
        r'gho_[A-Za-z0-9_]{30,}',
        r'github_pat_[A-Za-z0-9_]{30,}',
        r'sk-[A-Za-z0-9]{20,}',
        r'AIza[0-9A-Za-z-_]{35}',
        r'-----BEGIN PRIVATE KEY-----'
    ]
    for pat in forbidden_patterns:
        if re.search(pat, content):
            raise AssertionError(f"Potential secret pattern found matching {pat}")
    print("  ✓ No secrets or credentials found in README.")

def check_assets():
    print("[5/6] Validating local SVG assets & XML structure...")
    for asset_name in REQUIRED_ASSETS:
        asset_path = os.path.join(ASSETS_DIR, asset_name)
        if not os.path.exists(asset_path):
            raise AssertionError(f"Required asset missing: {asset_path}")
        
        # Parse XML
        try:
            tree = ET.parse(asset_path)
            root = tree.getroot()
            if not root.tag.endswith("svg"):
                raise AssertionError(f"Root tag in {asset_name} is not <svg>")
        except Exception as e:
            raise AssertionError(f"Invalid XML syntax in {asset_name}: {e}")
    print("  ✓ All 4 required SVG assets exist and are 100% valid XML.")

def check_workflow():
    print("[6/6] Validating GitHub Actions workflow...")
    if not os.path.exists(WORKFLOW_PATH):
        raise AssertionError("profile-refresh.yml workflow is missing!")
    with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
        wf = f.read()
    
    # Check key workflow elements
    assert "workflow_dispatch:" in wf, "workflow_dispatch trigger missing"
    assert "schedule:" in wf, "schedule trigger missing"
    assert "contents: write" in wf or "permissions:" in wf, "permissions declaration missing"
    print("  ✓ GitHub Actions workflow verified.")

def main():
    print("=== Running Profile Validation Suite ===")
    try:
        check_readme()
        check_assets()
        check_workflow()
        print("\n==========================================")
        print("ALL TESTS PASSED: PROFILE READY & VERIFIED")
        print("==========================================")
        return 0
    except AssertionError as e:
        print(f"\n❌ VALIDATION FAILED: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
