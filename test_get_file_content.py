from functions.get_file_content import get_file_content
from config import MAX_CHARS

def main():
    # 1. Test Truncation
    print("Testing Truncation (lorem.txt):")
    lorem_content = get_file_content("calculator", "lorem.txt")
    print(f"Content length: {len(lorem_content)}")
    if "truncated" in lorem_content:
        print("Success: Truncation message found.")
    else:
        print("Failure: Truncation message NOT found.")
    print("\n" + "="*30 + "\n")

    # 2. Test Success Cases
    print("get_file_content('calculator', 'main.py'):")
    print(get_file_content("calculator", "main.py"))
    print("\n" + "="*30 + "\n")

    print("get_file_content('calculator', 'pkg/calculator.py'):")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print("\n" + "="*30 + "\n")

    # 3. Test Error Cases
    print("get_file_content('calculator', '/bin/cat'):")
    print(get_file_content("calculator", "/bin/cat"))
    print("\n" + "="*30 + "\n")

    print("get_file_content('calculator', 'pkg/does_not_exist.py'):")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    main()