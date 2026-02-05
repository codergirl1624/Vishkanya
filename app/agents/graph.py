import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Define the AI's "Memory"
class AgentState(TypedDict):
    transcript: str
    entities: dict
    call_active: bool
    mood: str # 'confused', 'agitated', 'cooperative'
    messages: list
    extracted_data: dict
    threat_level: int  # 0 to 100

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Node: The "Chameleon" Persona
def chameleon_persona(state: AgentState):
    prompt = "You are a slightly confused elderly person. Keep the caller talking. Do not give real info."
    # Logic to generate response based on current transcript
    response = llm.invoke(state['messages'] + [prompt])
    return {"messages": [response]}

# 3. Node: The "Harvester" (Forensic Extraction)
def harvest_data(state: AgentState):
    # Ask Gemini to extract UPI, Bank, or Phishing links from the last message
    last_msg = state['messages'][-1].content
    extraction_prompt = f"Extract UPI ID, Bank Name, or URLs from: {last_msg}. Return JSON."
    entities = llm.invoke(extraction_prompt)
    return {"extracted_data": entities}

# 4. Construct the Graph
workflow = StateGraph(AgentState)
workflow.add_node("chat", chameleon_persona)
workflow.add_node("harvest", harvest_data)
workflow.set_entry_point("chat")
workflow.add_edge("chat", "harvest")
workflow.add_edge("harvest", "chat") # Loop back to keep the conversation going
vish_kanya_graph = workflow.compile()
