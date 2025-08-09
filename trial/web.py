import webbrowser

def open_website(url):
    """
    使用系统默认浏览器打开指定的网站
    
    参数:
        url (str): 要打开的网站URL地址，需包含http://或https://
    """
    try:
        # 打开网站
        webbrowser.open(url)
        print(f"成功打开网站: {url}")
    except Exception as e:
        print(f"打开网站时出错: {e}")

if __name__ == "__main__":
    # 可以替换为你想要打开的任何网站URL
    website_url = "https://www.baidu.com"
    open_website(website_url)
