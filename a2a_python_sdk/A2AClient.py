import httpx
import json
import uuid
from typing import Dict, Any, Optional

# 自己实现的A2A客户端
class A2AClient:
    def __init__(self, server_url: str):
        # Ensure URL doesn''t end with a slash
        self.url = server_url.rstrip("/")
    
    async def send_task(self, message: str) -> Dict[str, Any]:
        """Send a simple task to the A2A server."""
        task_id = str(uuid.uuid4())
        message_id = str(uuid.uuid4())
        
        # Prepare the JSON-RPC request
        payload = {
            "id": task_id,
            "message": {
                "role": "user",
                "kind": "message",
                "messageId": message_id,
                "parts": [{
                    "text": message,
                    "kind": "text"
                }]
            }
        }
        
        # Send the request
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{self.url}",
                json={
                    "jsonrpc": "2.0",
                    "method": "message/send",
                    "params": payload,
                    "id": 1
                }
            )
            response.raise_for_status()
            result = response.json()
            
            # Return the result
            return result.get("result", {})
    
    async def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a task."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.url}",
                json={
                    "jsonrpc": "2.0",
                    "method": "tasks/get",
                    "params": {"id": task_id},
                    "id": 1
                }
            )
            response.raise_for_status()
            result = response.json()
            
            # Return the result
            return result.get("result", {})