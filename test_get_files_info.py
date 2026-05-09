from functions.get_files_info import get_files_info

def main():
    print("get_files_info('calculator', '.'):")
    print("Result for current directory:")
    print(get_files_info("calculator", "."))
    print("\n" + "="*30 + "\n")

    print("get_files_info('calculator', 'pkg'):")
    print("Result for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))
    print("\n" + "="*30 + "\n")

    print("get_files_info('calculator', '/bin'):")
    print("Result for '/bin' directory:")
    print(f"    {get_files_info('calculator', '/bin')}")
    print("\n" + "="*30 + "\n")

    print("get_files_info('calculator', '../'):")
    print("Result for '../' directory:")
    print(f"    {get_files_info('calculator', '../')}")

if __name__ == "__main__":
    main()