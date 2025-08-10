echo 开始安装项目依赖...

:: 检查requirements.txt是否存在
if not exist "requirements.txt" (
    echo 错误：未找到requirements.txt文件
    pause
    exit /b 1
)

:: 安装依赖
pip install -r requirements.txt

:: 检查安装是否成功
if %errorlevel% equ 0 (
    echo 依赖安装完成
) else (
    echo 依赖安装失败
    pause
    exit /b 1
)