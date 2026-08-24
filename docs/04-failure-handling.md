# 04 · Failure handling

The part of the system that took the longest to build and gets written about the least.

---

| What goes wrong | How it is detected | What the system does | Who finds out |
| :--- | :--- | :--- | :--- |
| **Unverified inbound request** | Meta webhook signature check | Rejected before any processing | Logged, no alert needed |
| **Same message delivered twice** | Redis deduplication | Second copy dropped — the lead is not answered twice | Nobody — by design |
| **Message arrives outside business hours** | Business-hours branch | Answered and qualified anyway, agent handoff deferred | Broker sees it in the morning with context |
| **AI provider call fails** | API error | Error logged, alert fired on the live channel — the lead is not silently dropped | Immediate alert |
| **Calendar booking fails** | API error | Broker still alerted with the conversation, booking flagged | Alert names the failed booking |
| **Lead goes quiet after qualifying** | No reply in the window | Enters the follow-up sequence rather than being closed | Nobody — handled |
| **Anything unanticipated** | Error handling on every critical path | Halt that path, keep the conversation state | Live alert channel |

## The three rules behind that table

**1 — Fail closed, not open.** When the system cannot establish that an action is safe, it holds. A held item is a visible problem. An item processed on a guess is an invisible one.

**2 — Nothing disappears.** Anything that cannot be completed is recorded where a human can find it later, not dropped from the run.

**3 — Silence is a fault.** An empty result where results were expected is treated as a possible failure of the source, not as an absence of work. This is the check most automations skip.

---

[← 03 · Architecture](03-architecture.md) · [05 · The stack →](05-stack.md)
