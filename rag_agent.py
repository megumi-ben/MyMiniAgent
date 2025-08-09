from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import embeding

load_dotenv()

class Question(BaseModel):
    question: str = Field(..., description="知识库指示词")

deepseek_provider = OpenAIProvider(api_key=os.getenv("DEEPSEEK_API_KEY"),
                                   base_url="https://api.deepseek.com/v1")
deepseek_model = OpenAIModel(
    model_name = "deepseek-chat",
    provider = deepseek_provider
)
agent = Agent(
    model=deepseek_model,
    system_prompt = "你是一个智能助手",
    deps_type= Question,
)  

@agent.tool
def retrieve(ctx: RunContext[Question]) -> str:
    strs = embeding.query_db(ctx.deps.question)
    return "\n------\n".join(strs)

def main(): 
    result = agent.run_sync(
        user_prompt='调用tool获取信息',
        deps=Question(question="西交学长")
    )
    print(result.output)




if __name__ == "__main__":
    main()