"""Assert the manifests say what the README promises.

Usage: python3 -I tools/check-manifests.py [ROOT]   (ROOT defaults to the current directory)
Exit 0 when every assertion holds, 1 otherwise.
"""
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
SHOP = "plugins/squatch-shop"
PIN_RE = re.compile(r"[0-9a-f]{40}")
errors = []


def load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return json.load(f)


def check(cond, msg):
    if not cond:
        errors.append(msg)


def files_under(top):
    out = set()
    for d, _, names in os.walk(os.path.join(ROOT, top)):
        for n in names:
            out.add(os.path.relpath(os.path.join(d, n), ROOT).replace(os.sep, "/"))
    return out


# 1. Exact file allowlist: the plugin ships no code, hooks, commands or agents.
want_files = {f"{SHOP}/{p}" for p in (
    ".claude-plugin/plugin.json", ".claude-plugin/icon.png", ".codex-plugin/plugin.json", ".mcp.json", "README.md",
    "skills/squatch-shop/SKILL.md")}
got_files = files_under("plugins")
check(got_files == want_files,
      f"files under plugins/ differ: extra={sorted(got_files - want_files)} missing={sorted(want_files - got_files)}")

# 1b. The directory listing icon: a real square PNG, 512-2048 px (the directory takes it once, at first submission).
icon = os.path.join(ROOT, SHOP, ".claude-plugin/icon.png")
if os.path.exists(icon):
    head = open(icon, "rb").read(24)
    w, h = int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")
    check(head[:8] == b"\x89PNG\r\n\x1a\n" and w == h and 512 <= w <= 2048, f"icon.png must be a square PNG of 512-2048 px, got {w}x{h}")

# 2. Claude marketplace.
mkt = load(".claude-plugin/marketplace.json")
check(mkt.get("name") == "squatch-stack", f"marketplace name is {mkt.get('name')!r}, want 'squatch-stack'")
plugins = {p["name"]: p for p in mkt.get("plugins", [])}
check(set(plugins) == {"squatch-shop", "petnecto"}, f"claude plugins are {sorted(plugins)}")
check(plugins.get("squatch-shop", {}).get("source") == f"./{SHOP}",
      f"claude squatch-shop source is {plugins.get('squatch-shop', {}).get('source')!r}")
pet = plugins.get("petnecto", {}).get("source")
check(
    isinstance(pet, dict)
    and set(pet) == {"source", "repo", "sha"}
    and pet.get("source") == "github"
    and pet.get("repo") == "squatch-stack/petnecto-claude-plugin"
    and PIN_RE.fullmatch(str(pet.get("sha", ""))) is not None,
    f"claude petnecto source must be exactly the github repo pinned to a 40-hex sha, got {pet!r}",
)

# 3. The shop's MCP config.
servers = load(f"{SHOP}/.mcp.json").get("mcpServers", {})
check(list(servers) == ["squatch-stack"], f"squatch-shop servers are {list(servers)}")
srv = servers.get("squatch-stack", {})
check(srv.get("url") == "https://mcp.squatch.cc/mcp", f"squatch-shop MCP url is {srv.get('url')!r}")
check(set(srv) <= {"type", "url"}, f"squatch-shop server has extra keys: {sorted(srv)}")

# 4. Codex marketplace agrees with the Claude one.
cdx = load(".agents/plugins/marketplace.json")
check(cdx.get("name") == "squatch-stack", f"codex marketplace name is {cdx.get('name')!r}")
cplugins = {p["name"]: p for p in cdx.get("plugins", [])}
check(set(cplugins) == set(plugins), f"codex plugins {sorted(cplugins)} differ from claude {sorted(plugins)}")
check(cplugins.get("squatch-shop", {}).get("source") == {"source": "local", "path": f"./{SHOP}"},
      f"codex squatch-shop source is {cplugins.get('squatch-shop', {}).get('source')!r}")
cpet = cplugins.get("petnecto", {}).get("source")
check(
    isinstance(cpet, dict)
    and set(cpet) == {"source", "url", "sha"}
    and cpet.get("source") == "url"
    and cpet.get("url") == "https://github.com/squatch-stack/petnecto-claude-plugin.git"
    and PIN_RE.fullmatch(str(cpet.get("sha", ""))) is not None
    and isinstance(pet, dict) and cpet.get("sha") == pet.get("sha"),
    f"codex petnecto source must be exactly {{source,url,sha}} with the fixed url and the claude pin, got {cpet!r}",
)

# 5. Plugin manifests: key allowlists, no hooks or apps, fixed skills and MCP paths.
base_keys = {"name", "version", "description", "author", "homepage", "repository", "license", "keywords"}
claude_pj = load(f"{SHOP}/.claude-plugin/plugin.json")
check(set(claude_pj) <= base_keys | {"privacyPolicyUrl"}, f"claude plugin.json has extra keys: {sorted(set(claude_pj) - base_keys - {'privacyPolicyUrl'})}")
check(claude_pj.get("privacyPolicyUrl") == "https://mcp.squatch.cc/privacy", f"claude privacyPolicyUrl is {claude_pj.get('privacyPolicyUrl')!r}")
codex_pj = load(f"{SHOP}/.codex-plugin/plugin.json")
check(set(codex_pj) <= base_keys | {"skills", "mcpServers"},
      f"codex plugin.json has extra keys: {sorted(set(codex_pj) - base_keys - {'skills', 'mcpServers'})}")
check(codex_pj.get("skills") == "./skills/", f"codex skills is {codex_pj.get('skills')!r}")
check(codex_pj.get("mcpServers") == "./.mcp.json", f"codex mcpServers is {codex_pj.get('mcpServers')!r}")
for k in ("hooks", "apps"):
    check(k not in codex_pj and k not in claude_pj, f"plugin.json declares {k}")

if errors:
    print("\n".join(f"FAIL: {e}" for e in errors))
    sys.exit(1)
print("manifests ok")
