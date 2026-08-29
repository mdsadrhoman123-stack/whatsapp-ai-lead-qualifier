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

## The decisions behind that table

### Why every message is signature-verified and deduplicated first

**What it does.** The signature is checked, then the message is deduplicated in Redis, before anything else happens to it.

**What was turned down.** Trusting the webhook. One less step in the hot path — and a retried delivery then answers the same lead a second time, which is the most obviously automated thing a system can do to a human being.

**What that costs.** Redis sits in the critical path of every single inbound message.

### Why the viewing is booked inside the conversation

**What it does.** A qualifying lead gets a calendar slot at the moment they are interested, with the broker alerted and the full conversation attached.

**What was turned down.** Handing the lead to a broker to call back. More human judgement applied — and the interest has cooled by the time the call happens, which is the entire problem the brief described.

**What that costs.** It assumes a maintained calendar with real availability. A stale calendar books a slot nobody is free for, and the system cannot tell.

### Why the agent holds session memory

**What it does.** The conversation keeps state, so a lead is never asked the same question twice.

**What was turned down.** Stateless replies. Trivially scalable and much simpler to reason about — and it reads like a form, which is what the lead was avoiding by messaging.

**What that costs.** State per conversation, and one number per deployment. Qualification quality still depends on the lead engaging: a one-word enquiry produces a thin summary, and the system says so rather than padding it.

## The rule that applies to all of them

**Nothing that only one person can operate.** A system that depends on the engineer who built it is a liability for the client, however well it runs on the day it is handed over. Every choice above had to survive that test before the technical merits mattered at all.

---

[← 04 · Failure handling](04-failure-handling.md) · [06 · Results →](06-results.md)
