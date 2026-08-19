"""Task in, Brief out.

`Task` is what you know about the work. `Brief` is what an agent should be
handed. The dials decide which sections exist, in what form -- they never
invent content. If a dial demands a section you did not supply, that becomes a
gap, not a hallucination.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .dials import Dials

# A brief that leans on evidence this long has stopped being a handoff.
BULKY_EVIDENCE_CHARS = 2000


@dataclass
class Subtask:
    id: str
    title: str
    purpose: str = ""
    scope: str = ""
    depends_on: list = field(default_factory=list)
    instructions: str = ""
    acceptance: list = field(default_factory=list)
    verification: str = ""
    returns: str = ""


@dataclass
class Task:
    objective: str
    current_state: str = ""
    files: list = field(default_factory=list)
    decisions: list = field(default_factory=list)     # already settled, do not reopen
    constraints: list = field(default_factory=list)
    non_goals: list = field(default_factory=list)
    evidence: str = ""
    attempts: str = ""
    subtasks: list = field(default_factory=list)      # list[Subtask]
    instructions: str = ""
    acceptance: list = field(default_factory=list)
    verification: str = ""
    open_decisions: list = field(default_factory=list)  # decisions the agent owns
    escalation_triggers: list = field(default_factory=list)
    return_format: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw: dict) -> "Task":
        raw = dict(raw)
        raw["subtasks"] = [
            s if isinstance(s, Subtask) else Subtask(**s) for s in raw.get("subtasks", [])
        ]
        known = {f for f in cls.__dataclass_fields__}
        unknown = set(raw) - known
        if unknown:
            raise KeyError(f"unknown task field(s): {sorted(unknown)}")
        return cls(**raw)


@dataclass
class Brief:
    text: str
    dials: Dials
    target: str
    phase: str
    stakes: str
    gaps: list = field(default_factory=list)
    fresh_conversation: bool = True

    def __str__(self) -> str:
        return self.text


def _bullets(items) -> str:
    return "\n".join(f"- {i}" for i in items)


def _section(title: str, body: str) -> str:
    return f"## {title}\n{body.strip()}\n" if body.strip() else ""


def _render_subtask(st: Subtask, bind_acceptance: bool, rigor: float) -> str:
    out = [f"### {st.id} — {st.title}"]
    if st.purpose:
        out.append(f"Purpose: {st.purpose}")
    if st.scope:
        out.append(f"Scope: {st.scope}")
    out.append(f"Depends on: {', '.join(st.depends_on) if st.depends_on else 'nothing'}")
    if st.instructions:
        out.append(f"Instructions: {st.instructions}")
    if bind_acceptance and st.acceptance:
        out.append("Acceptance criteria:\n" + _bullets(st.acceptance))
    if rigor >= 0.6 and st.verification:
        out.append(f"Verification: {st.verification}")
    if st.returns:
        out.append(f"Return: {st.returns}")
    return "\n".join(out) + "\n"


def render(task: Task, dials: Dials, profile) -> tuple:
    """Return (text, gaps). Pure -- no I/O, no model calls."""
    d = dials
    gaps: list = []
    parts: list = []

    if not task.objective.strip():
        gaps.append("objective is empty — every brief needs one concrete outcome")

    parts.append(f"# {profile.name.upper()} — {profile.role or 'task'}\n")

    if d.context_volume < 0.4 and profile.fresh_conversation_default:
        parts.append(
            "> Start a new conversation. Everything needed is below; prior history is not.\n"
        )

    parts.append(_section("Objective", task.objective.strip()))

    if d.context_volume >= 0.35:
        parts.append(_section("Current state", task.current_state))
    if task.files:
        parts.append(_section("Relevant files", _bullets(task.files)))
    if task.decisions:
        parts.append(_section(
            "Accepted decisions (do not reopen without evidence)", _bullets(task.decisions)))
    if task.constraints or task.non_goals:
        body = _bullets(task.constraints)
        if task.non_goals:
            body += ("\n" if body else "") + _bullets(f"NON-GOAL: {n}" for n in task.non_goals)
        parts.append(_section("Constraints and non-goals", body))

    # Prior failed attempts are cheap and stop an agent repeating them; they survive
    # a low context_volume, unlike the raw evidence corpus.
    parts.append(_section("What has already failed", task.attempts))

    if d.context_volume >= 0.6:
        parts.append(_section("Evidence", task.evidence))
        if not task.evidence.strip():
            gaps.append(
                "context_volume is high but no evidence supplied — either gather it "
                "or turn the dial down")
    elif task.evidence.strip():
        parts.append(_section("Evidence", task.evidence))
        if len(task.evidence) > BULKY_EVIDENCE_CHARS:
            gaps.append(
                f"evidence is {len(task.evidence)} chars but context_volume is "
                f"{d.context_volume:.2f} — compress it before sending")

    # --- the task itself -------------------------------------------------
    if d.autonomy >= 0.6:
        if task.open_decisions:
            parts.append(_section("Decisions you own", _bullets(task.open_decisions)))
        else:
            gaps.append(
                "autonomy is high but no open decisions were named — say what this "
                "agent is authorised to decide, or lower the dial")

    if d.decomposition >= 0.6:
        if task.subtasks:
            body = "\n".join(
                _render_subtask(st, d.acceptance_binding >= 0.6, d.verification_rigor)
                for st in task.subtasks)
            parts.append(_section("Subtasks (modular, individually testable)", body))
            if d.acceptance_binding >= 0.6:
                missing = [st.id for st in task.subtasks if not st.acceptance]
                if missing:
                    gaps.append(
                        "acceptance_binding is high but these subtasks carry no "
                        f"criteria: {', '.join(missing)}")
            untestable = [st.id for st in task.subtasks
                          if d.verification_rigor >= 0.6 and not st.verification]
            if untestable:
                gaps.append(
                    "verification_rigor is high but no verification method for: "
                    f"{', '.join(untestable)}")
        else:
            gaps.append(
                "decomposition is high but no subtasks supplied — this agent needs an "
                "engineering task list, not one outcome")
    else:
        verb = "Design an approach for" if d.specificity < 0.4 else "Do the following"
        body = task.instructions.strip() or f"{verb}: {task.objective.strip()}"
        parts.append(_section("Task", body))
        if d.specificity >= 0.6 and not task.instructions.strip():
            gaps.append(
                "specificity is high but no instructions supplied — this agent expects "
                "to be told what to do")

    if d.acceptance_binding < 0.6 or not task.subtasks:
        if task.acceptance:
            parts.append(_section("Acceptance criteria", _bullets(task.acceptance)))
        elif d.acceptance_binding >= 0.3:
            gaps.append("no acceptance criteria — there is no observable definition of done")

    if d.verification_rigor >= 0.6:
        if task.verification:
            parts.append(_section("Verification", task.verification))
        elif not task.subtasks:
            gaps.append(
                "verification_rigor is high but no verification method — name the "
                "command, test or visual check")

    if d.escalation_explicitness >= 0.6:
        if task.escalation_triggers:
            parts.append(_section("Escalate instead of proceeding when",
                                  _bullets(task.escalation_triggers)))
        else:
            gaps.append(
                "escalation_explicitness is high but no triggers named — say when to "
                "stop and hand back")

    contract = list(task.return_format) or list(profile.return_contract)
    if contract:
        parts.append(_section("Return", _bullets(contract)))

    text = "\n".join(p for p in parts if p).rstrip() + "\n"
    return text, gaps
