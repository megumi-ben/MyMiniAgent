from pydantic import BaseModel,Field
from pydantic_ai import Agent,RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os
from dotenv import load_dotenv

load_dotenv()

class Answer(BaseModel):
    text: str = Field(description="回答的文本内容")
    confidence: float = Field(description="回答的置信度")
    
class Student(BaseModel):
    id: str = Field(description="学生ID")
    name: str = Field(description="学生姓名")
    age: int = Field(description="学生年龄")
    
deepseek_provider = OpenAIProvider(api_key=os.getenv("DEEPSEEK_API_KEY"),
                                   base_url="https://api.deepseek.com/v1")
deepseek_model = OpenAIModel(
    model_name = "deepseek-chat",
    provider = deepseek_provider
)

def check_customer(ctx: RunContext[Student]) -> str:
    student = ctx.deps
    return f"学生 {student.name} 的年龄是 {student.age} 岁，学号是 {student.id}。"

agent = Agent(model=deepseek_model,
              system_prompt = "你是一个智能助手",
              deps_type = Student,
              output_type = Answer,
              tools = [check_customer])

# @agent.tool
# def check_customer(ctx: RunContext[Student]) -> str:
#     student = ctx.deps
#     return f"学生 {student.name} 的年龄是 {student.age} 岁，学号是 {student.id}。"

response = agent.run_sync(user_prompt="该学生还差多少岁成年？",
                          deps=Student(id="1", name="张三", age=17))
print(response.output.model_dump_json(indent=2))

response = agent.run_sync(user_prompt="还有几年毕业呢？假设22岁毕业。",
                          message_history=response.all_messages())
print(response.output.model_dump_json(indent=2))