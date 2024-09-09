import os

def read_test_commands(file_path):
    """
    Read test_commands.txt and return case number, test commands, and error commands.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    case_number = lines[0].strip()  # The case number is on the first line
    test_commands = []
    error_commands = []

    # Reading test and error commands
    in_test_section = True
    for line in lines[1:]:
        line = line.strip()
        if not line:  # Empty line indicates switch to error cases
            in_test_section = False
            continue

        commands = [cmd.strip() for cmd in line.split(',')]
        if in_test_section:
            test_commands.append(commands)
        else:
            error_commands.append(commands)

    return case_number, test_commands, error_commands

def generate_description(case_number, test_commands, error_commands, output_path):
    """
    Generate a DESCRIPTION file based on the given commands.
    """
    # Start writing the description content
    description_content = []

    # Write the TEST CASES section
    description_content.append(f"# CASE {case_number} OVERVIEW")
    description_content.append("[case description]  # Human editable section\n- [case details here]\n")
    description_content.append("# TEST CASES")
    description_content.append("The following test cases should result in successful output, corresponding with the defined behavior for the program.\n")

    test_case_index = 'a'
    for commands in test_commands:
        description_content.append(f"## TEST CASE {case_number}{test_case_index}")
        description_content.append("This test case should be run [how]\n")
        description_content.append("[this tests]  # Human editable section\n- [list test conditions here]\n")
        description_content.append("A successful test result should [do what]  # Human editable section\n")
        for command in commands:
            description_content.append(f"**Command:**\n```bash\n{command}\n```")
            description_content.append("**Console output:**\n```bash\n[console output here]\n```")
            description_content.append("**context.txt output:**\n```\n[context output here]\n```\n")
        test_case_index = chr(ord(test_case_index) + 1)  # Increment 'a' -> 'b' -> 'c'

    # Write the ERROR CASES section
    description_content.append("# ERROR CASES")
    description_content.append("The following test cases should NOT result in successful output. These tests demonstrate how the program handles errors or undefined inputs under various conditions.\n")

    error_case_index = 'a'
    for commands in error_commands:
        description_content.append(f"## ERROR CASE {case_number}{error_case_index}")
        description_content.append("This test case should be run [how]\n")
        description_content.append("[this tests]  # Human editable section\n- [list test conditions here]\n")
        description_content.append("This should result in [what]  # Human editable section\n")
        for command in commands:
            description_content.append(f"**Command:**\n```bash\n{command}\n```")
            description_content.append("**Console output:**\n```bash\n[console output here]\n```")
        error_case_index = chr(ord(error_case_index) + 1)  # Increment 'a' -> 'b' -> 'c'

    # Write the generated content to the DESCRIPTION file
    with open(output_path, 'w') as file:
        file.write('\n'.join(description_content))

    print(f"DESCRIPTION file generated at: {output_path}")

def main():
    # Get the path to test_commands.txt and read it
    test_commands_path = input("Enter the path to test_commands.txt: ").strip()
    case_directory = os.path.dirname(test_commands_path)
    description_output_path = os.path.join(case_directory, 'DESCRIPTION')

    # Read the test commands and error commands
    case_number, test_commands, error_commands = read_test_commands(test_commands_path)

    # Generate the DESCRIPTION file
    generate_description(case_number, test_commands, error_commands, description_output_path)

if __name__ == "__main__":
    main()
