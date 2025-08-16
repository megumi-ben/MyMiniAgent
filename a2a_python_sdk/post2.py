import requests
import json
from uuid import uuid4
import time

# 配合自己pydantic_ai提供的构建A2A服务端的方法进行请求，相当于client去post
# 本质上是调ASGI服务，请求参数满足A2A协议规范即可
url = 'http://localhost:9999/'  # 替换为你的实际地址

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
        {"kind": "text", "text": "你好"}
      ]
    }
  },
  "id": 1
}

print(json.dumps(data, ensure_ascii=False, indent=2))
with requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"}) as resp:
    resp_json = resp.json()
    print(json.dumps(resp_json, ensure_ascii=False, indent=2))

task_id = None
# 解析任务ID
if "result" in resp_json and "id" in resp_json["result"]:
    task_id = resp_json["result"]["id"]

if task_id:
    # 轮询获取AI回复
    for _ in range(20):
        time.sleep(1)
        get_data = {
            "jsonrpc": "2.0",
            "method": "tasks/get",
            "params": {"id": task_id},
            "id": 2
        }
        r = requests.post(url, data=json.dumps(get_data), headers={"Content-Type": "application/json"})
        result = r.json()
        # print(json.dumps(result, ensure_ascii=False, indent=2))
        # 检查是否有AI回复
        history = result.get("result", {}).get("history", [])
        for msg in history:
            if msg.get("role") == "agent":
                print("AI回复：", msg["parts"][0].get("text"))
                exit()