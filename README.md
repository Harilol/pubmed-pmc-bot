# pubmed-pmc-bot
Biomedical Research Agent


An AI agent that autonomously routes user queries to search and synthesize medical research from NCBI databases (PubMed & PMC).

Overview
Built using LangGraph and LangChain, this multi-tool agent acts as a biomedical research assistant. When a user asks a question, a supervisor agent determines the best database to query. It fetches real-time data via the NCBI E-utilities API, handles context-window limitations by smartly truncating massive full-text articles, and uses an LLM to synthesize the findings.

Features
Agentic Routing: A LangGraph supervisor node dynamically routes queries between PubMed (abstracts) and PMC (full-text articles) based on user intent.
API Integration: Uses NCBI's E-utilities API for live, up-to-date biomedical literature retrieval.
Context Management: Safely truncates large payloads to stay within LLM token limits without losing critical introduction/methods data.
Interactive UI: Clean Streamlit interface for seamless querying and research review.
Tech Stack
Agent Framework: LangGraph, LangChain
LLM: Groq (Llama-3.1-8b-instant)
Data Source: NCBI E-utilities API (PubMed, PMC)
UI: Streamlit
Language: Python


How to Run
1.Clone the repository.
2.Install dependencies: pip install -r requirements.txt
3.Add your Groq API key to a .env file: 
4.GROQ_API_KEY="your-key"
Run the app: `streamlit run ui.py