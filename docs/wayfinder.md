# Wayfinder — the roadmap format

A roadmap that specifies everything up front is a roadmap that rots, because most of it describes
branches that get cut. Wayfinder keeps the map at the lowest resolution that still lets you move.

## Nodes are decisions, not tasks

The tree branches on **open questions**, not on work. A task list tells you what to do next; a
decision tree tells you *what you would be wrong about* if you did it. Every node carries:

- **the question** — phrased so it can be answered yes/no or by picking one option
- **status** — `OPEN` or `SETTLED (date, what settled it)`
- **what would settle it** — the specific evidence, not "more thought"
- **children** — tickets and sub-decisions gated behind it

A settled decision is never deleted. It stays as the record of why the branches below it exist,
which is what stops a project relitigating itself three months later.

## Fog levels

Every ticket carries exactly one:

| level | meaning | may I specify it in detail? |
|---|---|---|
| **CLEAR** | in scope now, fully specified, acceptance criteria written | yes |
| **DIM** | next up, shape known, details deliberately unwritten | one line only |
| **FOGGED** | known to exist, deliberately unspecified | name it and stop |

**The zoom rule:** a ticket may only be promoted to CLEAR once its parent decision is SETTLED.
Writing acceptance criteria for a ticket hanging off an open decision is how you end up defending
work that should have been deleted.

**The fog rule:** when you find yourself wanting to detail a FOGGED ticket, that is a signal to go
settle its parent decision instead. The urge to plan is usually an unanswered question in disguise.

## Zooming

Zooming in is an explicit act with a cost, so it is recorded:

```
FOGGED  --(parent decision settled)-->  DIM  --(pulled into scope)-->  CLEAR
```

Nothing skips a step. A ticket that goes straight from FOGGED to CLEAR was either not really
fogged, or is about to be built on an assumption nobody checked.

## Why this pairs with the dials

A CLEAR ticket has acceptance criteria, so it compiles into a high-`acceptance_binding` brief for an
executing agent. A FOGGED ticket has none, so it can only compile into a high-`autonomy`,
low-`specificity` brief for a researcher — which is correct, because the honest task at that node is
"find out", not "build". The fog level of a ticket effectively picks the shape of the brief that can
be written for it.
