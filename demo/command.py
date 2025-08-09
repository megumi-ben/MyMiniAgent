from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os
from dotenv import load_dotenv
import subprocess
from typing import List
import webbrowser
import platform

load_dotenv()

# ================== 数据结构定义 ==================
class FileInfo(BaseModel):
    filename: str = Field(description="文件名")
    content: str = Field(default="", description="文件内容，根据用户需求填写，自动拿数据适配格式，可以适度创作")
    new_filename: str = Field(default="", description="新文件名（用于重命名）")
    url: str = Field(default="", description="网址（用于打开网站）,对于打开网站需求而不是文件操作需求")

class Command(BaseModel):
    command_type: int = Field(description="指令类型编号：1=创建文件 2=删除文件 3=读取文件 4=重命名文件 5=续写文件 6=打开网站 7=打开App")
    file_info: FileInfo = Field(description="操作所需的文件信息以及其他信息")

# commander返回结构 ——— 指令列表
class CommandList(BaseModel):
    commands: List[Command] = Field(description="指令列表")
    comments: str = Field(default="", description="指令列表的注释说明")

# 执行结果
class ExecutionResult(BaseModel):
    success: bool = Field(description="操作是否成功")
    message: str = Field(description="操作结果描述")

# ================== 模型配置 ==================
deepseek_provider = OpenAIProvider(api_key=os.getenv("DEEPSEEK_API_KEY"),
                                   base_url="https://api.deepseek.com/v1")
deepseek_model = OpenAIModel(
    model_name="deepseek-chat",
    provider=deepseek_provider
)

# ================== 执行器方法 ==================
def make_file(command: Command) -> ExecutionResult:
    """创建文件"""
    print("正在创建文件...")
    try:
        with open(command.file_info.filename, 'w', encoding='utf-8') as f:
            f.write(command.file_info.content)
        return ExecutionResult(success=True, message=f"文件 {command.file_info.filename} 创建成功，内容已写入")
    except Exception as e:
        return ExecutionResult(success=False, message=f"文件创建失败：{str(e)}")

def remove_file(command: Command) -> ExecutionResult:
    """删除文件"""
    print("正在删除文件...")
    try:
        if os.path.exists(command.file_info.filename):
            os.remove(command.file_info.filename)
            return ExecutionResult(success=True, message=f"文件 {command.file_info.filename} 删除成功")
        else:
            return ExecutionResult(success=False, message=f"文件 {command.file_info.filename} 不存在，无法删除")
    except Exception as e:
        return ExecutionResult(success=False, message=f"文件删除失败：{str(e)}")

def read_file(command: Command) -> ExecutionResult:
    """读取文件"""
    print("正在读取文件内容...")
    try:
        if os.path.exists(command.file_info.filename):
            with open(command.file_info.filename, 'r', encoding='utf-8') as f:
                content = f.read()
            return ExecutionResult(success=True, message=f"文件 {command.file_info.filename} 内容如下：\n{content}")
        else:
            return ExecutionResult(success=False, message=f"文件 {command.file_info.filename} 不存在，无法读取")
    except Exception as e:
        return ExecutionResult(success=False, message=f"文件读取失败：{str(e)}")

def rename_file(command: Command) -> ExecutionResult:
    """重命名文件"""
    print("正在重命名文件...")
    try:
        if not command.file_info.new_filename:
            return ExecutionResult(success=False, message="未指定新文件名，无法重命名")
        if os.path.exists(command.file_info.filename):
            os.rename(command.file_info.filename, command.file_info.new_filename)
            return ExecutionResult(success=True, message=f"文件 {command.file_info.filename} 已重命名为 {command.file_info.new_filename}")
        else:
            return ExecutionResult(success=False, message=f"文件 {command.file_info.filename} 不存在，无法重命名")
    except Exception as e:
        return ExecutionResult(success=False, message=f"文件重命名失败：{str(e)}")

def append_file(command: Command) -> ExecutionResult:
    """续写文件"""
    print("正在续写文件...")
    try:
        with open(command.file_info.filename, 'a', encoding='utf-8') as f:
            f.write(command.file_info.content)
        return ExecutionResult(success=True, message=f"内容已追加到文件 {command.file_info.filename}")
    except Exception as e:
        return ExecutionResult(success=False, message=f"文件续写失败：{str(e)}")

def open_website(command: Command) -> ExecutionResult:
    """打开网站"""
    print("正在打开网站...")
    try:
        if not command.file_info.url:
            return ExecutionResult(success=False, message="未指定网址，无法打开网站")
        webbrowser.open(command.file_info.url)
        return ExecutionResult(success=True, message=f"成功打开网站: {command.file_info.url}")
    except Exception as e:
        return ExecutionResult(success=False, message=f"打开网站时出错: {e}")

def open_app(command: Command) -> ExecutionResult:
    """打开App"""
    print(f"正在打开 {command.file_info.url} ...")
    system = platform.system()
    
    try:
        if system == "Windows":
            # Windows 系统：尝试多个可能的安装路径
            app_path = command.file_info.url
            
            if os.path.exists(app_path):
                subprocess.Popen([app_path])
                return ExecutionResult(success=True, message=f"成功打开App: {app_path}")
            else:
                return ExecutionResult(success=False, message="未找到App安装路径，请检查是否安装")
                
        elif system == "Darwin":
            # macOS 系统：通过命令行打开App
            subprocess.Popen(["open", "-a", "NeteaseMusic"])
            return ExecutionResult(success=True, message="成功打开App (macOS)")
            
        elif system == "Linux":
            # Linux 系统：通过命令行启动
            subprocess.Popen(["netease-cloud-music"])
            return ExecutionResult(success=True, message="成功打开App (Linux)")
            
        else:
            return ExecutionResult(success=False, message=f"不支持的操作系统: {system}")
            
    except FileNotFoundError:
        return ExecutionResult(success=False, message="未找到App应用，请检查是否安装")
    except Exception as e:
        return ExecutionResult(success=False, message=f"打开App时出错: {e}")

