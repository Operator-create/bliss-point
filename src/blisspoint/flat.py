"""Arm F — the flat renderer.

The experimental control. It takes the same `Task` and emits **every field it has**, in one
fixed order, under generic headings, with no reference to who is receiving it.

Three properties make it a control rather than a strawman, and each has a test:

1. **It never reads a dial or a profile.** `flat(task)` takes no recipient at all, so it
   cannot vary by one.
2. **It drops nothing.** Where the compiler *selects* — low `context_volume` omits evidence,
   low `decomposition` collapses the subtask list — flat emits all of it. Arm F therefore
   carries a superset of arm C's information.
3. **It is not deliberately bad.** No filler, no wall of text, no missing structure. It is
   what a careful person produces without this library: gather every field, label it, send it.

Point 2 is the one that matters. If a shaped brief beats a flat one while carrying *less*
text, shaping did the work. If it does not, the field-gathering was the whole product and
`docs/eval-protocol.md` §9 applies.
"""

from __future__ import annotations

from .brief import Subtask, Task

#: Fixed order. Never varies, never reorders, never conditionally reorders.
SECTIONS = (
    ("objective", "Objective"),
    ("current_state", "Current state"),
    ("files", "Relevant files"),
    ("decisions", "Accepted decisions"),
    ("constraints", "Constraints"),
    ("non_goals", "Non-goals"),
    ("evidence", "Evidence"),
    ("attempts", "Previous attempts"),
    ("instructions", "Instructions"),
    ("subtasks", "Subtasks"),
    ("acceptance", "Acceptance criteria"),
    ("verification", "Verification"),
    ("open_decisions", "Open decisions"),
    ("escalation_triggers", "Escalate when"),
    ("return_format", "Return"),
)


def _has(value) -> bool:
    return bool(value.strip()) if isinstance(value, str) else bool(value)


def _render_subtask(st: Subtask) -> str:
    """Every subtask field, unconditionally -- the compiler binds these by dial, flat does not."""
    lines = [f"### {st.id} — {st.title}"]
    for label, value in (("Purpose", st.purpose), ("Scope", st.scope),
                         ("Instructions", st.instructions), ("Verification", st.verification),
                         ("Return", st.returns)):
        if _has(value):
            lines.append(f"{label}: {value}")
    if st.depends_on:
        lines.append(f"Depends on: {', '.join(st.depends_on)}")
    if st.acceptance:
        lines.append("Acceptance criteria:")
        lines.extend(f"- {a}" for a in st.acceptance)
    return "\n".join(lines)


def _body(name: str, value) -> str:
    if name == "subtasks":
        return "\n\n".join(_render_subtask(st) for st in value)
    if isinstance(value, str):
        return value.strip()
    return "\n".join(f"- {item}" for item in value)


def flat(task) -> str:
    """Render `task` with no recipient. Takes no profile, no phase, no stakes, no dials."""
    if isinstance(task, str):
        task = Task(objective=task)
    elif isinstance(task, dict):
        task = Task.from_dict(task)

    parts = ["# Task brief\n"]
    for name, heading in SECTIONS:
        value = getattr(task, name)
        if _has(value):
            parts.append(f"## {heading}\n{_body(name, value)}\n")
    return "\n".join(parts).rstrip() + "\n"


def marker(task, field: str) -> str | None:
    """A short string that appears in rendered output iff `field`'s content was emitted.

    Used to verify information parity between arms mechanically rather than by reading them.
    """
    value = getattr(task, field)
    if not _has(value):
        return None
    if field == "subtasks":
        return value[0].id
    if isinstance(value, str):
        return value.strip()[:24]
    return str(value[0])[:24]


def emitted(text: str, task) -> set:
    """Which of `task`'s populated fields actually made it into `text`."""
    out = set()
    for field, _ in SECTIONS:
        m = marker(task, field)
        if m and m in text:
            out.add(field)
    return out
