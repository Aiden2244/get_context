import re
import sys

def get_line_number(content, position):
    """
    Find the line number in the file content for a given character position.

    Args:
        content (str): The entire content of the file.
        position (int): The character position within the content to find the line number for.

    Returns:
        int: The line number corresponding to the given position.
    """
    return content.count('\n', 0, position) + 1


def get_list_from_matches(pattern, description_text):
    """
    Generate a list of tuples containing the line number and matched element from the content.

    Args:
        pattern (re.Pattern): Compiled regular expression pattern to search for in the description_text.
        description_text (str): The text to search for pattern matches.

    Returns:
        list: A list of tuples where each tuple contains the line number and the matched element as a string.
    """
    parsed_outputs = []
    
    for match in pattern.finditer(description_text):
        element = match.group(1).strip()
        line_number = get_line_number(description_text, match.start())
        parsed_outputs.append((line_number, element))

    return parsed_outputs


def parse(content):
    """
    Extract lists of commands, test cases, error cases, and context.txt outputs from the content.

    Args:
        content (str): The entire file content to parse.

    Returns:
        tuple: A tuple containing four lists:
            - commands: List of (line number, command) tuples.
            - test_cases: List of (line number, test case label) tuples.
            - error_cases: List of (line number, error case label) tuples.
            - context_outputs: List of (line number, context output) tuples.
    """
    
    # Regular expressions to match commands, test case labels, error cases, and context.txt outputs
    command_pattern = re.compile(r'\*\*Command:\*\*\s*\n```bash\s*\n(.*?)\n```', re.DOTALL)
    test_case_pattern = re.compile(r'## (TEST CASE) (\d+[a-zA-Z])', re.DOTALL)
    error_case_pattern = re.compile(r'## (ERROR CASE) (\d+[a-zA-Z])', re.DOTALL)
    context_output_pattern = re.compile(r'\*\*context\.txt output:\*\*\s*```.*?\n(.*?)\n```', re.DOTALL)

    # Extract matches and associated line numbers
    commands = get_list_from_matches(command_pattern, content)
    test_cases = get_list_from_matches(test_case_pattern, content)
    error_cases = get_list_from_matches(error_case_pattern, content)
    context_outputs = get_list_from_matches(context_output_pattern, content)

    return commands, test_cases, error_cases, context_outputs
    

if __name__ == "__main__":
    """
    Main execution block to read file content from the command line argument, 
    parse the content, and print extracted commands, test cases, error cases, and context outputs.
    """
    file_path = sys.argv[1]

    with open(file_path, 'r') as file:
        content = file.read()

    commands, test_cases, error_cases, context_outputs = parse(content)

    print(f"Commands: {commands}\n")
    print(f"Test cases: {test_cases}\n")
    print(f"Error cases: {error_cases}\n")
    print(f"Context outputs: {context_outputs}\n")
