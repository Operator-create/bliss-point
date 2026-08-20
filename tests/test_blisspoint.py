import os
import shutil
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from blisspoint import (
    Dials, ProfileError, Subtask, Task, compile, correlation, cross_family,
    emitted, flat, list_profiles, resolve,
)
from blisspoint.profiles import load_profile


def codes(brief):
    """Consumers branch on gap codes, never on the English message."""
    return {g.code for g in brief.gaps}


class TestDials(unittest.TestCase):
    def test_clamped(self):
        self.assertEqual(Dials(autonomy=1.7).autonomy, 1.0)
        self.assertEqual(Dials(autonomy=-3).autonomy, 0.0)

    def test_unknown_dial_raises(self):
        with self.assertRaises(KeyError):
            Dials().shifted({"vibes": 0.5})


class TestResolution(unittest.TestCase):
    def test_deterministic(self):
        a = resolve("codex", "implement", "high")[1]
        b = resolve("codex", "implement", "high")[1]
        self.assertEqual(a, b)

    def test_phase_moves_the_point(self):
        impl = resolve("claude", "implement")[1]
        design = resolve("claude", "design")[1]
        self.assertGreater(design.autonomy, impl.autonomy)
        self.assertLess(design.specificity, impl.specificity)

    def test_high_stakes_tightens(self):
        normal = resolve("codex", "implement", "normal")[1]
        high = resolve("codex", "implement", "high")[1]
        self.assertGreater(high.verification_rigor, normal.verification_rigor)
        self.assertLess(high.autonomy, normal.autonomy)

    def test_every_profile_loads(self):
        self.assertTrue(list_profiles())
        for name in list_profiles():
            p = load_profile(name)
            self.assertTrue(p.family and p.role, name)

    def test_unknown_phase_raises(self):
        with self.assertRaises(KeyError):
            resolve("codex", "vibing")


class TestShape(unittest.TestCase):
    """The same task must come out shaped differently per target."""

    task = Task(
        objective="Make the payment retry converge on one terminal state.",
        instructions="Move idempotency into the state machine.",
        acceptance=["replaying a capture event twice leaves one paid order"],
        verification="pytest tests/payments -k retry",
    )

    def test_codex_gets_an_imperative(self):
        b = compile(self.task, "codex", phase="implement")
        self.assertIn("## Task", b.text)
        self.assertNotIn("## Subtasks", b.text)
        self.assertIn("## Verification", b.text)

    def test_antigravity_demands_subtasks(self):
        b = compile(self.task, "antigravity", phase="implement")
        self.assertIn("subtasks_missing", codes(b))

    def test_subtasks_carry_their_own_criteria(self):
        t = Task(
            objective="Rebuild the settings screen to match the reference.",
            evidence="Reference: design/settings-390.png, design/settings-1024.png",
            subtasks=[Subtask(id="ST1", title="Layout", acceptance=["matches ref at 390px"],
                              verification="screenshot diff")],
        )
        b = compile(t, "antigravity", phase="implement")
        self.assertIn("### ST1", b.text)
        self.assertIn("Acceptance criteria:", b.text)
        self.assertEqual(b.gaps, [])

    def test_claude_is_asked_to_decide(self):
        t = Task(objective="Choose the persistence layer.",
                 open_decisions=["sqlite vs postgres"])
        b = compile(t, "claude", phase="design")
        self.assertIn("## Decisions you own", b.text)

    def test_high_autonomy_without_open_decisions_is_a_gap(self):
        b = compile("Choose the persistence layer.", "claude", phase="design")
        self.assertIn("open_decisions_missing", codes(b))

    def test_grok_stays_narrow(self):
        b = compile("Which retry strategy is safer here?", "grok", phase="review")
        self.assertIn("Start a new conversation", b.text)
        self.assertLess(len(b.text), 1200)

    def test_bulky_evidence_flagged_for_narrow_agents(self):
        t = Task(objective="Audit this.", evidence="x" * 3000)
        b = compile(t, "grok", phase="review")
        self.assertIn("evidence_bulky", codes(b))
        gap = next(g for g in b.gaps if g.code == "evidence_bulky")
        self.assertEqual(gap.details["actual_chars"], 3000)

    def test_string_task_shorthand(self):
        self.assertIn("Objective", compile("ship it", "codex").text)

    def test_unknown_task_field_raises(self):
        with self.assertRaises(KeyError):
            compile({"objective": "x", "wat": 1}, "codex")


