/**
 * Protected Sensitive Files
 *
 * Keep normal YOLO flow, but require confirmation for edits/writes to:
 * - .env files
 * - .gitignore
 *
 * Also require confirmation for destructive delete bash commands.
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const DELETE_PATTERNS = [
  /\brm\s+(-rf?|--recursive)\b/i,
  /\bfind\b.*\b-delete\b/i,
];

function isProtectedPath(path: string): boolean {
  const normalized = path.replace(/\\/g, "/");
  const base = normalized.split("/").pop() ?? normalized;

  return (
    base === ".gitignore" ||
    base === ".env" ||
    base.startsWith(".env.")
  );
}

export default function (pi: ExtensionAPI) {
  pi.on("tool_call", async (event, ctx) => {
    if (event.toolName === "bash") {
      const command = String(event.input.command ?? "");
      const needsConfirm = DELETE_PATTERNS.some((p) => p.test(command));
      if (!needsConfirm) return undefined;

      if (!ctx.hasUI) {
        return { block: true, reason: `Delete command blocked (no UI): ${command}` };
      }

      const ok = await ctx.ui.confirm(
        "Confirm delete",
        `Allow destructive delete command?\n\n${command}`,
      );
      if (!ok) return { block: true, reason: "Blocked delete command" };
      return undefined;
    }

    if (event.toolName === "write" || event.toolName === "edit") {
      const path = String(event.input.path ?? "");
      if (!isProtectedPath(path)) return undefined;

      if (!ctx.hasUI) {
        return { block: true, reason: `Protected file blocked (no UI): ${path}` };
      }

      const ok = await ctx.ui.confirm(
        "Confirm sensitive file change",
        `Allow ${event.toolName} on ${path}?`,
      );
      if (!ok) return { block: true, reason: `Blocked sensitive file change: ${path}` };
    }

    return undefined;
  });
}
