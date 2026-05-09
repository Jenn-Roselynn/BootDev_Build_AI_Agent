from functions.run_python_file import run_python_file

def main():
    test_cases = [
        # Success cases
        ("calculator", "main.py", None),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py", None),
        # Error cases
        ("calculator", "../main.py", None),
        ("calculator", "nonexistent.py", None),
        ("calculator", "lorem.txt", None),
    ]

    for i, (wdir, fpath, args) in enumerate(test_cases, 1):
        print(f"--- Test Case {i}: {fpath} ---")
        result = run_python_file(wdir, fpath, args)
        print(result)
        print("\n")

if __name__ == "__main__":
    main()