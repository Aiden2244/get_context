import subprocess
import sys
import os
from parse_description import parse_description

def run_command(command_list):
    try:
        # Run the command and print output if success
        result = subprocess.run(command_list, check=True, capture_output=True, text=True)
        print(f"Command '{' '.join(command_list)}' executed successfully.")
        print("\nConsole Output:")
        print(result.stdout)
        print("Contents of context.txt: \n")
        print("v" * 30 + "\n")
        print(get_context_output_as_string())
        print("^" * 30 + "\n")
    except subprocess.CalledProcessError as e:
        # Print the error but continue to the next command
        print(f"Error executing command: {' '.join(command_list)}")
        print("\nError message: ")
        print(f"{e.stdout}")


def get_context_output_as_string(directory='.'):
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

    combined_list = parse_description(content)

    for item in combined_list:
        if item[0] in ["TEST CASE", "ERROR CASE"]:
            print("*" * 50 + "\n")
            print("*" * 50 + "\n")
            print(f"{' '.join(item)}")
        else:
            # Otherwise, treat it as a command and run it
            print(f"Running command: {' '.join(item)}")
            run_command(item)
            print()
    
    file.close()

if __name__ == "__main__":
    main()