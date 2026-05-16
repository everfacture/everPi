import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const zeroCost = { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 } as const;

export default function (pi: ExtensionAPI) {
  pi.registerProvider("bailian-coding-plan", {
    name: "Bailian Coding Plan",
    baseUrl: "https://coding-intl.dashscope.aliyuncs.com/v1",
    apiKey: "!zsh -lc 'source ~/.zprofile >/dev/null 2>&1; printf %s \"$DASHSCOPE_API_KEY\"'",
    api: "openai-completions",
    models: [
      {
        id: "qwen3.6-plus",
        name: "qwen3.6-plus",
        reasoning: false,
        input: ["text", "image"],
        contextWindow: 1_000_000,
        maxTokens: 65_536,
        cost: zeroCost,
        compat: { thinkingFormat: "qwen" },
      },
      {
        id: "kimi-k2.5",
        name: "kimi-k2.5",
        reasoning: false,
        input: ["text", "image"],
        contextWindow: 256_000,
        maxTokens: 32_768,
        cost: zeroCost,
        compat: { thinkingFormat: "qwen" },
      },
      {
        id: "glm-5",
        name: "glm-5",
        reasoning: false,
        input: ["text"],
        contextWindow: 202_752,
        maxTokens: 16_384,
        cost: zeroCost,
        compat: { thinkingFormat: "qwen" },
      },
      {
        id: "MiniMax-M2.5",
        name: "MiniMax-M2.5",
        reasoning: false,
        input: ["text"],
        contextWindow: 196_608,
        maxTokens: 32_768,
        cost: zeroCost,
      },
    ],
  });
}
