---
description: Ask the agent to produce an evaluation pack for fast review
argument-hint: "<task>"
---
Complete this task: $@

Before you finish, prepare an evaluation pack that makes review fast and reliable.

Evaluation pack requirements:
- Summarize what changed and why
- List exact files changed
- List commands run and their outcomes
- State how I should evaluate success
- If this is UI or browser work, include screenshots and, if possible, a short demo recording
- If this is terminal rendering or animation work, include screenshots or an animated GIF when possible
- If this is behavior or bug-fix work, include a minimal reproduction and the verification steps
- Include known limitations or anything not fully verified
- Present the pack as a single self-contained HTML page when possible
- Save the HTML file locally (e.g., evaluation-pack.html) and serve it so the user can view it
- At the end of your response, provide the localhost URL (e.g., http://localhost:8000/evaluation-pack.html) so the user can open it directly
- Do not claim success without showing the evidence used to verify it
