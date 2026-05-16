---
description: Analyze a previous agent session for wasted motion and repo friction
argument-hint: "[session/context]"
---
Analyze the previous Pi session${ARGUMENTS:+: $@}.

Focus on:
- places where the agent went in the wrong direction before later finding the right path
- repeated searches, file reads, or tool calls that suggest missing affordances
- documentation gaps, wrong commands, stale instructions, or naming confusion
- warnings, noisy output, or broken workflows that likely distracted the agent
- context bloat or dead-end side quests that should have been branched away sooner

Output:
1. Session summary
2. Friction points
3. Root cause for each friction point
4. What could be added or changed in the repo to prevent it next time
5. Highest-priority fixes first

Present the result as a single self-contained HTML slide deck.
