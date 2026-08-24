# 05 · The stack

Each choice, and the reason for it.

---

| Component | Why this one |
| :--- | :--- |
| **n8n** | Orchestration, self-hosted |
| **WhatsApp Business API** | Where the leads already are |
| **Redis** | Deduplication, so one message is never processed twice |
| **Claude API** | Runs the qualifying conversation with session memory |
| **Google Calendar API** | Books the viewing slot at the moment the lead is hot |

## What was deliberately not used

- **A hosted automation SaaS.** Client data would transit a third party, and the failure handling would be limited to what that vendor exposes.
- **A bespoke application where automation was enough.** The cheapest system to maintain is the one with the least custom code in it.
- **Anything that could not be redeployed by someone else.** A system only one person can operate is a liability for the client.

---

[← 04 · Failure handling](04-failure-handling.md) · [06 · Results →](06-results.md)
