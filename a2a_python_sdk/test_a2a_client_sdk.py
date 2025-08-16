
from uuid import uuid4
import httpx
from a2a.client import A2ACardResolver, ClientFactory
from a2a.client.client import ClientConfig
from a2a.types import AgentCard

# 使用A2A Python SDK，可以直接构造Client，下面是测试代码
async def main() -> None:

    async with httpx.AsyncClient() as httpx_client:
        # 初始化A2ACardResolver
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url='http://localhost:9999',
        )

        # 获取公共Agent Card并初始化客户端
        final_agent_card_to_use: AgentCard | None = await resolver.get_agent_card()
        client = ClientFactory(ClientConfig(httpx_client=httpx_client)).create(
            card=final_agent_card_to_use
        )
        
        payload = {
            'role': 'user',
            'parts': [
                {'kind': 'text', 'text': 'how much is 10 USD in INR?'}
            ],
            'messageId': uuid4().hex,
        }

        async for response in client.send_message(payload):
            print(response.model_dump_json())
            print(response.parts[0].root.text)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
