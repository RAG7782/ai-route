# AI Route — Go-to-Market Plan

## Positioning

**Tagline:** "The missing router for your AI coding agents."
**One-liner:** Stop choosing between Claude, Aider, Gemini, Codex, and Copilot. Just describe your task — ai-route picks the right tool.

**Category:** Developer Tools > AI Agent Orchestration
**Competitors:** RouteLLM (API router), ClawRouter (API router), OpenRouter Auto
**Differentiator:** First router for CLI agents (not just API models)

---

## Phase 0 — Product Polish (Week 1)

### Must-have before launch:
- [ ] GIF demo (asciinema) showing 5 queries being routed differently
- [ ] `pip install ai-route` working (PyPI publish)
- [ ] `brew install` via tap (optional but nice)
- [ ] Config via YAML (users can add their own agents)
- [ ] 3-5 unit tests passing
- [ ] README with clear install + usage in < 60 seconds
- [ ] LICENSE file (MIT)

### GIF script (record with asciinema):
```bash
# Query 1: shell → copilot
ai-route --dry "how to kill process on port 8080"

# Query 2: architecture → claude  
ai-route --dry "redesign the auth system to use OAuth2 with PKCE"

# Query 3: quick fix → aider-groq
ai-route --dry "fix the typo in config.py line 42"

# Query 4: explanation → gemini
ai-route --dry "explain how this codebase handles authentication"

# Query 5: offline → ollama
ai-route --dry "analyze this sensitive code without internet"
```

---

## Phase 1 — Seed Audience (Weeks 2-3)

### LinkedIn Post (carousel PDF — 596% more engagement)

**Slide 1 (hook):**
> I have 8 AI coding agents installed.
> Every time I need help, I waste 30 seconds choosing which one to use.
> So I built a router.

**Slide 2 (problem):**
> The AI Tool Fatigue is real.
> 85% of devs use AI tools in 2026.
> Product Hunt lists 30+ new AI tools per day.
> The consensus is "pick one and stop looking."
> But what if you already have 5+ installed?

**Slide 3 (solution):**
> ai-route analyzes your task and picks the best CLI agent:
> "fix bug in parser.py" → Aider-Groq (fast, free)
> "redesign the auth system" → Claude (deep reasoning)
> "how to kill port 8080" → Copilot (instant)
> "explain this code" → Gemini (free, large context)

**Slide 4 (how it works):**
> Regex scoring across 15+ dimensions:
> - Shell keywords → Copilot
> - Architecture terms → Claude
> - File references → Aider
> - Privacy/offline → Ollama
> Zero config. Zero dependencies. One Python file.

**Slide 5 (results):**
> Before ai-route: 
>   Think → Choose tool → Open → Type
>   ~45 seconds of decision overhead
> 
> After ai-route:
>   ai-route "your task" → Done
>   ~2 seconds

**Slide 6 (CTA):**
> Open source. MIT license.
> github.com/RAG7782/ai-route
> pip install ai-route
> 
> Star if this solves your problem too.

### Twitter/X Thread

```
Thread: I have 8 AI coding agents. Here's how I stopped wasting time choosing.

1/ The problem nobody talks about: AI Tool Fatigue.
   85% of devs use AI tools. Most have 3-5 installed.
   Every task = "should I use Claude? Aider? Copilot? Gemini?"

2/ I mapped my actual usage over 2 weeks:
   - 40% = quick fixes (Aider-Groq handles these)
   - 25% = shell commands (Copilot, instant)
   - 20% = architecture (Claude, worth the cost)
   - 10% = explanations (Gemini, free)
   - 5% = offline/private (Ollama)

3/ The insight: 65% of my tasks don't need Claude.
   I was paying $$$ for tasks that free tools handle better.

4/ So I built ai-route: describe your task, it picks the tool.
   Regex scoring. 200 lines of Python. Zero dependencies.
   
   ai-route "fix bug in parser.py" → aider-groq
   ai-route "redesign auth system" → claude
   ai-route "kill port 8080" → copilot

5/ Open source: github.com/RAG7782/ai-route
   Star it. Fork it. Add your own agents.
   
   The future isn't one AI tool. It's the right tool at the right time.
```

### Hacker News (Show HN)

