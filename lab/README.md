# The lab

The code in this repository makes claims. This folder is the record of testing them, including the
claims that did not survive.

It is a real working notebook, not a retrospective write-up: entries are dated, mistakes stay in,
and `refuted/` is never cleaned out.

```
hypothesis/   a falsifiable statement, one per file, with a stated killer
    |
    v         experiment run, logged in logbooks/
logbooks/     dated, append-only, written as it happens - not tidied afterwards
    |
    +-----> confirmed/   survived a test that could have killed it
    +-----> refuted/     did not, and what killed it
    |
findings/     results worth citing, whichever direction they went
theory/       the current model of why any of this works, revised by findings
```

## Rules

1. **A hypothesis without a stated killer is an opinion.** Every file in `hypothesis/` names the
   observation that would end it.
2. **`refuted/` is the valuable folder.** A project that never fills it is not testing anything.
   Nothing is deleted from it when it becomes embarrassing.
3. **Logbooks are written in the moment**, including the mistakes and the dead ends. A logbook
   edited to look competent afterwards is worthless as evidence.
4. **Confirmed is provisional.** Moving a file to `confirmed/` records that it survived one test at
   one sample size, not that it is true.
5. **The date and the source go in every file.** A claim you cannot re-derive is a rumour.
