# H5–H9 — The harness changes the agent, independently of the model

**Status: OPEN, Phase 0 not yet run.** Filed 2026-08-20 by the operator. Protocol pre-registered
in [docs/harness-bakeoff.md](../../docs/harness-bakeoff.md).

## The claims

| | claim |
|---|---|
| **H5** | Melchior is faster and a better coder on **DeepSeek Harness** than on Hermes |
| **H6** | Balthasar is a better researcher on **Playwright CLI** than on Hermes |
| **H7** | Casper uses fewer tokens and is sharper on **Prime agent** than on Hermes |
| **H8** | Melchior is better on **pi** |
| **H9** | Balthasar is better on **DeepSeek Harness** |

## Why they are testable only together

H5–H7 on their own are three unrelated A/Bs, and each would be equally well explained by "that
harness happens to suit that one role" or by "that harness is just better". H8 and H9 close the
grid: two roles across three harnesses, one harness across two roles. That is the difference
between a preference and an **interaction**.

- dsh wins for **both** Melchior and Balthasar → general harness effect, adopt it, role-independent.
- dsh wins for Melchior **only** → **role × harness interaction**.

The second result is [T1](../theory/T1-shape-as-a-function-of-recipient.md) one level up. This
project claims a brief must be shaped to its recipient; an interaction here would say the *runtime*
must be too — and unlike everything else in this lab, it would be evidence for that shape argument
measured on something we did not build.

## The confound that would make all five meaningless

**The harness and the model must not move together.** Hermes runs MiniMax-M3. Run dsh on a DeepSeek
model and "Melchior codes better on dsh" measures DeepSeek and credits dsh. Every one of the five
claims has this failure mode.

This is [R1](../refuted/R1-arm-M-as-falsifier.md) again in a new costume: comparing a thing against
a differently-shaped thing and reporting the difference as though one variable moved. It cost us an
entire eval arm the first time.

The control is the operator's own instruction — **all harnesses on MiniMax OAuth**. Recorded as
load-bearing, not as setup convenience. A harness that cannot be pointed at MiniMax has an
unfalsifiable claim attached to it, and gets reported as *not tested* rather than run with a
footnote.

## The second confound: a role is not a harness feature

"Melchior" is a Hermes profile — prompt, skills, tool allowlist. dsh has no Melchior. So H5 really
reads "the Melchior role, **reconstructed** on dsh", and a sloppy reconstruction loses for being
sloppy. Controls: byte-identical system prompt, capability-matched tools, every forced edit recorded
as a diff.

## What would kill each claim

Declared before Phase 0:

- **H5/H8 dead** if steps-to-green are within ±10% of Hermes, or pass rate is no better.
- **H6/H9 dead** if the verifiable-citation rate does not improve by 20 points. Note this can go
  *negative*: a browsing harness may raise fabrication rather than lower it, which would be the most
  useful finding available and directly extends [F1](../findings/F1-agent-reports-need-grepping.md).
- **H7 dead** if total tokens at equal success land within ±10%.

The null — every harness within noise of every other — is the single most likely outcome at n=3
tasks, and the pilot is explicitly **underpowered to confirm anything**. It can kill a claim, expose
a capability gap, or price a real run. Nothing else.

## What we want out of it regardless

A **seam report**: for each harness, what it does structurally that Hermes does not, and whether
that structure is portable into Bliss Point.
[C1](../confirmed/C1-dsh-plugin-seam-is-real.md) already established dsh's plugin seam can host a
prompt compiler without patching core. A claim can die and its harness still produce the most
valuable finding of the experiment.

Related: [[H2-recipients-want-different-shapes]], [[R1-arm-M-as-falsifier]], [[C1-dsh-plugin-seam-is-real]]
