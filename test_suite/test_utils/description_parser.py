import re
import sys

class DescriptionParser:
    """
    A class to encapsulate logic for parsing command descriptions, test cases, error cases,
    and context outputs from a file's content.
    """
    
    __COMMAND_PATTERN = re.compile(r'\*\*Command:\*\*\s*\n```bash\s*\n(.*?)\n```', re.DOTALL)
    __TEST_CASE_PATTERN = re.compile(r'## (TEST CASE) (\d+[a-zA-Z])', re.DOTALL)
    __ERROR_CASE_PATTERN = re.compile(r'## (ERROR CASE) (\d+[a-zA-Z])', re.DOTALL)
    __CONTEXT_OUTPUT_PATTERN = re.compile(r'\*\*context\.txt output:\*\*\s*```.*?\n(.*?)\n```', re.DOTALL)

    __commands = []
    __test_cases = []
    __error_cases = []
    __context_outputs = []
    __description_text = ""
    
    def __get_line_number(self, position):
        return self.__description_text.count('\n', 0, position) + 1

    def __get_list_from_matches(self, pattern):
        parsed_outputs = []
        
        for match in pattern.finditer(self.__description_text):
            element = match.group(1).strip()
            line_number = self.__get_line_number(match.start())
            parsed_outputs.append((line_number, element))

        return parsed_outputs


    def __init__(self, description_path):
        # read the description text in from the file
        with open(description_path, 'r') as file:
            self.__description_text = file.read()

        self.__commands = self.__get_list_from_matches(self.__COMMAND_PATTERN)
        self.__test_cases = self.__get_list_from_matches(self.__TEST_CASE_PATTERN)
        self.__error_cases = self.__get_list_from_matches(self.__ERROR_CASE_PATTERN)
        self.__context_outputs = self.__get_list_from_matches(self.__CONTEXT_OUTPUT_PATTERN)

    def get_commands(self):
        return self.__commands

    def get_test_cases(self):
        return self.__test_cases

    def get_error_cases(self):
        return self.__error_cases

    def get_context_outputs(self):
        return self.__context_outputs

if __name__ == "__main__":
    """
    Main execution block to read file description text from the command line argument,
    parse the description text, and print extracted commands, test cases, error cases, and context outputs.
    """
    file_path = sys.argv[1]

    parser = DescriptionParser(file_path)

    print(f"Commands: {parser.get_commands()}\n")
    print(f"Test cases: {parser.get_test_cases()}\n")
    print(f"Error cases: {parser.get_error_cases()}\n")
    print(f"Context outputs: {parser.get_context_outputs()}\n")
