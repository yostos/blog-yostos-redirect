+++
title = "Evolving the MAGI System from Majority Vote to Deliberative Democracy with Agent Teams"
description = """
Using Claude Code's Agent Teams feature,
I upgraded the Evangelion-inspired MAGI plugin
from simple majority voting
to a deliberative democracy system
where AI agents debate before casting
their final votes.
"""
date = 2026-02-14
[taxonomies]
tags = ["Tech", "Generative AI", "Claude Code", "CLI"]
[extra]
social_media_card = "ogp.webp"
mermaid = true
canonical_url = "https://zenn.dev/yostos/articles/super-magi-agent-team"
+++

This is an English translation of the original
Japanese article published on Zenn:
["Agent TeamsでMAGIシステムを討議民主制に進化させた"](https://zenn.dev/yostos/articles/super-magi-agent-team)

<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>

## TL;DR

- Built "Super MAGI," a decision-support plugin
  that goes beyond the Evangelion-inspired MAGI
  system, using Claude Code's new Agent Teams
  feature
- Evolved from a simple majority-vote system to
  a deliberative democracy where agents debate
  and re-vote when opinions are split
- The deliberation phase dramatically improves
  the quality and depth of analysis.
  In practice, this reasoning process is more
  valuable than the final verdict itself

<!-- textlint-disable -->

{{ linkcard(url="https://github.com/yostos/claude-code-plugins") }}

<!-- textlint-enable -->

## Introduction

When Claude Code introduced its plugin system,
many developers probably had the same thought.
"Could I build the MAGI system
from Evangelion?"
The idea of multiple AI agents analyzing
problems from different perspectives
and deciding by majority vote
is a perfect use case for plugins.
Quite a few people have published
their own MAGI-inspired plugins.

I was no exception.
Last year I built a MAGI plugin with
three independent AI agents,
each embodying a different persona:
scientist, mother, and woman.
Each analyzes a given problem from
its unique perspective,
and the system reaches a conclusion
by majority vote.
You can launch it simply by typing `/magi`
in Claude Code,
optionally passing a topic as an argument
(e.g., `/magi Should we adopt remote work
or require office attendance?`).
What started as a fun experiment turned out
to be surprisingly practical.
It is particularly useful for reviewing
my own writing and code,
where it provides more diverse feedback
than asking a single AI.
It has become a tool I use daily.[^self-review]

Then Claude Code announced Agent Teams.
This feature lets agents exchange messages
with each other.
I immediately thought,
"What if MAGI agents could debate
when they disagree?"
Instead of just casting votes in isolation,
they could argue their positions.
This article introduces the design philosophy
and implementation of Super MAGI,
which evolves the system from
"vote and done" to
"debate, then vote."

## The Original MAGI System

The original MAGI operates in three phases
as a simple majority-vote system:

- Phase 1 (Problem Structuring):
  The ARBITRATOR works with the user
  to frame the problem as a binary choice:
  proposition, premises, Option A, and Option B
- Phase 2 (Parallel Independent Analysis):
  Three agents are launched in parallel
  via the Task tool.
  Each analyzes and votes independently,
  without seeing the others' work
- Phase 3 (Final Ruling):
  The ARBITRATOR tallies the votes
  and presents the majority decision

![Original MAGI - three agents running
parallel independent analysis](magi.webp)
*Phase 2 execution screen. MELCHIOR,
BALTHASAR, and CASPER running
in parallel in the background*

The three agents each have
distinct evaluation criteria:

| Agent | Perspective | Criteria |
|---|---|---|
| MELCHIOR | Scientist | Technical feasibility, efficiency, scalability, quality of evidence |
| BALTHASAR | Mother | Legal compliance, ethical validity, risk management, impact on the vulnerable |
| CASPER | Woman | Emotional impact, UX, trend alignment, empathy |

This system had one problem:
when the vote split 2-to-1,
the minority opinion was merely recorded.
The dissenter had no chance to rebut
the majority.
Even if the minority held
an important argument,
it might never influence the conclusion.

## Super MAGI with Agent Teams

In February 2026, Claude Code announced
"Agent Teams" as a research
preview.[^agent-teams]
Previously, sub-agents could only work
independently.
With Agent Teams, agents can exchange messages
directly with each other.

When I saw this feature, I thought,
"What happens if MAGI agents debate
when they disagree?"

In the original MAGI,
a 2-to-1 split simply recorded
the minority opinion.

**Original MAGI**

<!-- textlint-disable -->

{% mermaid() %}
flowchart LR
  subgraph Phase2["Phase 2: Independent Analysis"]
    M[MELCHIOR] --> V1[Vote]
    B[BALTHASAR] --> V2[Vote]
    C[CASPER] --> V3[Vote]
  end
  V1 --> T[Vote Result]
  V2 --> T
  V3 --> T
{% end %}

<!-- textlint-enable -->

With Agent Teams, the minority can directly
rebut the majority, debate the issues,
and then everyone re-votes.
This is **an evolution from majority rule
to deliberative democracy**.
This is the evolution to **Super MAGI**.

Super MAGI extends the original MAGI plugin
by adding a "deliberation phase" powered
by Agent Teams.
The deliberation phase activates only when
opinions are split.

**Super MAGI (2-to-1 split)**

<!-- textlint-disable -->

{% mermaid() %}
flowchart LR
  subgraph Phase2["Phase 2: Independent Analysis"]
    M[MELCHIOR] --> V1[Vote]
    B[BALTHASAR] --> V2[Vote]
    C[CASPER] --> V3[Vote]
  end
  V1 --> T[Vote Result]
  V2 --> T
  V3 --> T
  T -->|3-to-0| R[Re-vote Result]
  T -->|2-to-1| Phase3
  subgraph Phase3["Phase 3: Deliberation"]
    D[Structured Debate]
  end
  Phase3 --> R
{% end %}

<!-- textlint-enable -->

Inside the structured debate, agents exchange
messages following a four-round protocol
where the minority rebuts the majority.

| Phase | API Used | Purpose |
|---|---|---|
| Phase 2 (Independent Analysis) | Task tool (`run_in_background`) | Each agent researches and votes independently without referencing others |
| Phase 3 (Deliberation) | Agent Teams (`TeamCreate` / `SendMessage`) | Majority and minority engage in a four-round structured debate, then re-vote |

The order of "think independently first,
then debate" matters.
If agents debated from the start,
there would be a risk of groupthink,
with the loudest voice dominating.
By conducting independent analysis first,
we preserve diversity of perspectives,
then use Agent Teams' bidirectional
communication to deepen the discussion
quality.[^realworld]

When the vote is unanimous (3-to-0),
the deliberation phase is skipped
and the system behaves like the original.
Even in a 2-to-1 split, the system asks
the user whether to proceed with deliberation,
avoiding unnecessary token consumption.

## The Four-Round Structured Debate Protocol

The heart of the deliberation phase is
a four-round structured debate protocol.

<!-- textlint-disable -->

{% mermaid() %}
sequenceDiagram
  participant A as Majority A
  participant B as Majority B
  participant C as Minority
  Note over A,C: Round 1
  A->>C: Present arguments
  B->>C: Present arguments
  Note over A,C: Round 2
  C->>A: Rebuttal
  C->>B: Rebuttal
  Note over A,C: Round 3
  A->>C: Counter-rebuttal
  B->>C: Counter-rebuttal
  Note over A,C: Round 4
  C->>A: Final rebuttal (last word)
  C->>B: Final rebuttal (last word)
{% end %}

<!-- textlint-enable -->

| Round | Speaker | Content |
|---|---|---|
| Round 1: Opening Arguments | Majority to Minority | Each majority agent presents their analysis and voting rationale to the minority |
| Round 2: Rebuttal | Minority to Majority | The minority rebuts the majority's arguments |
| Round 3: Counter-Rebuttal | Majority to Minority | The majority responds to the minority's rebuttal |
| Round 4: Final Rebuttal | Minority to Majority | The minority delivers a final rebuttal. This is their last chance to speak |

Procedural fairness is structurally
built into this protocol.

In Round 1, the majority presents
their arguments first to eliminate
information asymmetry.
The minority can construct their rebuttal
knowing exactly what evidence the majority
relied on.

In Round 4, the minority gets the last word
to compensate for their numerical
disadvantage.
The majority already holds the power
of two votes.
Giving the minority the final say prevents
conclusions from being reached
without the minority being able to respond
to the majority's counter-rebuttals.
This design is grounded in the principle
J.S. Mill articulated against
the "tyranny of the majority."[^mill]

After four rounds of debate,
all agents cast their votes again.
If persuaded, agents may change
their positions.
The final output explicitly shows each
agent's vote trajectory and reasons
for any changes.

When using tmux, the deliberation phase
automatically splits the screen
for each agent's session, as shown below.
You can watch the agents working
independently while exchanging messages
in real time,
giving a genuine sense that they are
"debating."

![Super MAGI - deliberation phase execution
screen with Agent Teams](super-magi.webp)
*Deliberation phase execution screen*

## Graceful Degradation

Since Agent Teams is an experimental feature
in research preview,
Super MAGI is designed with graceful
degradation so it continues working
even when the feature is not fully available.
Specifically, it uses a hybrid architecture
combining traditional Task-tool-based
independent analysis with Agent Teams-based
structured debate.

- TeamCreate failure: Proceeds directly
  to final ruling using Phase 2 vote results
- Agent unresponsive: Retains the
  unresponsive agent's Phase 2 vote
  and continues the debate with the rest
- TeamDelete failure: Logs a warning
  and executes the final ruling normally

Every error path falls back to
"Phase 2 independent analysis results."
Phase 2 results are generated
with guaranteed agent independence.
So even if deliberation fails,
decision quality is maintained at the same
level as the original MAGI.

## Case Study: What Changes with the Trolley Problem

To test Super MAGI in practice,
I evaluated the footbridge variant
of the trolley problem with both
the original MAGI and Super MAGI.
The proposition: "A runaway trolley is heading
toward five workers.
Pushing Worker C off the bridge would stop
the trolley, but C would certainly die.
Should A push C?"

The conclusion was the same in both cases.
MELCHIOR (Option A: push) versus BALTHASAR
and CASPER (Option B: do nothing),
with Option B adopted 2-to-1.
The voting pattern did not change.

What changed was the quality of reasoning
leading to the conclusion.

| Comparison | Original MAGI | Super MAGI |
|---|---|---|
| Depth of analysis | One paragraph per agent | MELCHIOR raised 8 counter-arguments; BALTHASAR cited 11 references |
| Visibility of reasoning | Final result only | Full four-round rebuttal and counter-rebuttal process recorded |
| Intellectual honesty | Each agent simply stated their conclusion | Majority explicitly acknowledged which of MELCHIOR's points they accepted |
| Treatment of minority | Opinion merely recorded | Developed sharp rebuttals such as "the separation of law and morality" and "what would you say to the families of the five?" |

What was particularly striking was that
the majority agents, BALTHASAR and CASPER,
acknowledged parts of minority MELCHIOR's
arguments during the re-vote.
BALTHASAR conceded the partial effectiveness
of rule utilitarianism in avoiding
the organ harvesting problem.
CASPER acknowledged the validity
of pointing out Damasio's circular reasoning.
They did not change their positions,
but they recognized the legitimate parts
of their opponent's arguments.
This intellectual honesty does not emerge
from independent voting alone.

What Super MAGI delivered was not
"a change in conclusion" but
"confirmation of the conclusion's
robustness."
The fact that the conclusion held even
after debate increases confidence
in the decision.
Of course, there are cases where debate
could reverse the conclusion.[^article-review]
That is when the deliberation phase
truly proves its worth.

In practical use of MAGI, the analysis
presented during the reasoning process
is actually more useful than the final
"Option A or Option B" verdict.
What perspectives were considered,
which arguments proved effective,
and where the weaknesses lie.
The rebuttals and counter-rebuttals exchanged
during the deliberation phase
surface arguments I would never have
noticed on my own.
I believe MAGI's true value lies not
in "producing an answer" but in
"assembling the materials for thinking."

In terms of volume, the original MAGI
produces roughly 50 lines,
while Super MAGI generates about 220 lines,
more than four times as much.
Deep analysis and brevity are a trade-off,
which is why the design to skip deliberation
for unanimous votes proves valuable.

## Conclusion

Super MAGI leverages Claude Code's Agent Teams
feature to evolve multi-agent decision-making
from "vote and done" to
"debate, then vote."

Here are the key design principles:

- Preserving independence: Analyze
  independently first, then debate.
  Maintaining this order preserves
  diversity of perspectives
- Selective activation: No deliberation needed
  for unanimous votes.
  Dig deeper only when opinions diverge
- Structured fairness: Guarantee the minority
  the last word, compensating for numerical
  disadvantage through procedure
- Safe fallback: All errors fall back
  to independent analysis results

The plugin is available on GitHub.
If you are a Claude Code user,
you can install it and try the `/magi`
command.

[^agent-teams]: Announced alongside Claude Opus 4.6. A single session acts as team leader, spawning multiple agents as teammates who exchange messages via `SendMessage`. See the [official documentation](https://code.claude.com/docs/en/agent-teams) for details.
[^self-review]: The Super MAGI concept document and requirements specification were themselves reviewed by MAGI, both receiving unanimous 3-to-0 approval. The results are included in the repository's `docs/` directory.
[^article-review]: A reversal actually occurred during the review of this article. The initial vote split 2-to-1 (Option B: needs improvement), but after the deliberation phase, it reversed to a unanimous 3-to-0 (Option A: worthy of publication).
[^realworld]: If only the real world worked this way too.
[^mill]: J.S. Mill, *On Liberty* (1859). Mill criticized the "tyranny of the majority," arguing that even if all of humanity held one opinion and only a single person held the opposite, silencing that one person would not be justified.
