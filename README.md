Here's the updated README:

---

# SecOps Agent — v1 → v2

> Single-agent toy that exposed every wrong assumption. v2 fixes them.

---

## v1 — What Broke (and Why)

The first version was embarrassingly simple by design — one agent, one LLM, a handful of hardcoded function calls. It found the failure points fast:

**LLM Guardrails killed speed.** Standard models hedge, refuse, and over-explain on anything security-adjacent. Legitimate tasks got caught in the same net as malicious ones. Useless in a real workflow.

**Zero environment awareness.** The agent operated completely blind — no knowledge of what was running, what was exposed, or what tools were even available on the host.

**Static vulnerability knowledge.** CVE lookups hit a flat JSON file updated by hand. By the time it mattered, the data was stale.

**One agent doing everything.** No separation of concerns. Scanning, summarizing, decision-making — all crammed into a single prompt loop with no specialization.

**Human approval blocked everything.** Sign-off was required too early and too often. Built for safety, killed for speed.

---

## v2 — What's Different

### Guardrails Removed — Heretic LLM Backbone
Standard models are replaced with **Heretic** — an uncensored LLM backbone that removes refusal behavior on security-sensitive prompts. Offensive tasks, exploit analysis, vulnerability chaining — no hedging, no Ethics 101 disclaimers. Human oversight is preserved for high-impact decisions, but the model itself doesn't flinch.

### Multi-Agent Architecture — Manager + Specialists

Three agents, clearly separated:

| Agent | Role |
|---|---|
| **Manager** | Goal setter and final decision maker. Breaks down objectives, assigns tasks, reviews outputs, decides what gets actioned. |
| **Shell Agent** | Executes commands, runs tools, interacts with the live environment. Hands-on, fast, scoped to what the manager authorizes. |
| **Scraper Agent** | Continuously pulls from NVD, ExploitDB, vendor advisories, and PoC repositories. Cross-verifies findings across sources before surfacing anything. |

Manager talks to both specialists. Specialists don't talk to each other. Clean hierarchy.

### Live System Awareness
The Shell Agent profiles the environment on startup — running services, exposed ports, available tools, installed packages. The Manager makes decisions with actual context, not assumptions.

### Human Authority — Where It Actually Matters
Humans are no longer asked to rubber-stamp every step. Approval is required only for two things:

- **Package installation** — nothing gets installed without explicit human sign-off
- **External connections** — any outbound call or new integration requires human authorization before it's established

Everything else runs autonomously. The loop doesn't halt; it surfaces decisions that genuinely require a human and keeps moving on everything else.

### Offensive + Defensive Capability
v2 can simulate attacker behavior — not just scan checklists. The Shell Agent operates in both modes depending on what the Manager assigns. Authorized environments only.

---

## Architecture

```
                        [ Human ]
                            |
              package installs & connection approvals
                            |
                      [ Manager Agent ]
                      goal setter · final decision maker
                       /                    \
          [ Shell Agent ]            [ Scraper Agent ]
          command execution          live CVE · ExploitDB
          env profiling              vendor advisories · PoCs
          tool invocation            cross-source verification
```

---

## Status

- [x] v1 — failure points documented
- [ ] v2 — in design

---
