import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from blisspoint import Dials, Subtask, Task, compile, cross_family, list_profiles, resolve
from blisspoint.profiles import load_profile


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
        self.assertTrue(any("decomposition is high" in g for g in b.gaps))

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
        self.assertTrue(any("autonomy is high" in g for g in b.gaps))

    def test_grok_stays_narrow(self):
        b = compile("Which retry strategy is safer here?", "grok", phase="review")
        self.assertIn("Start a new conversation", b.text)
        self.assertLess(len(b.text), 1200)

    def test_bulky_evidence_flagged_for_narrow_agents(self):
        t = Task(objective="Audit this.", evidence="x" * 3000)
        b = compile(t, "grok", phase="review")
        self.assertTrue(any("compress it" in g for g in b.gaps))

    def test_string_task_shorthand(self):
        self.assertIn("Objective", compile("ship it", "codex").text)

    def test_unknown_task_field_raises(self):
        with self.assertRaises(KeyError):
            compile({"objective": "x", "wat": 1}, "codex")


class TestCrossFamily(unittest.TestCase):
    def test_validator_is_never_same_family(self):
        for v in cross_family("balthasar"):
            self.assertNotEqual(load_profile(v).family, "minimax")

    def test_author_excluded(self):
        self.assertNotIn("codex", cross_family("codex"))


if __name__ == "__main__":
    unittest.main()
