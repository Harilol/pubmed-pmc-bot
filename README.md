# 🧬 pubmed-pmc-bot
 
> **Biomedical Research Agent** — Ask a medical question, get synthesized insights from real scientific literature.
 
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)](https://langchain-ai.github.io/langgraph/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit)](https://streamlit.io)
[![LLM](https://img.shields.io/badge/LLM-Groq%20Llama--3.1--8b-green)](https://groq.com)
[![Data](https://img.shields.io/badge/Data-NCBI%20E--utilities-lightblue)](https://www.ncbi.nlm.nih.gov/home/develop/api/)
 
---
 
## 🔍 What is this?
 
**pubmed-pmc-bot** is an agentic AI system that autonomously routes your biomedical research queries to the right NCBI database — **PubMed** (abstracts) or **PMC** (full-text articles) — fetches real-time scientific literature, and uses an LLM to synthesize the findings into a coherent answer.
 
No more manually searching PubMed. Just ask your question in plain English.
 
---
 
## 🏗️ Architecture
 
```
User Query
    │
    ▼
┌─────────────────────────┐
│   Supervisor Agent      │  ◄── LangGraph node
│  (Intent Classifier)    │      decides routing
└────────┬────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
PubMed     PMC Tool
 Tool      (Full-text)
(Abstracts)
    │         │
    └────┬────┘
         ▼
  NCBI E-utilities API
  (Live literature fetch)
         │
         ▼
  Context Truncation
  (Smart token management)
         │
         ▼
   Groq LLM (Llama-3.1-8b)
   Synthesizes findings
         │
         ▼
  Streamlit UI Response
```
 
The **supervisor node** is the brain — it reads the user's query and dynamically decides whether to search PubMed (good for quick abstract-level answers) or PMC (good for methodology, full study details). This is **agentic routing**, not static if-else logic.
 
---
 
## ✨ Features
 
| Feature | Description |
|---|---|
| 🤖 **Agentic Routing** | LangGraph supervisor dynamically picks PubMed vs PMC based on query intent |
| 📡 **Live Data** | Fetches real-time papers via NCBI E-utilities API — no static datasets |
| 🧠 **LLM Synthesis** | Groq's Llama-3.1-8b reads and synthesizes multiple papers into one answer |
| ✂️ **Smart Context Management** | Truncates large full-text PMC articles to stay within LLM token limits without losing intro/methods sections |
| 🖥️ **Clean UI** | Streamlit interface for seamless querying and research review |
| 🆓 **Fully Free Stack** | Groq free tier + NCBI free API — zero cost to run |
 
---
 
## 🛠️ Tech Stack
 
| Layer | Tool |
|---|---|
| Agent Framework | LangGraph + LangChain |
| LLM | Groq — `llama-3.1-8b-instant` |
| Data Source | NCBI E-utilities API (PubMed & PMC) |
| UI | Streamlit |
| Language | Python 3.10+ |
 
---
 
## 🚀 Getting Started
 
### 1. Clone the repository
 
```bash
git clone https://github.com/Harilol/pubmed-pmc-bot.git
cd pubmed-pmc-bot
```
 
### 2. Install dependencies
 
```bash
pip install -r requirements.txt
```
 
### 3. Set up your API key
 
Create a `.env` file in the root directory:
 
```bash
GROQ_API_KEY="your-groq-api-key-here"
```
 
Get your free Groq API key at [console.groq.com](https://console.groq.com)
 
### 4. Run the app
 
```bash
streamlit run ui.py
```
 
Open your browser at `http://localhost:8501` and start asking biomedical questions!
 
---
 
## 💡 Example Queries
 
```
"What are the latest treatments for triple-negative breast cancer?"
"Summarize research on GLP-1 receptor agonists and weight loss"
"What does literature say about CRISPR off-target effects?"
"Recent studies on Alzheimer's and neuroinflammation"
```
 
---
 
## 📁 Project Structure
 
```
pubmed-pmc-bot/
├── bot.py              # Core agent logic (LangGraph graph, tools, routing)
├── ui.py               # Streamlit frontend
├── requirements.txt    # Dependencies
├── .env                # API keys (not committed)
├── .gitignore
└── README.md
```
 
---

## ⚠️ Known Limitations
 
### PMC Full-Text Truncation
PMC articles are often **very long** (10,000–50,000+ characters). To avoid hitting Groq's token limits, extracted full-text is currently **truncated to the first 4,000 characters**.
 
This means:
- You get the intro and early methods, but **results/discussion/conclusion may be cut off**
- Complex multi-paper synthesis may be incomplete
**If this is a problem for your use case, consider:**
- Switching to a model with a larger context window (e.g. `llama-3.1-70b` on Groq, or GPT-4o / Claude)
- Using PubMed abstracts instead of PMC full-text for quicker, summarized answers
- Increasing the truncation limit carefully: in `bot.py`, find `[:4000]` and increase — but watch out for rate limit / token errors
> 💡 **Tip:** For most research questions, PubMed abstracts are sufficient. Route to PMC only when you need full methodology or supplementary details.
 
---
 
## 🔮 Roadmap
 
- [ ] Add citation links back to original PubMed/PMC papers
- [ ] Support multi-turn conversation memory
- [ ] Export research summaries as PDF
- [ ] Add MeSH term expansion for better query coverage
- [ ] Deploy on Streamlit Cloud
---
 
## 🧑‍💻 Author
 
**Harilol (Narasimha Reddy)**
Final-year B.Tech AI & Data Science | Aspiring AI for Drug Discovery researcher
 
[GitHub](https://github.com/Harilol) · [LinkedIn](https://www.linkedin.com/in/narasimha-reddy291204)
 
---
 
## 📄 License
 
MIT License — free to use, modify, and distribute.
 
---
 
*Built with LangGraph + Groq + NCBI E-utilities*
