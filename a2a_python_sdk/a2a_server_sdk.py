from agent_executor import (
    HelloWorldAgentExecutor
)

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore  # 用于任务状态管理
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

# 使用A2A Python SDK，搭建A2A Server
if __name__ == '__main__':
    # 1. 定义技能
    skill = AgentSkill(
        id='hello_world',
        name='Returns hello world',
        description='just returns hello world',
        tags=['hello world'],
        examples=['hi', 'hello world'],
    )
    
    # 2. 定义智能体名片
    agent_card = AgentCard(
        name='Hello World Agent',
        description='Just a hello world agent',
        url='http://localhost:9999/',
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )
    
    # 3. 定义请求处理器
    request_handler = DefaultRequestHandler(
        agent_executor=HelloWorldAgentExecutor(),
        task_store=InMemoryTaskStore(),  # 用于任务状态管理
    )

    # 4. 构建服务器
    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    

    # 5. 使用 Uvicorn 启动服务器
    import uvicorn
    uvicorn.run(server.build(), host='0.0.0.0', port=9999)