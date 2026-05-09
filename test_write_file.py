from functions.write_file import write_file

def main():
    # Case 1: Overwrite lorem.txt
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    
    # Case 2: Create new file in sub-package
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    
    # Case 3: Unauthorized path
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

if __name__ == "__main__":
    main()