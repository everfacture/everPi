# everpi

DashScope Coding Plan provider for Pi. Four zero-cost models from Alibaba's Bailian platform, registered as a drop-in `/model` option.

## Install

```bash
pi install git:github.com/everfacture/everpi
npm install
/reload
```

## Models

All four are free under the [DashScope Coding Plan](https://bailian.console.aliyun.com/):

| Model | Context | Output | Inputs |
|-------|---------|--------|--------|
| qwen3.6-plus | 1M | 64K | text, image |
| kimi-k2.5 | 256K | 32K | text, image |
| glm-5 | 203K | 16K | text |
| MiniMax-M2.5 | 197K | 32K | text |

Endpoint: `coding-intl.dashscope.aliyuncs.com` (Alibaba Cloud, international route)

## Setup

```bash
export DASHSCOPE_API_KEY="your-key"
```

Add to `~/.zprofile` so Pi picks it up on every session.
