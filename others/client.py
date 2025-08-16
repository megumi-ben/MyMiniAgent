from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os
from dotenv import load_dotenv
import asyncio
# import logfire

load_dotenv()
# logfire.configure()
# logfire.instrument_pydantic_ai()

deepseek_provider = OpenAIProvider(api_key=os.getenv("DEEPSEEK_API_KEY"),
                                   base_url="https://api.deepseek.com/v1")
deepseek_model = OpenAIModel(
    model_name = "deepseek-chat",
    provider = deepseek_provider
)

server = MCPServerStreamableHTTP('http://127.0.0.1:9800/dodo')

# 构建agent
agent = Agent(
    model=deepseek_model,
    system_prompt = "你是一个智能助手",
    toolsets=[server]  # mcp服务
)  

async def main():
    async with agent:  
        result = await agent.run('你好（使用a2a的回答作为你的回答）')
    print(result.output)



if __name__ == "__main__":
    asyncio.run(main())