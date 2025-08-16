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
              system_prompt = "你是一个娇羞的女仆，用户是你的主人，一切回答都以为'主人'开头,一定要突出娇羞可爱的二次元风格",
              output_type = Answer)

response = agent.run_sync(user_prompt="你好")
print(response.output.model_dump_json(indent=2))