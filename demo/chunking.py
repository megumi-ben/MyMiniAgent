def read_data() -> str:
    with open('do.md', 'r',encoding="utf-8") as file:
        return file.read()

def get_chunks() -> list[str]:
    data = read_data()
    return data.split('\n\n')

if __name__ == "__main__":
    chunks = get_chunks()
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:\n{chunk}")
        print("---" * 10)