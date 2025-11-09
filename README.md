
# Krew – Autonomous Multi-Agent AI Organization Platform
> **Prototype Repository (Open Source) — Final Commercial Version Owned by DevKnight (DKCDEVKNIGHT TECHNOLOGIES PRIVATE LIMITED)**  
> **Original Author & Developer: Adil Deokar**

---

## 1. Overview  
Krew is a modular, autonomous **multi-agent AI orchestration platform** designed to simulate a fully functioning AI “organization” where multiple specialized AI agents collaborate on a task, similar to a human team.  
Instead of a single chatbot producing a response, Krew coordinates **multiple role-based agents** (Researcher, Technical Analyst, Writer, QA, Strategist, etc.) under a central **Manager Agent** that delegates work, synchronizes responses, and synthesizes the final output.

Krew is built for tasks such as:
- Research & analysis  
- Technical report generation  
- Business planning / strategy synthesis  
- Document interpretation and summarization  
- AI-assisted content creation  
- Multi-file data extraction + collaborative reasoning  

The platform runs locally using **Streamlit**, uses **OpenAI GPT-4o-mini** (or any compatible LLM), and requires no backend or external DB.  
It is fast to deploy, lightweight, extendable, and suitable for enterprise-grade workflows.

---

## 2. Origin & Development History  
Krew began as an independent R&D project by **Adil Deokar**, who conceptualized and developed **99% of the system’s architecture, agent logic, UI, backend workflow, and overall implementation**.

The goals during initial development were:
1. Prove that AI agents can collaborate meaningfully, not just generate isolated answers  
2. Create a deterministic, loop-safe multi-agent architecture without infinite recursion  
3. Build a **real-world usable prototype**, not just a research toy  
4. Make it modular enough to evolve into a commercial SaaS product  

The project evolved through internal **alpha → prototype → production-design** phases.  
All early code versions (pre-commercial) will remain open-source under `/prototype/`.

---

## 3. Ownership & Licensing Notice  

| Component | Ownership | License |
|-----------|-----------|---------|
| **Prototype (this repo)** | Created by **Adil Deokar** | Open-source (Custom License – see §15) |
| **All alpha builds & experimental versions** | Created by **Adil Deokar** | Open-source, archived under `/prototype/` |
| **Final commercial SaaS version** | **Sold to DevKnight (DKCDEVKNIGHT TECHNOLOGIES PRIVATE LIMITED)** | Closed-source, commercial license |
| **Trademark & brand “Krew” (software IP)** | Transferred to DevKnight | Legally owned & controlled by DevKnight |

✅ This repository contains **ONLY** the open-source prototype version.  
✅ The commercial version is **not** open-source, not hosted here, and is not permitted to be cloned, modified, or resold.  

---

## 4. Prototype vs Commercial Product

| Feature | Prototype (This Repo) | Final SaaS Version (Owned by DevKnight) |
|---------|-----------------------|----------------------------------------|
| Streamlit UI | ✅ | ✅ |
| Multi-Agent Logic | ✅ | ✅ (Advanced) |
| Local execution | ✅ | ❌ (Cloud-hosted SaaS) |
| User authentication | ❌ | ✅ |
| Billing / credits | ❌ | ✅ |
| Teams / workspaces | ❌ | ✅ |
| Export & reports | ✅ Basic | ✅ Enterprise-grade |
| Model options | GPT-4o-mini | Multiple LLM options + fine-tuned models |
| Plugin marketplace | ❌ | ✅ |
| API access | ❌ | ✅ |
| Enterprise deployment | ❌ | ✅ SOC-2, RBAC, SSO, Logging |

The prototype exists as a **reference implementation**, a technical proof-of-concept, and a foundation for future community forks.

---

## 5. Architecture & Technology Stack  

```

┌──────────────────────────────────────────────┐
│                User Interface                │
│              (Streamlit Frontend)            │
└──────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────┐
│           Session & State Engine             │
│         (Python, In-Memory Store)            │
└──────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────┐
│                Manager Agent                 │
│    Coordinates, delegates, synthesizes       │
└──────────────────────────────────────────────┘
│
┌──────────┼──────────┬──────────┐
▼          ▼          ▼          ▼
Research    Technical   Creative     QA
Agent       Agent       Writer     Agent
(LLM Role)  (LLM Role)   (LLM Role) (LLM Role)
└──────────┴──────────┴──────────┘
│
▼
Final Answer + Export + Logs

````

✅ Modular Python codebase  
✅ Plug-and-play agent roles  
✅ File parsing for PDF / DOCX / CSV / TXT  
✅ Deterministic round-robin message passing  

---

## 6. Features  

✅ Multi-agent collaborative reasoning  
✅ Agent role templates (editable in UI)  
✅ Upload & parse documents  
✅ Real-time agent chat timeline + status feed  
✅ Export chat, final results, and config as ZIP  
✅ Streamed OpenAI responses  
✅ No API key stored — user enters dynamically  
✅ Lightweight: runs locally on any machine  
✅ Fully modifiable + extendable Python architecture  

---

## 7. Installation & Setup  

### 1️⃣ Clone repository
```bash
git clone https://github.com/your-username/krew.git
cd krew
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the app

