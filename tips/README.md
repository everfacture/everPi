# Tips

## Multi-machine setup

Pi auto-discovers extensions from `~/.pi/agent/extensions/` on every machine.
Install this package on each machine:

```bash
pi install git:github.com/everfacture/everpi
```

Then set required environment variables in your shell profile (`~/.zprofile`,
`~/.bashrc`, etc).

## VPS with Bailian

On a headless VPS, the bailian-coding-plan provider works without a browser.
The apiKey is loaded via shell command from `~/.zprofile`:

```bash
export DASHSCOPE_API_KEY="your-key"
```

Extensions that require interactive UI (`ctx.hasUI`) block or skip gracefully
in non-interactive mode.

## Permission system

everpi-yolo uses YOLO mode by default — most operations allowed, only
`rm -rf` and external directory access ask. Toggle YOLO off in
`everpi-yolo/config.json` for full confirmation mode.
