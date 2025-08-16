import sys

if __name__ == "__main__":
    input_value = sys.argv[1] if len(sys.argv) > 1 else ""
    print(f"main.py收到参数: {input_value}")