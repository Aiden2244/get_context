import subprocess
import sys
import os
from parse_description import parse

def run_command(command_list, context_output_from_list):
    try:
        # Run the command and print output if success
        result = subprocess.run(command_list, check=True, capture_output=True, text=True)
        print(f"Command '{' '.join(command_list)}' EXECUTED SUCCESSFULLY.")
        print("\nConsole Output:")
        print(result.stdout)

        # print("Contents of context.txt FROM TEST:\n")
        # print("v" * 30 + "\n")
        # print(get_context_output_from_test())
        # print("^" * 30 + "\n")

        # print(f"Contents of context.txt FROM LIST (output index {output_index}):\n")
        # print("v" * 30 + "\n")
        # print(context_output_from_list)
        # print("^" * 30 + "\n")

        result = "PASS" if get_context_output_from_test().strip() == context_output_from_list.strip() else "FAIL"
        print(f"\nTEST RESULT: {result}")

        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR EXECUTING COMMAND: {' '.join(command_list)}")
        print("\nConsole output: ")
        print(f"{e.stdout}")
        print("\nError message: ")
        print(f"{e.stderr if not e.stderr == "" else "No error message"}")

        return False


def get_context_output_from_test(directory='.'):
    context_file_path = os.path.join(directory, 'context.txt')

    # Check if the context.txt file exists
    if os.path.exists(context_file_path):
        # Read the contents of the file and return it
        with open(context_file_path, 'r') as file:
            return file.read()
    else:
        # File not found, return None
        return None


def main():
    # Ensure a markdown file is provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py <description_file>")
        sys.exit(1)

    description_file = sys.argv[1]
    with open(description_file, 'r') as file:
        content = file.read()

    combined_list, context_output_list = parse(content)

    output_index = 0
    for item in combined_list:
        if item[0] in ["TEST CASE", "ERROR CASE"]:
            print("*" * 50 + "\n")
            print("*" * 50 + "\n")
            print(f"{' '.join(item)}")
        else:
            print("-----")
            print(f"Running command: {' '.join(item)}")
            success = run_command(item, context_output_list[output_index])
            if success: output_index += 1
            output_index = min(output_index, len(context_output_list)-1)
            print()
    
    file.close()

if __name__ == "__main__":
    main()