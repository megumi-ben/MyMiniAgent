from mcp.server.fastmcp import FastMCP
import requests
import json
from uuid import uuid4
import time

app = FastMCP(
    name="ben-mcp",  # 好像没有什么用
    port=9800,  # 默认是8000
    streamable_http_path="/dodo" # 默认是/mcp，url中的路径
)

@app.tool()
def get_string() -> str:
    return "我是哈尔滨工业大学的学生，我叫张三，学号是123456。"

@app.tool()
def ask_a2a_agent(question: str) -> str:
    """调用A2A agent并返回最终AI回复，如果涉及a2a，必须调用该方法"""
    url = 'http://localhost:9999/'
    data = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "id": uuid4().hex,
            "message": {
                "role": "user",
                "kind": "message",
                "messageId": uuid4().hex,
                "parts": [
                    {"kind": "text", "text": question}
                ]
            }
        },
        "id": 1
    }
    try:
        resp = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        resp_json = resp.json()
        task_id = resp_json.get("result", {}).get("id")
        if not task_id:
            return "无法获取任务ID，A2A agent响应异常。"
        # 轮询获取AI回复
        for _ in range(30):
            time.sleep(1)
            get_data = {
                "jsonrpc": "2.0",
                "method": "tasks/get",
                "params": {"id": task_id},
                "id": 2
            }
            r = requests.post(url, data=json.dumps(get_data), headers={"Content-Type": "application/json"})
            result = r.json()
            history = result.get("result", {}).get("history", [])
            for msg in history:
                if msg.get("role") == "agent":
                    return msg["parts"][0].get("text", "（无文本内容）")
        return "未能在规定时间内获得AI回复。"
    except Exception as e:
        return f"调用A2A agent出错：{e}"

if __name__ == '__main__':
    app.run(transport='streamable-http') # 使用流式http方式