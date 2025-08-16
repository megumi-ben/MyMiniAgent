from fastapi import FastAPI
from ag_ui.core import RunAgentInput
from http import HTTPStatus
from pydantic_ai.ag_ui import run_ag_ui, SSE_CONTENT_TYPE
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import Agent
from pydantic import ValidationError
import os
import json
from dotenv import load_dotenv
from fastapi.requests import Request
from fastapi.responses import Response, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


deepseek_provider = OpenAIProvider(api_key=os.getenv("DEEPSEEK_API_KEY"),
                                   base_url="https://api.deepseek.com/v1")
deepseek_model = OpenAIModel(
    model_name = "deepseek-chat",
    provider = deepseek_provider
)

agent = Agent(model=deepseek_model,
              system_prompt = "你是一个智能助手"
            )



app = FastAPI()
app.add_middleware(  # 跨域处理
    CORSMiddleware,
    allow_origins=["*"],  # 或指定你的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def ag_ui_endpoint(request: Request):
    accept = request.headers.get('accept', SSE_CONTENT_TYPE)
    try:
        run_input = RunAgentInput.model_validate(await request.json())
    except ValidationError as e:
        return Response(
            content=json.dumps(e.json()),
            media_type='application/json',
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    event_stream = run_ag_ui(agent, run_input, accept=accept)
    return StreamingResponse(event_stream, media_type=accept)