```bash
streamlit run app.py
```

### 4️⃣ Enter your OpenAI API key inside UI sidebar (not stored anywhere)

---

## 8. Deployment Options

| Method                        | Supported              |
| ----------------------------- | ---------------------- |
| Local execution (PC / laptop) | ✅                      |
| Streamlit Cloud               | ✅                      |
| Dockerized deployment         | ✅ (manual setup)       |
| Heroku / Railway / Render     | ✅                      |
| Kubernetes scaling            | Prototype: ❌ / SaaS: ✅ |

---

## 9. Folder Structure

```
krew/
│── app.py
│── core/
│   ├── agents.py
│   ├── processor.py
│   ├── export.py
│   └── session.py
│── ui/
│   ├── layout.py
│   └── sidebar.py
│── config/
│   └── predefined_agents.py
│── prototype/         ← all alpha + earlier builds stored here
│── requirements.txt
│── README.md
│── LICENSE
```

---

## 10. Roadmap (Public Prototype)

| Stage                      | Status      |
| -------------------------- | ----------- |
| v1 Prototype (Open Source) | ✅ Completed |
| Agent modularization       | ✅           |
| File ingestion pipeline    | ✅           |
| Export system              | ✅           |
| Plugin system              | 🔜          |
| Local vector memory        | 🔜          |
| Model-agnostic LLM support | 🔜          |
| HuggingFace offline mode   | 🔜          |

---

## 11. Contribution Guidelines

✅ Forks are allowed
✅ Pull requests welcome (prototype only)
❌ No derivative products may use the **Krew** name commercially
❌ Do not attempt to clone or reverse-engineer the **DevKnight production version**

---

## 12. Legal Notice (IP Sale & Rights Transfer)

* **Krew was created, authored, and engineered primarily by *Adil Deokar* (99% contributor).**
* The **commercial rights, brand usage rights, distribution rights, and SaaS licensing rights** were **sold to DevKnight (DKCDEVKNIGHT TECHNOLOGIES PRIVATE LIMITED)**.
* The code in this repository is **not** the commercial version and **must not** be marketed, sold, or deployed as a paid service.
* This repository exists as a **permanent open-source record of the prototype**, not the final platform.

---

## 13. Credits

| Name               | Contribution                                            |
| ------------------ | ------------------------------------------------------- |
| **Adil Deokar**    | Founder, Architect, Lead Developer                      |
| **Monika Jadhav**  | Supporting Work                                         |
| **Azhaan Shaikh**  | Supporting Work                                         |
| **Pranav Bulbule** | Supporting Work                                         |
| **Soham Bagul**    | Supporting Work                                         |
| **Mohit Pokale**   | Supporting Work                                         |

No other parties, mentors, institutes, or organizations contributed to the codebase.

---

## 14. Contact & Support

📩 Business / Licensing: **[adildeokar@outlook.com](mailto:adildeokar@outlook.com)**
👤 Creator & Author (Prototype): **Adil Deokar**
🌐 Adil Deokar: **[https://adildeokar.com](https://adildeokar.com)**
🌐 DevKnight: **[https://devknight.club](https://devknight.club)**
🔒 Commercial product inquiries handled **exclusively by DevKnight**

---

## 15. License

This repository is released under a **Custom “Open-Source Prototype License”**:

```
You may:
✅ View, study, and modify the prototype code
✅ Fork the repository for educational or research use
✅ Build extensions or experimental versions for non-commercial use

You may NOT:
❌ Sell, host, or commercially deploy this code as a paid service
❌ Use the name “Krew” for any commercial product
❌ Redistribute a modified version under a commercial license
❌ Claim authorship or remove origin/ownership attribution

The final enterprise SaaS version of Krew is CLOSED SOURCE and owned by:
DevKnight (DKCDEVKNIGHT TECHNOLOGIES PRIVATE LIMITED)
```

Full legal license text is provided in `/LICENSE`.

---

