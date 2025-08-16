from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

class Answer(BaseModel):
    text: str = Field(description="给用户的回答，报告操作结果")
    confidence: float = Field(description="回答的置信度")
    
class FileInfo(BaseModel):
    filename: str = Field(description="文件名")
    content: str = Field(description="文件内容")
    new_filename: str = Field(default="", description="新文件名（用于重命名）")
    
deepseek_provider = OpenAIProvider(api_key=os.getenv("DEEPSEEK_API_KEY"),
                                   base_url="https://api.deepseek.com/v1")
deepseek_model = OpenAIModel(
    model_name = "deepseek-chat",
    provider = deepseek_provider
)

def make_file(ctx: RunContext[FileInfo]) -> str:
    """创建文件"""
    print("agent正在创建文件...")
    file_info = ctx.deps
    try:
        with open(file_info.filename, 'w', encoding='utf-8') as f:
            f.write(file_info.content)
        return f"文件 {file_info.filename} 创建成功，内容已写入。"
    except Exception as e:
        print(f"创建文件时发生错误：{str(e)}")
        return f"文件创建失败：{str(e)}"

def remove_file(ctx: RunContext[FileInfo]) -> str:
    """删除文件"""
    print("agent正在删除文件...")
    file_info = ctx.deps
    try:
        if os.path.exists(file_info.filename):
            os.remove(file_info.filename)
            return f"文件 {file_info.filename} 删除成功。"
        else:
            return f"文件 {file_info.filename} 不存在，无法删除。"
    except Exception as e:
        print(f"删除文件时发生错误：{str(e)}")
        return f"文件删除失败：{str(e)}"

def read_file(ctx: RunContext[FileInfo]) -> str:
    print("agent正在读取文件内容...")
    file_info = ctx.deps
    try:
        if os.path.exists(file_info.filename):
            with open(file_info.filename, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"文件 {file_info.filename} 内容如下：\n{content}"
        else:
            return f"文件 {file_info.filename} 不存在，无法读取。"
    except Exception as e:
        return f"文件读取失败：{str(e)}"

def rename_file(ctx: RunContext[FileInfo]) -> str:
    print("agent正在重命名文件...")
    file_info = ctx.deps
    try:
        if not file_info.new_filename:
            return "未指定新文件名，无法重命名。"
        if os.path.exists(file_info.filename):
            os.rename(file_info.filename, file_info.new_filename)
            return f"文件 {file_info.filename} 已重命名为 {file_info.new_filename}。"
        else:
            return f"文件 {file_info.filename} 不存在，无法重命名。"
    except Exception as e:
        return f"文件重命名失败：{str(e)}"

def append_file(ctx: RunContext[FileInfo]) -> str:
    print("agent正在续写文件...")
    file_info = ctx.deps
    try:
        with open(file_info.filename, 'a', encoding='utf-8') as f:
            f.write(file_info.content)
        return f"内容已追加到文件 {file_info.filename}。"
    except Exception as e:
        return f"文件续写失败：{str(e)}"

def call_main_py(ctx: RunContext[FileInfo]) -> str:
    print("agent正在调用main.py...")
    file_info = ctx.deps
    try:
        result = subprocess.run(
            ["python", "main.py", file_info.content],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"{result.stdout}")
            return f"main.py输出：\n{result.stdout}"
        else:
            return f"调用main.py失败：{result.stderr}"
    except Exception as e:
        return f"调用main.py异常：{str(e)}"

agent = Agent(model=deepseek_model,
              system_prompt="你是一个文件管理助手，可以帮助用户对文件进行增删改查重命名等操作，"
              "记住调用tool方法时不要说自己无法操作，而是根据方法的返回值来回答操作结果",
              deps_type=FileInfo,
              output_type=Answer,
              tools=[make_file, remove_file, read_file, rename_file, append_file, call_main_py])

# # 创建文件
# response = agent.run_sync(
#     user_prompt="请创建一个test.txt文件，内容是'Hello World'",
#     deps=FileInfo(filename="test.txt", content="Hello World")
# )
# print(response.output.model_dump_json(indent=2))

# # 续写文件
# response = agent.run_sync(
#     user_prompt="请在test.txt文件后追加内容' 你好，世界！'",
#     deps=FileInfo(filename="test.txt", content=" 你好，世界！"),
#     # message_history=response.all_messages()
# )
# print(response.output.model_dump_json(indent=2))

# # 读取文件
# response = agent.run_sync(
#     user_prompt="请读取test.txt文件内容",
#     deps=FileInfo(filename="test.txt", content=""),
#     # message_history=response.all_messages()
# )
# print(response.output.model_dump_json(indent=2))

# 调用main.py
response = agent.run_sync(
    user_prompt="请调用main.py",
    deps=FileInfo(filename="", content="测试参数"),
    # message_history=response.all_messages()
)
print(response.output.model_dump_json(indent=2))

# # 重命名文件
# response = agent.run_sync(
#     user_prompt="请把test.txt重命名为test2.txt",
#     deps=FileInfo(filename="test.txt", content="", new_filename="test2.txt"),
#     # message_history=response.all_messages()
# )
# print(response.output.model_dump_json(indent=2))

# # 删除文件
# response = agent.run_sync(
#     user_prompt="请删除test2.txt文件",
#     deps=FileInfo(filename="test2.txt", content=""),
#     message_history=response.all_messages()
# )
# print(response.output.model_dump_json(indent=2))


# response = agent.run_sync(
#     user_prompt="首先创建文件test.txt，内容是'helloworld'，然后继续新增内容'你好世界'，最后把文件重命名为test2.txt，回答要体现每个步骤的结果",
#     deps=FileInfo(filename="test.txt", content="你好世界", new_filename="test2.txt"),
#     # message_history=response.all_messages()
# )
# print(response.output.model_dump_json(indent=2))