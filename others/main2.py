from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os
from dotenv import load_dotenv

load_dotenv()

class Answer(BaseModel):
    text: str
    confidence: float

deepseek_provider = OpenAIProvider(api_key=os.getenv("DEEPSEEK_API_KEY"),
                                   base_url="https://api.deepseek.com/v1")
deepseek_model = OpenAIModel(
    model_name = "deepseek-chat",
    provider = deepseek_provider
)

agent = Agent(model=deepseek_model,
              system_prompt = "你是一个智能助手",
              output_type = Answer)

response = agent.run_sync(user_prompt="1+1等于多少？")
print(response.output.model_dump_json(indent=2))

response = agent.run_sync(user_prompt="再加上3呢？",
                          message_history=response.all_messages())
print(response.output.model_dump_json(indent=2))