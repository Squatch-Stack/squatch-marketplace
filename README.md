# Squatch Stack marketplace

Plugins for Claude Code and Codex from [Squatch Stack](https://squatch.cc/). This first release lists two plugins. Both
connect your assistant to a server that we run, and neither installs any code that runs on your machine.

| Plugin | What it is | Server |
|---|---|---|
| `squatch-shop` | Browse the Squatch Stack shop, find a gift, and get a checkout link. | `https://mcp.squatch.cc/mcp` |
| `petnecto` | Find adoptable shelter pets with [Petnecto](https://petnecto.com/) and get the shelter's contact details. | `https://petnecto.com/mcp` |

`petnecto` is not copied here. It is listed from its own public repository,
[squatch-stack/petnecto-claude-plugin](https://github.com/squatch-stack/petnecto-claude-plugin), pinned to one reviewed
commit.

## Install in Claude Code

```
/plugin marketplace add squatch-stack/squatch-marketplace
/plugin install squatch-shop@squatch-stack
/plugin install petnecto@squatch-stack
```

Then ask, for example: "Show me the Squatch Stack shop", "Help me find a gift in the Squatch Stack shop", or "Find
adoptable dogs near me with Petnecto".

## Install in Codex

```
codex plugin marketplace add squatch-stack/squatch-marketplace
codex plugin add squatch-shop@squatch-stack
codex plugin add petnecto@squatch-stack
```

## What the plugins can and cannot do

- They have no local code: no scripts, hooks or commands. Each plugin is a link to a server we run, plus a short written
  skill that tells the assistant how to use it well.
- Everything is read-only, with one exception. With `squatch-shop`, the assistant can leave a request with the studio
  (a custom piece, or help with an order). It does that only after you confirm the text and whether to include your
  email address.
- `squatch-shop` never pays for you and never asks for payment details. Its Buy link opens the store in your browser, and
  you pay there.
- `petnecto` cannot reserve or adopt a pet. Adoption always goes through the shelter.

## Privacy

- Squatch Stack shop server: https://mcp.squatch.cc/privacy
- Petnecto: https://petnecto.com/privacy

To report a security problem, see [SECURITY.md](SECURITY.md).

## License

MIT. Run by Squatch.cc LLC.