```
Title: Show HN: AI Route – A router for CLI coding agents (Claude, Aider, Gemini, etc.)

I have 8 AI coding CLI tools installed. Every time I needed help, 
I'd waste 30 seconds deciding which one to use.

ai-route solves this: describe your task in natural language, 
it scores against 15+ regex patterns and routes to the best agent.

- "fix bug in parser.py" → Aider-Groq (554 t/s, free)
- "redesign the auth system" → Claude Code (deep reasoning)  
- "how to kill port 8080" → GitHub Copilot (instant)
- "explain this codebase" → Gemini CLI (free, large context)
- "analyze this sensitive code" → Ollama (offline, private)

200 lines of Python. Zero dependencies. MIT license.

There are routers for LLM APIs (RouteLLM, ClawRouter, OpenRouter), 
but none for CLI agents. This is the first.

github.com/RAG7782/ai-route
```

---

## Phase 2 — Product Hunt Launch (Week 4)

### Timing
- Launch on Tuesday or Wednesday (best engagement days)
- Post at 00:01 PST (start of PH day)
- Have 20-30 people ready to upvote in the first 2 hours

### Listing

**Name:** AI Route
**Tagline:** The missing router for your AI coding agents
**Description (800 chars max):**

> Stop choosing between Claude, Aider, Gemini, Codex, and Copilot every time you need help. 
> ai-route analyzes your task and automatically picks the best CLI agent.
> 
> Shell commands? → Copilot (instant, free)
> Quick code fix? → Aider-Groq (554 t/s, free)  
> Architecture? → Claude Code (deep reasoning)
> Explanation? → Gemini (large context, free)
> Offline? → Ollama (private, zero cost)
> 
> 200 lines of Python. Zero dependencies. Zero config. MIT license.
> The first router for CLI agents (not just API models).

**Gallery:** 5 screenshots/GIFs showing different routing decisions
**Topics:** Developer Tools, AI, Command Line, Open Source
**Maker's first comment:** Personal story about AI Tool Fatigue

---

## Phase 3 — Growth & Monetization (Months 2-6)

### Content Calendar (weekly)

| Week | Platform | Content |
|------|----------|---------|
| 1 | LinkedIn | Carousel: "8 AI tools, 1 router" |
| 2 | Twitter/X | Thread: usage breakdown |
| 3 | Dev.to | Article: "How I stopped paying $$$ for tasks free tools handle" |
| 4 | HN | Show HN post |
| 5 | Product Hunt | Launch |
| 6 | YouTube | 3-min demo video |
| 7 | LinkedIn | Results post: "X stars in Y weeks" |
| 8 | Dev.to | Tutorial: "Add your own agents to ai-route" |

### Monetization Timeline

| Month | Action | Revenue Target |
|-------|--------|---------------|
| 1 | Open source launch, build audience | $0 (investment) |
| 2 | Add YAML config + LLM classifier | $0 (building Pro) |
| 3 | Launch ai-route Pro ($9/mo) | $200-500/mo |
| 4 | Consultoria "AI Stack Setup" (R$3k) | R$6-9k/mo |
| 5 | Team tier ($29/mo per seat) | $500-2k/mo |
| 6 | Evaluate: double down or pivot | Data-driven |

### Pro Features (ai-route Pro — $9/mo)

- LLM-based classifier (more accurate than regex)
- Custom agent registry via YAML
- Decision history + analytics dashboard
- Feedback loop (learns your preferences)
- Priority support
- Badge: "Pro" in CLI output

### Consultoria Package

**"AI Stack Setup for Dev Teams"**
- Audit: which tools the team has, which are redundant
- Setup: ai-route configured for the team's stack
- Training: 2h workshop on optimal tool usage
- Deliverable: team-specific YAML config + documentation
- Price: R$3-5k per team (up to 10 devs)

---

## KPIs to Track

| Metric | Week 1 | Month 1 | Month 3 |
|--------|--------|---------|---------|
| GitHub Stars | 50 | 200 | 1000 |
| PyPI Downloads | 100 | 500 | 2000 |
| LinkedIn Post Views | 5k | - | - |
| HN Points | 50+ | - | - |
| Product Hunt Upvotes | - | 200+ | - |
| Paying Customers | - | - | 20+ |

---

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Big player builds this | First-mover + community loyalty |
| Regex too simple | Upgrade to LLM classifier in v0.2 |
| Low adoption | Content marketing + consultoria |
| Free copycats | MIT is fine — brand + community is the moat |
| Tools change fast | YAML config lets users update without code |
