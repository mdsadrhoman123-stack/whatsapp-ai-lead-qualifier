<img src="assets/banner.svg" alt="WhatsApp Lead Qualifier — 24/7 inbound qualification" width="100%">

# WhatsApp Lead Qualifier

**Every inbound WhatsApp lead is answered immediately, qualified in conversation, and either handed to an agent with full context or put into a follow-up sequence.**

![production · v4.0](https://img.shields.io/badge/status-delivered%20to%20client-2F6B52?style=flat-square) ![sector](https://img.shields.io/badge/sector-Real%20estate-12151B?style=flat-square) ![built with](https://img.shields.io/badge/built%20with-n8n-12151B?style=flat-square) ![Production version](https://img.shields.io/badge/Production%20version-v4.0-5B6472?style=flat-square)

| | |
| :--- | :--- |
| **Built for** | Real estate brokers |
| **Industry** | Real estate |
| **Status** | production · v4.0 |
| **Role** | Designed, built and deployed end to end |

---

### On this page

[The problem](#the-problem) · [What changed](#what-changed) · [How it works](#how-it-works) · [When it breaks](#when-it-breaks) · [The stack](#the-stack) · [Limitations](#honest-limitations) · [Read deeper](#read-deeper)

---

## The problem

Inbound property enquiries arrive at every hour, and the first reply wins. A lead who messages at 11pm and hears nothing until morning has usually already messaged someone else.

Manual triage cannot cover the clock, and a broker reading back through a thread to work out what a lead wants is time the lead does not wait for.

## What changed

| | Before | After |
| :--- | :--- | :--- |
| **Reply time at 11pm** | Next morning | Immediate |
| **Qualification** | Broker reads the thread back | Done in conversation, summarised |
| **Handoff context** | “Someone asked about a flat” | Full conversation attached |
| **Viewing booking** | A second exchange to arrange it | Slot booked while the lead is hot |
| **Cold leads** | Forgotten | 3-day follow-up sequence |
| **A failed step** | Nobody notices | Error logged and alerted live |

<sub>Before/after describes the change in process, not benchmarked throughput. Where a number is not measured, it is not claimed.</sub>

## How it works

Every inbound message is signature-verified, deduplicated, and answered by an agent that holds session memory across the conversation. Hot leads fire an instant broker alert with the full conversation and an auto-booked calendar slot; the rest enter a follow-up sequence.

<table>
<tr>
<td width="42" valign="top" align="center"><b>01</b></td><td valign="top"><b>A lead messages</b><br>On WhatsApp, at any hour, with no form to fill in.</td>
</tr>
<tr>
<td width="42" valign="top" align="center"><b>02</b></td><td valign="top"><b>The request is verified</b><br>Signature-checked before anything runs, and deduplicated so one message means one conversation.</td>
</tr>
<tr>
<td width="42" valign="top" align="center"><b>03</b></td><td valign="top"><b>Someone answers immediately</b><br>The agent holds context across the whole conversation, so the lead is not repeating themselves.</td>
</tr>
<tr>
<td width="42" valign="top" align="center"><b>04</b></td><td valign="top"><b>The clock is respected</b><br>Inside hours a live agent takes over. Outside hours the lead is still qualified, not parked.</td>
</tr>
<tr>
<td width="42" valign="top" align="center"><b>05</b></td><td valign="top"><b>A hot lead reaches the broker</b><br>With the full conversation and a calendar slot already booked — not a notification to go and read something.</td>
</tr>
<tr>
<td width="42" valign="top" align="center"><b>06</b></td><td valign="top"><b>A cold lead is kept</b><br>A three-day follow-up sequence, because not-now is not the same as no.</td>
</tr>
<tr>
<td width="42" valign="top" align="center"><b>07</b></td><td valign="top"><b>A broken step is visible</b><br>Every critical path logs errors to a live alert channel. This is the part that keeps the zero honest.</td>
</tr>
</table>

### How it flows

<sub>What happens to the client's work, in the order they experience it. The internal build — node graph, execution order, prompts, thresholds — is deliberately not published.</sub>

```mermaid
flowchart LR
    in(["A lead messages, any hour"])
    qual["Answered and qualified in conversation"]
    hot{"Ready to move?"}
    hand["Yes → broker gets it, slot booked"]
    warm["Not yet → kept warm, not dropped"]
    err["A broken step is caught and alerted"]

    in --> qual
    qual --> hot
    hot --> hand
    hot --> warm
    qual -.-> err

    classDef default fill:#F8F7F3,stroke:#12151B,stroke-width:1px,color:#12151B;
    classDef ok fill:#2F6B52,stroke:#12151B,stroke-width:1px,color:#F5F4EF;
    classDef bad fill:#FEE2E2,stroke:#DC2626,stroke-width:1.5px,color:#7F1D1D;
    class hand ok;
    class err bad;
```

<details>
<summary><b>What the shapes mean</b> — colour is not the only signal</summary>

| Shape | Means |
| :--- | :--- |
| **rounded** | Where the client's process starts |
| **box** | Something the system does |
| **diamond** | A decision point |
| **slanted** | A person has to act |
| **green box** | The good outcome |
| **red box** | Failure path — held, escalated or alerted |

Red appears in exactly one role across every repo in this portfolio: where failure goes. Nowhere else. If you see red, something is being held, escalated or alerted.
</details>

> **Walk it interactively** — [open the demo](https://mdsadrhoman123-stack.github.io/whatsapp-ai-lead-qualifier/) and press **Break it** to watch the failure path light up. Source: [`docs/index.html`](docs/index.html)

## When it breaks

Most automation portfolios show you the happy path. The happy path is the easy half. This is the half that decides whether a system survives contact with a real business.

| What goes wrong | How it is detected | What the system does | Who finds out |
| :--- | :--- | :--- | :--- |
| **Unverified inbound request** | Meta webhook signature check | Rejected before any processing | Logged, no alert needed |
| **Same message delivered twice** | Redis deduplication | Second copy dropped — the lead is not answered twice | Nobody — by design |
| **Message arrives outside business hours** | Business-hours branch | Answered and qualified anyway, agent handoff deferred | Broker sees it in the morning with context |
| **AI provider call fails** | API error | Error logged, alert fired on the live channel — the lead is not silently dropped | Immediate alert |
| **Calendar booking fails** | API error | Broker still alerted with the conversation, booking flagged | Alert names the failed booking |
| **Lead goes quiet after qualifying** | No reply in the window | Enters the follow-up sequence rather than being closed | Nobody — handled |
| **Anything unanticipated** | Error handling on every critical path | Halt that path, keep the conversation state | Live alert channel |

The default on an unhandled condition is to **stop and tell someone** — never to continue on a guess. A silent success is the failure mode that costs the most, because nobody goes looking for it.

## The stack

| Component | Why this one |
| :--- | :--- |
| **n8n** | Orchestration, self-hosted |
| **WhatsApp Business API** | Where the leads already are |
| **Redis** | Deduplication, so one message is never processed twice |
| **Claude API** | Runs the qualifying conversation with session memory |
| **Google Calendar API** | Books the viewing slot at the moment the lead is hot |

### Counted, not estimated

| | |
| :--- | :--- |
| Production version | **v4.0** |
| Coverage | **24/7** |
| Missed leads | **0** |

<sub>These are counts from the built system — nodes, stages, versions, gates. No efficiency percentages are published here without a stated measurement method.</sub>

### Also worth knowing

- This is the repo that did not exist. The system has been in production since May 2026 and had no public record of it.

## Honest limitations

Every design decision costs something. These are the trade-offs in this build, stated by the person who made them.

- Qualification quality depends on the lead engaging in conversation. A one-word enquiry gets a thinner summary.
- Booking assumes a maintained calendar with real availability. A stale calendar books a slot nobody is free for.
- Single WhatsApp number per deployment. More numbers means more instances, not more configuration.

## What is not in this repo

- **Client data.** None, in any form. Not anonymised, not sampled.
- **Credentials and endpoints.** Never committed. See [`NOTICE.md`](NOTICE.md).
- **The workflow itself.** No exports, no node graph, no execution order, no prompts, no scoring thresholds, no integration wiring — not sanitised, not partial, not in a screenshot. That is the build, and the build belongs to the engagement that paid for it.

This repository documents *how the problem was thought about* — the failure paths, the trade-offs, the reasoning. That is what tells you whether to hire someone. A copy of the wiring would not.

This is a portfolio repository documenting delivered work. It is not a product you can clone and run against your own accounts.

## Read deeper

| | |
| :--- | :--- |
| [01 · The problem](docs/01-problem.md) | The situation before, in full |
| [02 · The client journey](docs/02-journey.md) | Step by step, from their side |
| [03 · Architecture](docs/03-architecture.md) | Diagrams and the reasoning |
| [04 · Failure handling](docs/04-failure-handling.md) | Every path, and where it lands |
| [05 · The stack](docs/05-stack.md) | What was chosen and what was rejected |
| [06 · Results](docs/06-results.md) | What is measured and what is not |
| [07 · Limitations](docs/07-limitations.md) | The trade-offs, in detail |

---

<img src="assets/cta.svg" alt="If a process depends on someone noticing when it breaks, that is the problem I work on." width="100%">

### Tell me what the process is

I will tell you honestly whether automating it is worth your money — including when the answer is no.

**K MD SAYAD RAHMAN** — AI Automation Engineer  
n8n · AI agents · production reliability  
[LinkedIn](https://www.linkedin.com/in/khandokarsayad) · [More systems](https://github.com/mdsadrhoman123-stack)

