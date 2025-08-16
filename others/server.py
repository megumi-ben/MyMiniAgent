from mcp.server.fastmcp import FastMCP
import requests
import json

app = FastMCP(
    name="ben-mcp",  # 好像没有什么用
    port=9800,  # 默认是8000
    streamable_http_path="/dodo" # 默认是/mcp，url中的路径
)

@app.tool()
def get_string() -> str:
    """获取个人信息，先调用该方法再调用gen_key"""
    return "我是哈尔滨工业大学的学生，我叫张三，学号是123456。"

@app.tool()
def gen_key(name: str, sid: str, school: str) -> str:
    """生成唯一标识符,格式为: {学号}_{姓名}_{学校},前置条件是先调用get_string获取信息"""
    return f"{sid}_{name}_{school}"

@app.tool()
def static_anime_info() -> str:
    """获取静态动漫信息,调用get_character的前置条件"""
    return "查询的人物name是[yuigahama yui]，page=1"

@app.tool()
def get_character(name: str, page: int) -> str:
    """
    获取角色信息,调用static_anime_info是调用该函数的前置条件,
    其中name是角色的名字，page是页码
    """
    url = "https://animedb1.p.rapidapi.com/characters"
    querystring = {"q": name, "page": page}

    headers = {
        "x-rapidapi-key": "233ac3bb36mshcc33feefaa6dba5p1df36cjsn5ccbf45c3865",
        "x-rapidapi-host": "animedb1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return json.dumps(response.json(), indent=2)

if __name__ == '__main__':
    app.run(transport='streamable-http') # 使用流式http方式