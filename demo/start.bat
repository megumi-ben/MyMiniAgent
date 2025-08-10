@echo off

echo 启动mcp_server.py...
start "" python mcp_server.py

echo 等待2秒...
timeout /t 2 /nobreak >nul

echo 启动uvicorn服务...
start "" uvicorn agui_agent:app --reload --port 8000

echo 等待2秒...
timeout /t 2 /nobreak >nul

echo 打开chat.html...
start "" chat.html

echo 所有服务已启动