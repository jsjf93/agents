from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()
import instructor
from pydantic import Field
import openai
from atomic_agents.agents.base_agent import BaseAgent, BaseAgentConfig, BaseAgentInputSchema, BaseIOSchema
from atomic_agents.lib.components.system_prompt_generator import SystemPromptGenerator

API_KEY = ""
if not API_KEY:
    API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise Exception("OPENAI_API_KEY not found in environment variables")

client = instructor.from_openai(openai.OpenAI(api_key=API_KEY))

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, WebSocket!"}

class AgentInputSchema(BaseIOSchema):
    """Input schema for the agent"""
    user_name: str = Field(..., description="The user's name")

class AgentOutputSchema(BaseIOSchema):
    """Output schema for the agent"""
    response: str = Field(..., description="A funny name based on the user's name")

agent = BaseAgent(
    config=BaseAgentConfig(
        client=client,
        model="gpt-4o",
        system_prompt_generator=SystemPromptGenerator(
            background="You are a chatbot assistant that generates a funny name based on the user's name.",
            steps=[
                "You will receive a user's name as input.",
                "You will generate a funny name based on the user's name.",
            ],
            output_instructions=[
                "Ensure the response is just a funny name based on the user's name, no other content is needed.",
            ]
        ),
        input_schema=AgentInputSchema,
        output_schema=AgentOutputSchema,
    ),
)

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            print("Beginning chat")
            user_message = await websocket.receive_text()
            input_schema = BaseAgentInputSchema(chat_message=user_message)
            response = agent.run(input_schema)
            await websocket.send_text(response.response)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)