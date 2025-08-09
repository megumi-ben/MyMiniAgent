from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os
from dotenv import load_dotenv
import subprocess
from typing import List

load_dotenv()

# ================== 数据结构定义 ==================
class FileInfo(BaseModel):
    filename: str = Field(description="文件名")
    content: str = Field(default="", description="文件内容")
    new_filename: str = Field(default="", description="新文件名（用于重命名）")

class Command(BaseModel):
    prompt: str = Field(description="给operator的操作指令")
    file_info: FileInfo = Field(description="操作所需的文件信息")

# commander返回结构 ——— 指令列表
class CommandList(BaseModel):
    commands: List[Command] = Field(description="指令列表")
    
# operator返回结构
class OperatorResponse(BaseModel):
    text: str = Field(description="操作结果描述")
    success: bool = Field(description="操作是否成功")

# ================== 模型配置 ==================
deepseek_provider = OpenAIProvider(api_key=os.getenv("DEEPSEEK_API_KEY"),
                                   base_url="https://api.deepseek.com/v1")
deepseek_model = OpenAIModel(
    model_name="deepseek-chat",
    provider=deepseek_provider
)

# ================== Operator 工具方法 ==================
def make_file(ctx: RunContext[FileInfo]) -> str:
    """创建文件"""
    print("operator正在创建文件...")
    file_info = ctx.deps
    try:
        with open(file_info.filename, 'w', encoding='utf-8') as f:
            f.write(file_info.content)
        return f"文件 {file_info.filename} 创建成功，内容已写入。"
    except Exception as e:
        return f"文件创建失败：{str(e)}"

def remove_file(ctx: RunContext[FileInfo]) -> str:
    """删除文件"""
    print("operator正在删除文件...")
    file_info = ctx.deps
    try:
        if os.path.exists(file_info.filename):
            os.remove(file_info.filename)
            return f"文件 {file_info.filename} 删除成功。"
        else:
            return f"文件 {file_info.filename} 不存在，无法删除。"
    except Exception as e:
        return f"文件删除失败：{str(e)}"

def read_file(ctx: RunContext[FileInfo]) -> str:
    """读取文件"""
    print("operator正在读取文件内容...")
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
    """重命名文件"""
    print("operator正在重命名文件...")
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
    """续写文件"""
    print("operator正在续写文件...")
    file_info = ctx.deps
    try:
        with open(file_info.filename, 'a', encoding='utf-8') as f:
            f.write(file_info.content)
        return f"内容已追加到文件 {file_info.filename}。"
    except Exception as e:
        return f"文件续写失败：{str(e)}"

def call_main_py(ctx: RunContext[FileInfo]) -> str:
    """调用main.py"""
    print("operator正在调用main.py...")
    file_info = ctx.deps
    try:
        result = subprocess.run(
            ["python", "main.py", file_info.content],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return f"main.py执行成功，输出：\n{result.stdout}"
        else:
            return f"调用main.py失败：{result.stderr}"
    except Exception as e:
        return f"调用main.py异常：{str(e)}"

# ================== Agent 定义 ==================
# Commander Agent - 负责指令编排
commander = Agent(
    model=deepseek_model,
    system_prompt="""你是一个指令编排器，负责将用户的复杂请求分解为具体的操作指令。

支持的操作类型：
- 创建文件：prompt="创建文件"
- 读取文件：prompt="读取文件" 
- 删除文件：prompt="删除文件"
- 重命名文件：prompt="重命名文件"
- 续写文件：prompt="续写文件"
- 调用脚本：prompt="调用main.py"

请将用户请求分解为有序的指令列表，每个指令包含：
1. prompt: 给operator的具体操作指令
2. file_info: 操作所需的文件信息（filename, content, new_filename等）

注意：
- 如果是多步操作，请按执行顺序排列
- 确保每步的file_info信息完整准确
- 重命名操作需要同时提供filename和new_filename""",
    output_type=CommandList
)

# Operator Agent - 负责执行具体操作
operator = Agent(
    model=deepseek_model,
    system_prompt="""你是一个文件操作执行器，根据指令执行具体的文件操作。
请根据tool方法的返回结果，准确报告操作的成功与否及详细信息。""",
    deps_type=FileInfo,
    output_type=OperatorResponse,
    tools=[make_file, remove_file, read_file, rename_file, append_file, call_main_py]
)

# ================== 主要处理函数 ==================
def process_user_request(user_input: str) -> List[dict]:
    """处理用户请求的主函数"""
    print(f"用户输入: {user_input}")
    print("=" * 60)
    
    # 第一步：Commander 生成指令列表
    print("Commander 正在分析并生成指令列表...")
    commander_response = commander.run_sync(user_input)
    command_list = commander_response.output.commands
    
    print(f"Commander 生成了 {len(command_list)} 条指令:")
    for i, cmd in enumerate(command_list, 1):
        print(f"  {i}. {cmd.prompt} -> {cmd.file_info.filename}")
    print("-" * 40)
    
    # 第二步：Operator 逐个执行指令
    results = []
    for i, command in enumerate(command_list, 1):
        print(f"执行第 {i} 条指令: {command.prompt}")
        
        operator_response = operator.run_sync(
            user_prompt=command.prompt,
            deps=command.file_info
        )
        
        result = {
            "step": i,
            "command": command.prompt,
            "file_info": command.file_info.model_dump(),
            "result": operator_response.output.model_dump()
        }
        results.append(result)
        
        print(f"  结果: {operator_response.output.text}")
        print(f"  成功: {operator_response.output.success}")
        print("-" * 40)
    
    return results

# ================== 测试用例 ==================
if __name__ == "__main__":
    test_cases = [
        "请创建一个hello.txt文件，内容是'Hello World'",
        "首先创建文件test.txt，内容是'原始内容'，然后在后面添加'新增内容'，最后重命名为final.txt",
        "创建demo.txt写入'演示内容'，然后读取文件内容，最后删除该文件",
        "调用main.py脚本，参数是'测试参数'"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{'='*20} 测试用例 {i} {'='*20}")
        results = process_user_request(test_input)
        
        print(f"\n最终执行结果摘要:")
        for result in results:
            status = "✅" if result["result"]["success"] else "❌"
            print(f"  {status} 步骤{result['step']}: {result['command']}")
        
        print("\n" + "="*60)