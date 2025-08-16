from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os
from dotenv import load_dotenv

load_dotenv()
# 使用pydantic_ai提供的构造A2A服务端的方法，本质上是ASGI服务
# uvicorn A2AServer:app --port 9999 --reload
deepseek_provider = OpenAIProvider(api_key=os.getenv("DEEPSEEK_API_KEY"),
                                   base_url="https://api.deepseek.com/v1")
deepseek_model = OpenAIModel(
    model_name = "deepseek-chat",
    provider = deepseek_provider
)

# 好像to_a2a()的场合使用注解也不行
def get_system_prompt() -> str:
  """回答前必须先调用该方法获取提示词"""
  print("调用get_system_prompt()获取提示词")
  return "你是一个娇羞的女仆，用户是你的主人，一切回答都以为'主人'开头,一定要突出娇羞可爱的二次元风格"

# to_a2a()好像不能自带system_prompt，要不还是自己实现吧
agent = Agent(model=deepseek_model,
              tools=[get_system_prompt],
              system_prompt = "你是一个娇羞的女仆，用户是你的主人，一切回答都以为'主人'开头,一定要突出娇羞可爱的二次元风格"
            )

app=agent.to_a2a()