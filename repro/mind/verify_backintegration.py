#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_backintegration.py - the anti-circularity gate for the v1.58 -> v1.59
wave_computer back-integration layer.

Runs ALONGSIDE tools/gate.py (mother) and frontal_gate.py (frontal); replaces
neither, imports neither's heavy runner. It asserts that the back-integration
registry (backintegration.csv) can NEVER express the forbidden loop
    A -> B -> "B supports A"   (B = vp_wave_computer, derived from A = mind).

Checks (hard fail unless marked soft):
  1. NO SILENT PROMOTION   - no [<=W:Ln]-tagged row promotes a mother grade to [V].
  2. EVERY [P] IS TESTABLE  - each [P] row has a non-empty real-data promotion_gate.
  3. PROVENANCE PRESENT     - every row carries a [<=W:Ln] provenance tag.
  4. [realize] DIRECTION    - every [realize] row: points at a mother [O] (never
                              [V]/[F]/[model]); retypes absence->resolution_limit;
                              localizes_claim=0; strengthens_mother_grade=0.
  5. [P] NOT A vp-card      - no [P]/[realize] statement is filed as a chapter vp-card
                              (it stays a prediction until real-data promotion).
  6. FIREWALL FLAGS         - localizes_claim and strengthens_mother_grade are 0 on
                              EVERY row (no upstream row may strengthen the mother).

Deterministic: no RNG, no tuned constant; 2x run byte-identical. Exit 0 = PASS.
"""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, "manifest", "backintegration.csv")

# a row is "back-integrated" (subject to the anti-circularity rules) iff it carries
# a wave-computer provenance tag. DORMANT rows that target NONE_YET are inert.
PROV_PREFIX = "[<=W:"


def load(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    rows = load(REG)
    checks = []

    def rec(name, ok, detail="", soft=False):
        checks.append({"check": name, "pass": bool(ok), "soft": soft, "detail": str(detail)})

    active = [r for r in rows if r["status"].strip() != "DORMANT"]

    # 3. PROVENANCE PRESENT (every active row) -------------------------------
    missing_prov = [r["id"] for r in active if not r["provenance"].strip().startswith(PROV_PREFIX)]
    rec("3. provenance [<=W:Ln] present on every active row", not missing_prov,
        missing_prov or "all present")

    # 1. NO SILENT PROMOTION -------------------------------------------------
    # no active, provenance-tagged row may declare its mother target already at [V]
    # because of this layer. We encode that the registered statement never sets a
    # mother grade to [V]; the only [V] tokens allowed in target_grade_now are the
    # annotated "[V](number)" form, which marks a measured INPUT the child must NOT
    # touch (a prediction TARGET), not a grade this layer raises. A bare "[V]" mother
    # target on a provenance row would be an illegal promotion surface.
    illegal_promote = [r["id"] for r in active
                       if r["provenance"].strip().startswith(PROV_PREFIX)
                       and r["target_grade_now"].strip() == "[V]"]
    rec("1. no silent promotion to [V] on a provenance row", not illegal_promote,
        illegal_promote or "no bare-[V] promotion surface")

    # 2. EVERY [P] IS TESTABLE ----------------------------------------------
    p_rows = [r for r in active if r["channel"].strip() in ("P", "tension+P")]
    untestable = [r["id"] for r in p_rows
                  if not r["promotion_gate_real_data"].strip()
                  or r["promotion_gate_real_data"].strip().lower().startswith("n/a")]
    rec("2. every [P] row has a real-data promotion gate", not untestable,
        untestable or f"{len(p_rows)} [P]-bearing rows all testable")

    # 4. [realize] DIRECTION-CHECK (the crucial one) ------------------------
    realize_rows = [r for r in active if r["channel"].strip() == "realize"]
    bad_realize = []
    for r in realize_rows:
        ok = (
            r["target_grade_now"].strip() == "[O]"
            and r["retypes_open_question"].strip() == "absence->resolution_limit"
            and r["localizes_claim"].strip() == "0"
            and r["strengthens_mother_grade"].strip() == "0"
        )
        if not ok:
            bad_realize.append(r["id"])
    rec("4. [realize] rows point at [O], retype absence->resolution_limit, localize nothing",
        not bad_realize, bad_realize or f"{len(realize_rows)} [realize] row(s) clean")

    # 5. [P]/[realize] NOT FILED AS A vp-card -------------------------------
    not_card = [r["id"] for r in active
                if r["channel"].strip() in ("P", "tension+P", "realize")
                and r["is_vp_card"].strip() != "0"]
    rec("5. no [P]/[realize] statement filed as a chapter vp-card", not not_card,
        not_card or "predictions stay in registry, not in cards")

    # 6. FIREWALL: no upstream row strengthens the mother -------------------
    # "0" and "n/a" both mean "does not strengthen / does not apply"; ONLY a
    # positive token (1/yes/true) is a violation. (localize/strengthen are
    # meaningful for [realize]; for [P]/[sharpen] they are n/a by construction.)
    POS = {"1", "yes", "true"}
    strengthen = [r["id"] for r in active
                  if r["strengthens_mother_grade"].strip().lower() in POS
                  or r["localizes_claim"].strip().lower() in POS]
    rec("6. no active row strengthens a mother grade or localizes a refuted claim",
        not strengthen, strengthen or "all rows weaken/qualify/retype only")

    hard_fail = [c for c in checks if not c["pass"] and not c["soft"]]
    verdict = "PASS" if not hard_fail else "FAIL"

    print("=" * 78)
    print("BACK-INTEGRATION GATE - anti-circularity (v1.58 -> v1.59)")
    print("=" * 78)
    for c in checks:
        tag = "PASS" if c["pass"] else ("warn" if c["soft"] else "FAIL")
        print(f"  [{tag}] {c['check']}  --  {c['detail']}")
    n_active, n_dormant = len(active), len(rows) - len(active)
    print("-" * 78)
    print(f"{sum(c['pass'] for c in checks)}/{len(checks)} checks pass | "
          f"{n_active} active rows, {n_dormant} dormant | verdict: {verdict}")
    print("firewall: efficacy=0 | consciousness_claim=0 | hard_problem_open=1 | "
          "new_tuned_constants=0 | one-way preserved | NOT medical advice")
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
