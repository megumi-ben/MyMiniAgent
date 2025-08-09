import requests
import json

 
url = 'http://localhost:8000/'  # 替换为你的实际地址
 
data = {
    "threadId": "thread-1",
    "runId": "run-1",
    "state": {},
    "tools": [],
    "context": [],
    "forwardedProps": {},
    "messages": [
        {
            "role": "user",
            "id": "314344",
            "content": "你好"
        }
    ]
}
 
print(json.dumps(data, ensure_ascii=False, indent=2))
with requests.post(url, data=json.dumps(data), stream=True) as resp:
    for line in resp.iter_lines():
        if line:
            try:
                print(line.decode('utf-8'))
            except Exception:
                print(line)