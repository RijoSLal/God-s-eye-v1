# SecOps Agent — Failure Point Analysis Project

> **Purpose:** This is a research/experimental project built to stress-test current AI-driven SecOps pipelines, identify their failure points, and document limitations before designing a more capable v2 system.

---

## What This Project Does

Simulates an AI-assisted security operations workflow where agents are given access to function calls that retrieve commands (from a database or external file sources) and execute them within defined boundaries. The goal is not to build a production system — it's to **find where things break** using a toy system.

---

## Observed Failure Points (v1)

### LLM Guardrails & Ethics Hesitation
Standard LLMs refuse or heavily hedge on security-relevant tasks — even legitimate ones. This creates friction in real SecOps workflows where speed and directness matter.

### No Real-Time System Knowledge
Agents have no awareness of the live environment they're operating in — no current network state, no running services, no asset inventory. Decisions are made blind.

### MCP Client Setup Limitations
Not all platforms support external MCP tools, and most sit behind paid tiers

### Human Intervention Bottlenecks
The current design requires human sign-off at too many points, which defeats the purpose of autonomous response — but removing it entirely introduces unacceptable risk.

### Bounded Command Execution
Agents can only run what's pre-approved in the function/command database. Novel attack surfaces or unexpected scenarios fall outside these boundaries with no graceful fallback.

---

## v2 — Planned Improvements

| Area | v1 | v2 |
|---|---|---|
| LLM | Censored, guardrailed | Uncensored LLM to reduce hesitation on offensive tasks |
| Platform Integration | MCP-dependent | MCP removed — direct integrations only |
| Human Intervention | Blocking | Advisory — human-in-the-loop without halting execution |
| Attack Capability | Defensive only | Capable of controlled offensive operations |
| Vulnerability Knowledge | Static DB | Sophisticated scraper to pull live CVEs, exploit disclosures, PoCs |
| Cross-Verification | None | Scraped vuln data cross-verified against multiple sources |
| System Awareness | None | Live system knowledge and capability profiling |

---

## v2 Design Principles

- **Uncensored LLM backbone** — reduces refusals on security-sensitive prompts while keeping human oversight for high-impact actions
- **Offensive + Defensive capability** — the system can simulate attacker behavior to find real exposure, not just scan checklists
- **Live vuln scraper** — pulls from NVD, ExploitDB, vendor advisories, and other sources; cross-verifies before acting on findings
- **System context awareness** — agent knows what it's running on, what's exposed, and what tools are available
- **No MCP dependency** — direct API and CLI integrations for reliability and cost control

---

## Disclaimer

This is a toy project. Offensive capabilities are to be used exclusively in authorized environments. Nothing here is intended for use against systems without explicit permission.

---

## Status

- [x] v1 — Failure point identification complete
- [ ] v2 — In design