class TestGapContract(unittest.TestCase):
    """Codes are the API; the message wording is not."""

    def test_codes_are_stable_identifiers(self):
        b = compile(Task(objective="Rebuild the screen.",
                         subtasks=[Subtask(id="ST1", title="Layout")]),
                    "antigravity", phase="implement")
        self.assertLessEqual(
            {"subtask_acceptance_missing", "subtask_verification_missing"}, codes(b))
        gap = next(g for g in b.gaps if g.code == "subtask_acceptance_missing")
        self.assertEqual(gap.details["subtask_ids"], ["ST1"])

    def test_message_still_readable(self):
        b = compile("", "codex")
        self.assertIn("objective is empty", str(b.gaps[0]))

    def test_fresh_conversation_matches_the_rendered_banner(self):
        for target in list_profiles():
            for phase in ("research", "implement", "review"):
                b = compile("x", target, phase=phase)
                self.assertEqual(b.fresh_conversation,
                                 "Start a new conversation" in b.text,
                                 f"{target}/{phase}")


class TestProfileDirectoryContract(unittest.TestCase):
    """A custom profiles directory is a complete configuration, validated on load."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self._prev = os.environ.get("BLISSPOINT_PROFILES")
        os.environ["BLISSPOINT_PROFILES"] = self.tmp
        self.addCleanup(self._restore)

    def _restore(self):
        if self._prev is None:
            os.environ.pop("BLISSPOINT_PROFILES", None)
        else:
            os.environ["BLISSPOINT_PROFILES"] = self._prev

    def write(self, name, text):
        Path(self.tmp, name).write_text(textwrap.dedent(text))

    def minimal(self):
        self.write("_phases.yaml", "implement: {}\n")
        self.write("_stakes.yaml", "normal: {}\n")
        self.write("mine.yaml", """\
            family: acme
            role: doer
            dials:
              autonomy: 0.2
            """)

    def test_a_valid_custom_directory_works(self):
        self.minimal()
        self.assertEqual(list_profiles(), ["mine"])
        self.assertEqual(resolve("mine")[1].autonomy, 0.2)

    def test_missing_modifier_tables_fail_loudly(self):
        self.write("mine.yaml", "family: acme\nrole: doer\n")
        with self.assertRaises(ProfileError) as ctx:
            resolve("mine")
        self.assertIn("_phases.yaml", str(ctx.exception))

    def test_typo_in_dials_key_does_not_resolve_to_defaults(self):
        self.minimal()
        self.write("mine.yaml", """\
            family: acme
            role: doer
            dial:
              autonomy: 0.2
            """)
        with self.assertRaises(ProfileError):
            resolve("mine")

    def test_unknown_dial_name_is_rejected(self):
        self.minimal()
        self.write("mine.yaml", """\
            family: acme
            role: doer
            dials:
              vibes: 0.9
            """)
        with self.assertRaises(ProfileError):
            resolve("mine")

    def test_family_is_required_because_validators_depend_on_it(self):
        self.minimal()
        self.write("mine.yaml", "role: doer\n")
        with self.assertRaises(ProfileError):
            resolve("mine")

    def test_name_must_match_filename(self):
        self.minimal()
        self.write("mine.yaml", "name: other\nfamily: acme\nrole: doer\n")
        with self.assertRaises(ProfileError):
            resolve("mine")

    def test_yaml_string_false_is_not_true(self):
        self.minimal()
        self.write("mine.yaml", """\
            family: acme
            role: doer
            fresh_conversation_default: "false"
            """)
        with self.assertRaises(ProfileError):
            resolve("mine")

    def test_modifier_tables_are_validated_too(self):
        self.minimal()
        self.write("_phases.yaml", "implement:\n  vibes: 0.1\n")
        with self.assertRaises(ProfileError):
            resolve("mine")


class TestBlockingGaps(unittest.TestCase):
    """Only two conditions stop a dispatch; the rest advise."""

    def test_no_objective_blocks(self):
        b = compile("", "codex")
        self.assertIn("objective_empty", [g.code for g in b.blocking_gaps])

    def test_missing_acceptance_blocks_only_when_contract_is_tight(self):
        tight = compile("ship it", "codex", phase="implement")
        self.assertIn("acceptance_missing", [g.code for g in tight.blocking_gaps])

        loose = compile("which retry strategy is safer?", "grok", phase="review")
        self.assertNotIn("acceptance_missing", [g.code for g in loose.blocking_gaps])

    def test_subtask_criteria_missing_blocks_when_the_contract_is_tight(self):
        """The gate had a hole: high acceptance_binding moves the criteria into the
        subtasks, and that branch only advised. A brief for a tight-contract profile could
        carry no observable definition of done anywhere and still dispatch. Found while
        building the corpus admissibility gate, which is the point of building it first.
        """
        t = Task(objective="Guard the capture transition.",
                 subtasks=[Subtask(id="ST1", title="make it idempotent")])
        tight = compile(t, "antigravity", phase="implement")   # acceptance_binding 1.0
        self.assertIn("subtask_acceptance_missing", [g.code for g in tight.blocking_gaps])

        withcriteria = Task(objective="Guard the capture transition.",
                            subtasks=[Subtask(id="ST1", title="make it idempotent",
                                              acceptance=["replay yields one paid order"])])
        ok = compile(withcriteria, "antigravity", phase="implement")
        self.assertNotIn("subtask_acceptance_missing", [g.code for g in ok.blocking_gaps])

    def test_acceptance_survives_when_subtasks_are_not_rendered(self):
        """The two branches each assumed the other was carrying the criteria.

        `codex` sits at decomposition 0.35 and acceptance_binding 0.9 — deliberately, that
        is the "hand a principal engineer the contract, not a checklist" shape. A Task with
        subtasks hit both branches wrong: the top-level acceptance section was skipped
        because binding was high and subtasks existed, and the subtasks were never rendered
        because decomposition was low. Criteria dropped silently, with no gap raised.
        """
        t = Task(objective="Ship it.",
                 subtasks=[Subtask(id="ST1", title="do the thing",
                                   acceptance=["the thing is done"])],
                 acceptance=["the suite is green"])
        for target in list_profiles():
            b = compile(t, target, phase="implement")
            self.assertIn("the suite is green" if b.dials.decomposition < 0.6
                          else "the thing is done", b.text, target)

    def test_advisory_gaps_do_not_block(self):
        b = compile(Task(objective="Audit this.", evidence="x" * 3000), "grok", phase="review")
        self.assertIn("evidence_bulky", codes(b))
        self.assertNotIn("evidence_bulky", [g.code for g in b.blocking_gaps])


class TestDialIndependence(unittest.TestCase):
    """D6: are seven dials seven axes, or fewer wearing more names?"""

    def test_correlation_covers_every_pair(self):
        pts = [load_profile(n).dials for n in list_profiles()]
        c = correlation(pts)
        self.assertEqual(len(c), 21)  # 7 choose 2
        self.assertTrue(all(-1.0 <= v <= 1.0 for v in c.values()))

    def test_refuses_to_report_on_too_few_profiles(self):
        with self.assertRaises(ValueError):
            correlation([Dials(), Dials()])


UNION_COMPLETE = Task(
    objective="Make the retried capture converge on one terminal state.",
    current_state="The handler is idempotent; the state machine is not.",
    files=["api/payments/webhook.py"],
    decisions=["The public API contract does not change."],
    constraints=["No new database columns."],
    non_goals=["Rewriting the state machine."],
    evidence="Sentry PAY-4471: 38 orders stuck pending.",
    attempts="A dedupe set in the handler moved the race.",
    instructions="Move idempotency into the state machine.",
    subtasks=[Subtask(id="ST1", title="Guard the capture transition",
                      purpose="stop double-apply", scope="api/orders/state.py",
                      instructions="make the transition idempotent",
                      acceptance=["replaying capture twice yields one paid order"],
                      verification="pytest tests/payments -k retry",
                      returns="the diff")],
    acceptance=["replaying a capture event twice leaves one paid order"],
    verification="pytest tests/payments -k retry",
    open_decisions=["whether to key on event id or transition id"],
    escalation_triggers=["the fix requires a schema change"],
    return_format=["changed files", "test output"],
)


class TestFlatRenderer(unittest.TestCase):
    """Arm F is the experimental control. These tests are what make that true."""

    def test_takes_no_recipient(self):
        """It cannot vary by profile because it is never given one."""
        import inspect
        self.assertEqual(list(inspect.signature(flat).parameters), ["task"])

    def test_drops_nothing(self):
        """Every populated field of the Task appears in the output."""
        text = flat(UNION_COMPLETE)
        populated = {f for f, _ in __import__(
            "blisspoint.flat", fromlist=["SECTIONS"]).SECTIONS
            if getattr(UNION_COMPLETE, f)}
        self.assertEqual(emitted(text, UNION_COMPLETE), populated)

    def test_flat_carries_a_superset_of_every_compiled_brief(self):
        """The control must never hold less information than the arm it controls for.

        This is the property the whole comparison rests on: if arm C wins while carrying a
        subset of arm F's content, shaping did the work rather than field-gathering.
        """
        f_fields = emitted(flat(UNION_COMPLETE), UNION_COMPLETE)
        for target in list_profiles():
            for phase in ("research", "design", "implement", "review", "verify", "synthesize"):
                c = compile(UNION_COMPLETE, target, phase=phase)
                c_fields = emitted(c.text, UNION_COMPLETE)
                self.assertLessEqual(c_fields, f_fields, f"{target}/{phase}")

    def test_compiled_briefs_really_do_drop_things(self):
        """Sanity check on the above: if C never dropped anything, the comparison is vacuous."""
        f_fields = emitted(flat(UNION_COMPLETE), UNION_COMPLETE)
        dropped_somewhere = any(
            emitted(compile(UNION_COMPLETE, t, phase=p).text, UNION_COMPLETE) < f_fields
            for t in list_profiles()
            for p in ("research", "implement", "synthesize"))
        self.assertTrue(dropped_somewhere)

    def test_subtask_fields_are_all_rendered(self):
        text = flat(UNION_COMPLETE)
        for fragment in ("ST1", "stop double-apply", "api/orders/state.py",
                         "replaying capture twice", "pytest tests/payments -k retry"):
            self.assertIn(fragment, text)

    def test_section_order_is_fixed(self):
        text = flat(UNION_COMPLETE)
        order = [text.index(h) for h in
                 ("## Objective", "## Evidence", "## Subtasks", "## Return")]
        self.assertEqual(order, sorted(order))

    def test_accepts_the_same_inputs_as_compile(self):
        self.assertIn("ship it", flat("ship it"))
        self.assertIn("ship it", flat({"objective": "ship it"}))


class TestCrossFamily(unittest.TestCase):
    def test_validator_is_never_same_family(self):
        for v in cross_family("balthasar"):
            self.assertNotEqual(load_profile(v).family, "minimax")

    def test_author_excluded(self):
        self.assertNotIn("codex", cross_family("codex"))


if __name__ == "__main__":
    unittest.main()
