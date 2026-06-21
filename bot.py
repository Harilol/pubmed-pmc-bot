import requests
import re
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@tool
def fetch_papers(query: str,max_results: int = 5) ->str:
     """Fetches papers from PubMed based on a query."""
     search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
     params = {
         "db" : "pubmed",
         "term" : query,
         "retmax" : max_results
     }

     response = requests.get(search_url,params=params)

     id = re.findall(r"<Id>(\d+)</Id>",response.text)

     if not id:
        return "not found"

     fetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

     params1 = {
        "db" : "pubmed",
        "id" : ",".join(id),
        "rettype" : "abstract",
        "retmode": "text"
     }

     res = requests.get(fetch,params = params1)
     return res.text
     return f"{res.text}\n\nSource: https://pubmed.ncbi.nlm.nih.gov/{id[0]}/"


@tool
def fetch_full_papers(query: str,max_results: int = 5) ->str:
     """Searches PMC for full-text research articles."""
     search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
     params = {
         "db" : "pmc",
         "term" : query,
         "retmax" : max_results
     }

     response = requests.get(search_url,params=params)

     id = re.findall(r"<Id>(\d+)</Id>",response.text)

     if not id:
        return "not found"

     fetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

     params1 = {
        "db" : "pmc",
        "id" : ",".join(id),
        "rettype" : "abstract",
        "retmode": "text"
     }

     res = requests.get(fetch,params = params1)
     return res.text
     return f"{res.text}\n\nSource: https://pubmed.ncbi.nlm.nih.gov/{id[0]}/"

from typing import TypedDict
from langchain_groq import ChatGroq
llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.1-8b-instant")



class box(TypedDict, total=False):
    query:str
    final:str
    db_choice:str
    max_results:int
    raw_results:str


def decide(state:box):
    if state.get('db_choice')=="pmc":
        return "agent1"
    else:
        return "agent"
        
def supervise(state:box):
    selected_db = state.get("db_choice", "auto")
    if selected_db in {"pubmed", "pmc"}:
        return {"db_choice" : selected_db}

    a = llm.invoke(f"ur a supervise agent who decides if user query related to pmc or pubmed and JUST REPLY WITH EITHER pmc or pubmed,nothing else. user query: {state['query']}")
    choice = a.content.strip().lower()
    return {"db_choice" : "pmc" if "pmc" in choice else "pubmed"}


def agent(state:box):
    a = fetch_papers.invoke({"query" : state['query'], "max_results": state.get("max_results", 5)})
    r = llm.invoke(f"ur a helpful research bot who helps for user in searching research papers and summarize the given content based on user request,dont miss the important details and give results in professional format and include author name and released date on top,research paper: {a},users query: {state['query']}")
    return {'final' : r.content, "raw_results": a}


def agent1(state:box):
    a = fetch_full_papers.invoke({"query" : state['query'], "max_results": state.get("max_results", 5)})
    short_papers = a[:3000] 
    r = llm.invoke(f"ur a helpful research bot who helps for user in searching research papers and summarize the given content based on user request,dont miss the important details and give results in professional format and include author name and released date on top,research paper: {short_papers},users query: {state['query']}")
    return {'final' : r.content, "raw_results": a}

#!pip install langgraph
from langgraph.graph import StateGraph, END

gra = StateGraph(box)

gra.add_node("agent",agent)
gra.add_node("agent1",agent1)
gra.add_node("supervise",supervise)

gra.set_entry_point("supervise")
gra.add_conditional_edges("supervise",decide,{"agent1" : "agent1","agent" : "agent"})
gra.add_edge("agent1",END)
gra.add_edge("agent",END)

shi = gra.compile()