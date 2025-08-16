import asyncio
from A2AClient import A2AClient

# 测试自己搭建的A2AClient
async def main():
    # Replace with your A2A server URL
    client = A2AClient("http://localhost:9999")

    try:
        # Send a task
        print("Sending task to A2A server...")
        task = await client.send_task("你有什么用啊？")
        print(task)
        
        print(f"Task ID: {task.get('id')}")
        print(f"Task status: {task.get('status', {}).get('state')}")
        print(task["parts"][0]["text"])
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())