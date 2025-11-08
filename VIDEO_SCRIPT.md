# Agent-Ledger: Video Script for Hackathon Submission

**Duration:** 3 minutes
**Format:** Screen recording with voiceover
**Tone:** Professional, confident, clear

---

## 🎬 **Opening (0:00 - 0:15)**

**[SHOW: Title slide or you on camera]**

> "Hi! I'm [Your Name], and I built **Agent-Ledger** — the first AI-powered legal services platform that's actually compliant with legal ethics rules.
>
> We're solving a trillion-dollar problem that's kept the entire legal industry out of Web3. Let me show you."

---

## 💡 **The Problem (0:15 - 0:45)**

**[SHOW: Simple slide or just talk to camera]**

> "Here's the problem: The legal industry wants to accept cryptocurrency payments, but they *can't*.
>
> Why? **Volatility.**
>
> When you pay a lawyer with Bitcoin or Ethereum, the New York State Bar says that's not a 'payment' — it's a 'property transaction.' And that triggers Rule 1.8(a), which requires lawyers to tell their clients to hire *another lawyer* just to review the payment terms.
>
> That's absurd. And it's all because of price volatility. So the $1 trillion legal industry is completely locked out of Web3."

---

## 🔧 **The Solution (0:45 - 1:15)**

**[SHOW: Architecture diagram or simple bullet points]**

> "Agent-Ledger solves this by **eliminating volatility from the entire payment stack.**
>
> Here's how:
>
> **First** — We use USDC. It's a stablecoin, 1-to-1 backed by US dollars. No volatility.
>
> **Second** — We built this on Arc, which is the *first blockchain ever* to use USDC as its *native gas token.* So even the transaction fees are stable and dollar-denominated.
>
> **Third** — We use Circle Paymaster to sponsor gas fees. So for the client, it's completely gasless — just like paying with a credit card.
>
> The result? 100% of the transaction is dollar-denominated. No volatility. Which means we've removed the ethical blocker. We created the first *compliant* on-chain payment rail for legal services."

---

## 🖥️ **The Demo (1:15 - 2:30)**

**[SHOW: Screen recording of your app at localhost:5000 or Vercel URL]**

> "Let me show you how it works. This is the full workflow, from order to completion.
>
> **[Navigate to Order Form]**
> A client can order a legal service — like forming a Wyoming DAO LLC. They just fill out this form with the basics: entity name, smart contract address, registered agent.
>
> **[Show voice alternative - optional]**
> Or, they can use our voice interface. They just say: 'I need to form a Wyoming DAO called DeFi Collective.' Our AI agent — powered by ElevenLabs and Google Gemini — understands that request and structures it automatically.
>
> **[Navigate to Payment]**
> The client pays in USDC. The platform moves the funds to an escrow wallet on the Arc Testnet. This transfer is *gasless* for the client — we sponsor it using Circle's Gas Station.
>
> **[Navigate to Lawyer Review]**
> Our human lawyer gets a notification. They review the AI-generated draft. If it looks good, they can approve it with one click — or even with a voice command.
>
> **[Navigate to Document Generated]**
> The AI instantly generates the final legal document from our template — this is deterministic, no hallucinations — and uploads it to a secure client locker.
>
> **[Navigate to Client Approval]**
> The client reviews the final document and approves it.
>
> At that moment, the funds are released from escrow to the law firm's main wallet. If there's a recurring annual fee, like for the Wyoming DAO, we schedule that automatically using APScheduler.
>
> **[Show final complete case]**
> And that's it. The case is complete. The document is theirs. The payment settled on-chain. All compliant, all gasless, all powered by USDC on Arc."

---

## 🚀 **The Platform Vision (2:30 - 2:50)**

**[SHOW: Roadmap slide or product slide]**

> "But Agent-Ledger isn't just one service. It's a *platform.*
>
> We've built what we call the 'Legal Service Factory.' It's designed to handle *any* deterministic legal task. We've already mapped out Wyoming DAOs, Delaware LLCs, and UCC-1 filings.
>
> Next up: contract review, cap table management, M&A due diligence.
>
> We're not building another tipping bot. We're building the infrastructure layer for the entire legal services industry to move on-chain."

---

## 🎯 **The Close (2:50 - 3:00)**

**[SHOW: You on camera or final slide with logo]**

> "This is the future of legal services: on-chain, autonomous, and powered by USDC.
>
> We used Arc's USDC-native gas because it's the *only* technical solution that solves the compliance problem that's blocked a trillion-dollar industry.
>
> Thanks for watching. I'm [Your Name], and this is Agent-Ledger."

---

## 📝 **Recording Tips**

### **For Screen Recording (Demo Section):**
1. **Open your app** at `http://localhost:5000` or your Vercel URL
2. **Have test accounts ready:**
   - Login as `client1` (password: `password123`)
   - Have `lawyer1` account ready for lawyer view
3. **Navigate slowly** — give viewers time to see each screen
4. **Point your cursor** to important elements (buttons, form fields)
5. **Keep browser window clean** — close other tabs

### **For Voiceover:**
1. **Speak clearly and at a moderate pace**
2. **Pause briefly** between sections
3. **Sound enthusiastic but professional**
4. **Re-record any section** if you stumble — it's okay!

### **Technical Setup:**
- **Tool:** Loom (https://www.loom.com/) or OBS Studio
- **Mode:** Screen + Camera (or just screen)
- **Resolution:** 1080p if possible
- **Audio:** Use headphones mic or dedicated mic (phone mic is okay too)

### **Editing (Optional):**
- Trim any long pauses
- Add captions if time permits
- Add your logo/project name at start/end

---

## 🎥 **Quick Loom Guide**

1. Go to https://www.loom.com/ and sign up (free)
2. Install Loom desktop app or Chrome extension
3. Click "Start Recording"
4. Choose:
   - **Screen + Camera** (shows you in corner bubble) — RECOMMENDED
   - **Screen Only** (just the app)
5. Select which screen/window to record
6. Click "Start Recording"
7. Read this script naturally (don't memorize — sound conversational!)
8. Click "Stop" when done
9. Loom gives you a shareable link immediately
10. **Paste that link into lablab.ai submission form**

---

## ⏱️ **Time Budget**

- **0:00-0:15** — Opening (15 sec)
- **0:15-0:45** — Problem (30 sec)
- **0:45-1:15** — Solution (30 sec)
- **1:15-2:30** — Demo (75 sec) ← *Most important!*
- **2:30-2:50** — Vision (20 sec)
- **2:50-3:00** — Close (10 sec)

**Total: 3 minutes**

---

## 🏆 **You've Got This!**

Remember:
- **Energy matters** — Sound excited about what you built!
- **Clarity over perfection** — A clear explanation beats perfect production
- **Show, don't just tell** — The demo is your strongest asset
- **Practice once** — Do a dry run to get comfortable, then record for real

**This is a winning project. Now show them why! 🚀**
