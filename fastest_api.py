from typing import Union 

from fastapi import FastAPI
from pydantic import BaseModel 

# Import agent - handle both relative and absolute imports
try:
    from . import agent
except ImportError:
    import agent

# Add parent directory to path to import apikey
import sys
import os

# Get the parent directory (root of the project)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import openai_api_key
from openai import OpenAI

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

#Allow calls from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def reat_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Define request model for better API design
class ResearchRequest(BaseModel):
    prompt: str
    max_questions: int = 5
    output_format: str = "html"  # "html" or "text"

class ResearchResponse(BaseModel):
    content: str
    format: str
    questions_count: int

@app.post("/research", response_model=ResearchResponse)
async def deep_research(request: ResearchRequest):
    prompt = request.prompt
    output_format = request.output_format
    
    #load OpenAI client
    cliente = OpenAI(api_key=openai_api_key)  # Fixed: changed 'apikey' to 'api_key'
    #create agent object
    core_agent = agent.Agent(cliente, 1)

    #Clear the research file before starting new research
    with open("test_research.txt", 'w') as file: 
        file.write("")

    #Breakdown the prompt, the prompt will come from the web ui 
    breakdown = core_agent.break_down_question_with_llm(prompt)
    #Create a set of questions and answer them all async 
    await core_agent.break_down_formatter_async(breakdown)
    
    # Get the result in the requested format
    if output_format == "html":
        final_result = core_agent.compile_research_html()
    else:
        final_result = core_agent.compile_research()
    
    # Count questions for metadata
    try:
        import json
        breakdown_data = json.loads(breakdown.strip().strip("'''").strip())
        questions_count = len(breakdown_data)
    except:
        questions_count = 0

    return ResearchResponse(
        content=final_result,
        format=output_format,
        questions_count=questions_count
    )

# Keep old endpoint for backward compatibility (deprecated)
@app.get("/asyncagent/{prompt}")
async def deep_research_legacy(prompt: str):
    """Legacy endpoint - use POST /research instead"""
    request = ResearchRequest(prompt=prompt)
    return await deep_research(request)
