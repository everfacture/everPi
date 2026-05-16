# bailian-coding-plan

Registers a DashScope provider with Pi. Models available via `/model` after install.

## Models

| Model | Context | Output | Inputs | Notes |
|-------|---------|--------|--------|-------|
| qwen3.6-plus | 1,000,000 | 65,536 | text, image | Alibaba's flagship model |
| kimi-k2.5 | 256,000 | 32,768 | text, image | Moonshot AI |
| glm-5 | 202,752 | 16,384 | text | Zhipu AI |
| MiniMax-M2.5 | 196,608 | 32,768 | text | MiniMax |

All at zero cost via DashScope Coding Plan subscription.

Endpoint: `https://coding-intl.dashscope.aliyuncs.com/v1` (Alibaba Cloud international)

**Requires:** `DASHSCOPE_API_KEY` in your environment.
