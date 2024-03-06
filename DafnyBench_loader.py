import os
import re

def remove_last_two_lines(s):
    """
    Removes the last two lines from a multiline string.
    
    Parameters:
    - s (str): The original multiline string.
    
    Returns:
    - str: The modified string with the last two lines removed.
    """
    # Split the string into lines
    lines = s.split('\n')
    
    # Remove the last two lines
    # If there are less than two lines, this will result in an empty list
    modified_lines = lines[:-2] if len(lines) > 2 else []
    
    # Join the remaining lines back into a single string
    modified_string = '\n'.join(modified_lines)
    
    return modified_string

def remove_method_and_following(s, method_name="MethodName"):
    """
    Removes "method MethodName" and everything that follows it from the string.

    Parameters:
    - s (str): The original string.
    - method_name (str): The specific method name to look for. Defaults to "MethodName".

    Returns:
    - str: The modified string with "method MethodName" and everything after it removed.
    """
    # Define the pattern to search for
    # If method_name can vary and is not just "MethodName", adjust the pattern accordingly
    pattern = f"method {re.escape(method_name)}.*"

    # Use re.sub() to replace the pattern and everything that follows it with an empty string
    # Flags used: re.DOTALL to make . match any character including newline
    modified_string = re.sub(pattern, "", s, flags=re.DOTALL)

    return modified_string

def extract_function_definition(s):
    """
    Extracts the function definition part of the string that precedes the '/* TODO */' comment.

    Parameters:
    - s (str): The original string containing the function definition and other content.

    Returns:
    - str: The extracted function definition part of the string.
    """
    # Define the pattern to search for. This pattern looks for the least greedy match up to an opening brace '{'
    # followed by any characters until the '/* TODO */' comment.
    pattern = r"^(.*?\{).*?/\* TODO \*/"

    # Use re.search() to find the match. The DOTALL flag allows '.' to match newline characters as well.
    match = re.search(pattern, s, flags=re.DOTALL)

    if match:
        # Extract and return the matched part, which is the function definition up to the opening brace
        return match.group(1)
    else:
        # If there is no match (which should not happen given your input but is good practice to check), return an empty string or appropriate message
        return ""

def dfy_annotation_iterator(base_path="DafnyBench/tasks/fill_body/"):
    # Walk through all subdirectories of the given base path
    for root, dirs, files in os.walk(base_path):
        # Filter and process only files that end with '_fillbody.dfy'
        for file in files:
            if file.endswith('_fillbody.dfy'):
                method_name = file.split('_fillbody.dfy')[0]
                file_path = os.path.join(root, file)
                # Open and read the content of the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    #content = remove_last_two_lines(content)
                    #content = remove_method_and_following(content, method_name=method_name) # remove the target method
                    content = f"/* Spec: Fill in the TODO sections of the Dafny code below. Here's the skeleton.*/\n```dafny\n" + content + f"```\nOkay now it is your turn:\n```dafny\n{extract_function_definition(content)}"
                    # Clean whitespace from end of prompt:
                    content = content.rstrip() + "\n\t"
                    # Yield the content of the file
                    yield method_name, content
    
if __name__ == "__main__":
    print(next(dfy_annotation_iterator())[0])
    print(next(dfy_annotation_iterator())[1])
