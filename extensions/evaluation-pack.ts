import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";

type EvalState = {
  enabled: boolean;
};

const STATE_ENTRY = "evaluation-pack-state";

function buildEvaluationInstructions(task?: string): string {
  const taskLine = task?.trim()
    ? `Complete this task: ${task.trim()}`
    : "Complete the user's requested task.";

  return `${taskLine}

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
- Do not claim success without showing the evidence used to verify it`;
}

function updateWidget(ctx: ExtensionContext, state: EvalState) {
  if (!ctx.hasUI) return;
  if (!state.enabled) {
    ctx.ui.setWidget("evaluation-pack", undefined);
    return;
  }
  ctx.ui.setWidget("evaluation-pack", [ctx.ui.theme.fg("accent", "Evaluation mode: ON")]);
}

async function loadState(ctx: ExtensionContext): Promise<EvalState> {
  const entries = ctx.sessionManager.getEntries();
  for (let i = entries.length - 1; i >= 0; i--) {
    const entry = entries[i] as { type: string; customType?: string; data?: EvalState };
    if (entry.type === "custom" && entry.customType === STATE_ENTRY && entry.data) {
      return entry.data;
    }
  }
  return { enabled: false };
}

export default function evaluationPackExtension(pi: ExtensionAPI): void {
  let state: EvalState = { enabled: false };

  function persist(next: EvalState, ctx?: ExtensionContext) {
    state = next;
    pi.appendEntry(STATE_ENTRY, next);
    if (ctx) updateWidget(ctx, next);
  }

  pi.on("session_start", async (_event, ctx) => {
    state = await loadState(ctx);
    updateWidget(ctx, state);
  });

  pi.on("before_agent_start", async (event, _ctx) => {
    if (!state.enabled) return;
    return {
      systemPrompt:
        event.systemPrompt +
        "\n\nEvaluation mode is enabled. For this task, you must finish with an evaluation pack. " +
        "Include changed files, commands run, verification evidence, success criteria, limitations, and present the pack as a single self-contained HTML page when possible.",
    };
  });

  pi.registerCommand("evaluation-mode", {
    description: "Toggle persistent evaluation-pack mode. Usage: /evaluation-mode on|off|toggle|status",
    handler: async (args, ctx) => {
      const action = args.trim().toLowerCase() || "status";

      if (action === "on") {
        persist({ enabled: true }, ctx);
        ctx.ui.notify("Evaluation mode enabled", "success");
        return;
      }

      if (action === "off") {
        persist({ enabled: false }, ctx);
        ctx.ui.notify("Evaluation mode disabled", "info");
        return;
      }

      if (action === "toggle") {
        persist({ enabled: !state.enabled }, ctx);
        ctx.ui.notify(`Evaluation mode ${state.enabled ? "enabled" : "disabled"}`, "info");
        return;
      }

      ctx.ui.notify(`Evaluation mode is ${state.enabled ? "ON" : "OFF"}`, "info");
    },
  });

  pi.registerCommand("evaluation-pack", {
    description: "Run a task with evaluation-pack instructions. Usage: /evaluation-pack <task>",
    handler: async (args, ctx) => {
      const task = args.trim();
      if (!task) {
        ctx.ui.notify("Usage: /evaluation-pack <task>", "warning");
        return;
      }
      pi.sendUserMessage(buildEvaluationInstructions(task));
    },
  });
}
