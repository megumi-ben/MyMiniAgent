import requests
import json
import asyncio

async def search_bocha(query):
    url = "https://api.bochaai.com/v1/web-search"
    payload = json.dumps({
        "query": query,
        "summary": True,
        "count": 10
    })
    headers = {
        'Authorization': 'Bearer sk-40229496e6654f728f48d394e6dd66f1',
        'Content-Type': 'application/json'
    }
    print(f"\n\n\n\n\n请求URL: {url}\n\n\n\n\n\n")
    response = requests.request("POST", url, headers=headers, data=payload)
    data =  response.json()
    results = []
    for item in data.get('data', {}).get('webPages', {}).get('value', []):
        title = item.get('name', '')
        summary = item.get('summary', '') or item.get('snippet', '')
        url = item.get('url', '')
        site = item.get('siteName', '')
        results.append(f"**{title}**\n{summary}\n来源：[{site}]({url})\n")
    if results:
        return "博查搜索结果：\n" + "\n".join(results)
    else:
        return "没有找到相关内容。"
    
if __name__ == "__main__":
    result = asyncio.run(search_bocha("GPT5发布时间"))
    print(result)