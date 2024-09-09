import re
import sys

def get_line_number(content, position):
    return content.count('\n', 0, position) + 1

def parse_description(content):
    combined_list = []

    # Regular expressions to match commands and test case labels
    command_pattern = re.compile(r'\*\*Command:\*\*\s*\n```bash\s*\n(.*?)\n```', re.DOTALL)
    case_pattern = re.compile(r'## (TEST CASE|ERROR CASE) (\d+[a-zA-Z])', re.DOTALL)

    # Extract commands
    for match in command_pattern.finditer(content):
        command = match.group(1).strip().split()  # Tokenize the command
        line_number = get_line_number(content, match.start())  # Get line number
        combined_list.append((line_number, command))

    # Extract test case labels
    for match in case_pattern.finditer(content):
        case_type = match.group(1)
        case_label = match.group(2)
        line_number = get_line_number(content, match.start())  # Get line number
        combined_list.append((line_number, [case_type, case_label]))

    # Sort the combined list by line number and return only the content (without line numbers)
    return [content for _, content in sorted(combined_list, key=lambda x: x[0])]

if __name__ == "__main__":
    # Read file content once
    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract and combine the commands and test cases
    combined = parse_description(content)

    # Print the combined list
    print("\nCombined List:")
    for entry in combined:
        print(entry)