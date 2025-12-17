def main(content: str):
    pass

if __name__ == "__main__":
    with open("./example-input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())
