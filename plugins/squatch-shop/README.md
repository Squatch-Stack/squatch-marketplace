# Squatch Stack shop plugin

Connects Claude Code or Codex to the Squatch Stack server at `https://mcp.squatch.cc/mcp` and adds one short skill. With
it you can ask for a gift idea, browse the goods, and get a checkout link.

## Install

In Claude Code:

```
/plugin marketplace add squatch-stack/squatch-marketplace
/plugin install squatch-shop@squatch-stack
```

## What it does

- Shows the shop and individual products, and builds checkout links.
- Leaves a request with the studio (custom pieces, order help) only after you confirm the text and whether to include
  your email.
- Searches the studio's essays, lists the ways to support the studio, and answers questions about who runs the server
  and what each tool does.

## What it does not do

- It never pays for you. The Buy link opens store.squatch.cc in your browser, and you pay there.
- It never asks for payment details.
- It has no sign-in and installs no local code: no scripts, hooks or commands.

Privacy: https://mcp.squatch.cc/privacy

MIT licensed. Run by Squatch.cc LLC.
