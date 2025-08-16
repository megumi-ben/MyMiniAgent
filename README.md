# MyMiniAgent

## 库功能

- 自定义响应格式(output_type)
- 调用自定义tool方法(注解 or 属性添加)
- 通用的大模型调用方式(api key, url, model)
- 一键获取上下文(all_messages免去手动记录上下文)
- 可以使用Field给自定义class的属性写注释指导ai思考
- API KEY最好放置在.env而不是直接编码进代码中

## 新版注意

1. 参数名result_type改为output_type；
2. 返回值不再是result.data而是result.output，output本身是BaseModel类型

## 进阶

### 使用依赖数据

实例化Agent时指定deps_type，后续对话时给deps参数传入对应类型的实例即可传入依赖数据，但是得结合tool来使用而不能单单作为输入数据，常用场景是作为tool方法的输入参数其中的deps属性类型。
由于deps_type只允许一种类型，所以对于含有多个tool方法的agent来说，可能每个tool方法的参数类型都不一样。这种情况下，一种思路是使用复合类型结构体包装所有可能的类型，或者使用Union。

### 指定tool方法

方法一：方注释@agent.tool,格式是@你的Agent实例名.tool;(tool方法定义在Agent实例化之前)
方法二：实例化Agent时定义tools属性，tools=[方法1,方法2,方法3]。(tool方法定义在Agent实例化之后)

## 痛点

大模型指导agent调用tool方法不够灵活，需要用户每次手动给出deps参数作为tool方法的参数，而不能大模型自主从用户文本输入中提取关键信息自动填充tool方法的参数。
解决办法：做agent二次封装（ai调ai）。具体来讲，一个ai在分析用户输入后给出格式化输出作为第二个ai的deps生成器方法的依据，然后第二个ai再去调用tool方法。其实另外一种思路是只使用一个ai来做，但是对于一次用户输入会实际会产生两轮对话，第一轮用于指令编排生成相应的deps实例，第二轮才是真正的调用服务。但是这样两轮对话是固定的，只能执行一次操作就结束了，对于用户输入中可能要求连续操作的场景支撑不足（多轮操作只能硬编码轮次到代码中去，非常不灵活）。

正则解析对输入文本要求高，不考虑。

其实如果全部工具都是本地tool方法，就没有必要两个agent了，直接一个指令编排器就行，剩下的可以由程序逻辑自动化完成。类似function_calling，模型只负责请求调用，真正执行方法是本地逻辑处理的。

## pydentic_ai 写的 agent 调用 mcp 服务

直接写tool方法适合本地，但实际上很多情况下都是外置的工具，所以要调 MCP 服务。这里使用pydentic_ai库实现的agent结合官方mcp库实现的mcp server来实现mcp服务的调用，更多详细信息可以看 [官方文档](https://ai.pydantic.dev/mcp/client/)。

有http、sse、stdio等方式去实现mcp client，这里只介绍最简单的http。

mcp server实现：

```python
from mcp.server.fastmcp import FastMCP

app = FastMCP(
    name="ben-mcp",  # 好像没有什么用
    port=9800,  # 默认是8000
    streamable_http_path="/dodo" # 默认是/mcp，url中的路径
)

@app.tool()
def get_string() -> str:
    return "我是哈尔滨工业大学的学生，我叫张三，学号是123456。"

if __name__ == '__main__':
    app.run(transport='streamable-http') # 使用流式http方式
```

mcp client实现：

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

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
        result = await agent.run('调用tool获取信息')
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
```

在client程序入口处加三行代码即可视化对话，在此之前先 `logfire auth` 认证一下。

```python
import logfire
logfire.configure()
logfire.instrument_pydantic_ai()
```

## 手写 RAG 个人知识库

参考google官方embeding模型：[gemini-api](https://ai.google.dev/gemini-api/docs/embeddings)

代码见chunking.py以及rag_agent.py

## 前端搭建

利用AG_UI协议（智能体用户交互协议），定义好后端接口，接收post请求返回流式响应。

运行：

>uvicorn agui_agent:app --reload --port 8000

加了reload参数就可以自动重载，修改代码后无需重新启动。

## 注意事项

- 记得自己在demo目录下创建.env文件写入你的api key；
- 如果使用个人知识库先使用embeding.py进行搭建，谷歌的genai是需要科学上网的；

## A2A

a2a中有两种重要角色，一类是作为a2a客户端的agent，一类是作为a2a服务端的agent，它们之间通过a2a协议进行通信，a2a协议规范了agent和agent之间的通信问题。
pydantic_ai文档（直接构造A2A服务器）：[pydantic_ai A2A](https://ai.pydantic.org.cn/a2a/)
官方网址：[a2aprotocol.org](https://www.a2aprotocol.org/zh)
开始使用A2A（官方）：[start A2A](https://www.a2aprotocol.org/zh/tutorials/getting-started)
自己实现A2A（官方）：[官方实现A2A教程](https://www.a2aprotocol.org/zh/tutorials/implementing-a2a-in-your-application)
爱好者网站(含python sdk教程，比官方直观)：[a2aprotocol.net](https://www.a2aprotocol.net/zh)
A2A python SDK(非官方，总结版)：[net](https://www.a2aprotocol.net/zh/docs/a2a-python-sdk-basic)
A2A python SDK(官方)：[org](https://a2a-protocol.org/latest/tutorials/python/1-introduction/)