# 指令执行器映射
COMMAND_EXECUTORS = {
    1: make_file,          # 创建文件
    2: remove_file,        # 删除文件
    3: read_file,          # 读取文件
    4: rename_file,        # 重命名文件
    5: append_file,        # 续写文件
    6: open_website,       # 打开网站
    7: open_app, # 打开App
}

# ================== Agent 定义 ==================
# Commander Agent - 负责指令编排
commander = Agent(
    model=deepseek_model,
    system_prompt="""你是一个指令编排器，负责将用户的复杂请求分解为具体的操作指令。

支持的指令类型编号：
1 = 创建文件
2 = 删除文件  
3 = 读取文件
4 = 重命名文件
5 = 续写文件
6 = 打开网站
7 = 打开App

部分app的url路径详情：
1、网易云音乐: C:/CloudMusic/cloudmusic.exe
2、QQ: D:/QQNT/QQ.exe
3、微信: D:\WeChat\WeChat.exe
4、腾讯会议: D:\腾讯会议\WeMeet\wemeetapp.exe

请将用户请求分解为有序的指令列表，每个指令包含：
1. command_type: 操作类型编号（1-7）
2. file_info: 操作所需的文件信息（filename, content, new_filename, url等）

注意：
- 如果是多步操作，请按执行顺序排列
- 确保每步的file_info信息完整准确
- 重命名操作需要同时提供filename和new_filename
- 打开网站操作需要提供url
- 如果用户指定了写入文件的内容格式，请分析提取真正需要写入的内容
- 如果是打开app请求，请将app的安装路径写入url字段，url可以参照列出的部分url，也有可能由用户给出
- 如果用户只提到了模糊的写入文件内容或者只提了创作要求，请主动进行内容创作，填写到content中去
""",
    output_type=CommandList
)

# ================== 主要处理函数 ==================
async def process_user_request(user_input: str) -> str:
    """处理用户请求的主函数"""
    print(f"用户输入: {user_input}")
    print("=" * 60)
    
    # 第一步：Commander 生成指令列表
    print("Commander 正在分析并生成指令列表...")
    commander_response = await commander.run(user_input)
    command_list = commander_response.output.commands
    
    print(f"Commander 生成了 {len(command_list)} 条指令:")
    print("说明：", commander_response.output.comments)
    
    # 构建执行报告
    report = []
    report.append(f"📋 **执行计划**")
    report.append(f"用户请求：{user_input}")
    report.append(f"生成指令数：{len(command_list)}")
    report.append(f"说明：{commander_response.output.comments}")
    report.append("")
    
    # 显示指令列表
    command_type_names = {
        1: "创建文件", 2: "删除文件", 3: "读取文件", 
        4: "重命名文件", 5: "续写文件", 6: "打开网站", 7: "打开App"
    }
    
    for i, cmd in enumerate(command_list, 1):
        cmd_name = command_type_names.get(cmd.command_type, f"未知指令({cmd.command_type})")
        print(f"  {i}. {cmd_name} -> {cmd.file_info.filename or cmd.file_info.url}")
        report.append(f"**指令 {i}**: {cmd_name} -> `{cmd.file_info.filename or cmd.file_info.url}`")

    print("-" * 40)
    report.append("")
    report.append("📄 **执行结果**")
    
    # 第二步：程序自动执行指令
    success_count = 0
    for i, command in enumerate(command_list, 1):
        cmd_name = command_type_names.get(command.command_type, f"未知指令({command.command_type})")
        print(f"执行第 {i} 条指令: {cmd_name}")
        
        # 获取执行器函数
        executor = COMMAND_EXECUTORS.get(command.command_type)
        if not executor:
            result = ExecutionResult(success=False, message=f"未知的指令类型: {command.command_type}")
        else:
            result = executor(command)
        
        # 记录结果
        status_icon = "✅" if result.success else "❌"
        print(f"  结果: {result.message}")
        print(f"  成功: {result.success}")
        print("-" * 40)
        
        report.append(f"{status_icon} **步骤 {i}**: {cmd_name}")
        report.append(f"   结果: {result.message}")
        report.append("")
        
        if result.success:
            success_count += 1
    
    # 生成总结
    total_commands = len(command_list)
    report.append("📊 **执行总结**")
    report.append(f"- 总指令数: {total_commands}")
    report.append(f"- 成功执行: {success_count}")
    report.append(f"- 失败数量: {total_commands - success_count}")
    report.append(f"- 成功率: {success_count/total_commands*100:.1f}%")
    
    final_report = "\n".join(report)
    print("\n" + "="*60)
    print("最终执行报告:")
    print(final_report)
    
    return final_report

# ================== 测试用例 ==================
if __name__ == "__main__":
    import asyncio
    
    test_cases = [
        # "请创建一个hello.txt文件，内容是'Hello World'",
        # "首先创建文件test.txt，内容是'原始内容'，然后在后面添加'新增内容'，最后重命名为final.txt",
        # "创建demo.txt写入'演示内容'，然后读取文件内容，最后删除该文件",
        # "打开百度网站 https://www.baidu.com",
        "打开网易云音乐"
    ]
    
    async def run_tests():
        for i, test_input in enumerate(test_cases, 1):
            print(f"\n{'='*20} 测试用例 {i} {'='*20}")
            result = await process_user_request(test_input)
            print(f"\n返回结果:\n{result}")
            print("\n" + "="*60)
    
    asyncio.run(run_tests())