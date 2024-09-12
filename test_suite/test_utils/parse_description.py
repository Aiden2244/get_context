import re
import sys

def get_line_number(content, position):
    """Helper function to find the line number given a position in the file content."""
    return content.count('\n', 0, position) + 1

def parse(content):
    """Extracts both commands and test case labels from the content."""
    combined_list = []
    context_output_list = []

    # Regular expression to match commands, test case labels, and output
    command_pattern = re.compile(r'\*\*Command:\*\*\s*\n```bash\s*\n(.*?)\n```', re.DOTALL)
    test_case_pattern = re.compile(r'## (TEST CASE) (\d+[a-zA-Z])', re.DOTALL)
    error_case_pattern = re.compile(r'## (ERROR CASE) (\d+[a-zA-Z])', re.DOTALL)
    context_output_pattern = re.compile(r'\*\*context\.txt output:\*\*\s*```.*?\n(.*?)\n```', re.DOTALL)

    # Extract commands
    for match in command_pattern.finditer(content):
        command = match.group(1).strip().split()  # Tokenize the command
        line_number = get_line_number(content, match.start())  # Get line number
        combined_list.append((line_number, command))

    # Extract test case labels
    for match in test_case_pattern.finditer(content):
        case_type = match.group(1)
        case_label = match.group(2)
        line_number = get_line_number(content, match.start())  # Get line number
        combined_list.append((line_number, [case_type, case_label]))

    # Extract context.txt outputs
    for match in context_output_pattern.finditer(content):
        context_output = match.group(1).strip()  # Get the entire context.txt output as a string
        context_output_list.append(context_output)

    # Sort the combined list by line number and return the lists
    sorted_combined_list = [content for _, content in sorted(combined_list, key=lambda x: x[0])]

    return sorted_combined_list, context_output_list

if __name__ == "__main__":
    file_path = sys.argv[1]

    with open(file_path, 'r') as file:
        content = file.read()

    combined_list, context_output_list = parse(content)

    print("Combined List:")
    for item in combined_list:
        print(item)

    print("\nContext.txt Output List:")
    for i in range(len(context_output_list)):
        print(f"\n\ncontext.txt output {i}: ")
        print(context_output_list[i])
