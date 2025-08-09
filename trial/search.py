import requests

# # SerpAPI,返回的是超多网址
# params = {
#     "q": "哈尔滨工业大学",
#     "api_key": "834d732ee1d1eb0aae581b4b649942dfec4684e1e913d85375a3a9be9ca5a7ee"
# }
# r = requests.get("https://serpapi.com/search", params=params)
# data = r.json()

# results = []
# for item in data.get("organic_results", []):
#     title = item.get("title", "")
#     snippet = item.get("snippet", "")
#     link = item.get("link", "")
#     results.append(f"{title}\n{snippet}\n{link}\n")

# if results:
#     print("SerpAPI 搜索结果：")
#     for res in results:
#         print(res)
# else:
#     print("没有找到相关内容。")

# # DuckDuckGo搜索，信息量极少
# r = requests.get("https://api.duckduckgo.com/?q=哈尔滨工业大学&format=json")
# data = r.json()
# # 提取 RelatedTopics 里的文本和网址
# results = []
# for topic in data.get("RelatedTopics", []):
#     # 有些 RelatedTopics 可能是分组
#     if "Text" in topic and "FirstURL" in topic:
#         results.append(f"{topic['Text']} ({topic['FirstURL']})")
#     elif "Topics" in topic:
#         for subtopic in topic["Topics"]:
#             if "Text" in subtopic and "FirstURL" in subtopic:
#                 results.append(f"{subtopic['Text']} ({subtopic['FirstURL']})")

# # 输出结果
# if results:
#     print("DuckDuckGo 搜索结果：")
#     for item in results:
#         print(item)
# else:
#     print("没有找到相关内容。")

