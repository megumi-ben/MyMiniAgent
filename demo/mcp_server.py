from mcp.server.fastmcp import FastMCP

app = FastMCP(
    name="ben-mcp",  # 好像没有什么用
    port=9800,  # 默认是8000
    streamable_http_path="/dodo" # 默认是/mcp，url中的路径
)

@app.tool()
def get_string() -> str:
    return "我是哈尔滨工业大学的学生，我叫张三，学号是123456。"

if __name__ == '__main__':
    app.run(transport='streamable-http') # 使用流式http方式