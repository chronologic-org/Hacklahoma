import re

def extract_code_blocks(text):
    """
    Extracts code blocks enclosed in triple backticks from the given text.
    
    :param text: str, input text containing code blocks
    :return: list of extracted code blocks
    """
    pattern = r'```(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches

# Example usage
if __name__ == "__main__":
    sample_text = """
    Here is some text.
    ```python
    def hello():
        print("Hello, world!")
    ```
    More text here.
    ```
    SELECT * FROM users;
    ```
    """
    
    extracted_codes = extract_code_blocks(sample_text)
    for i, code in enumerate(extracted_codes, 1):
        print(f"Code Block {i}:")
        print(code.strip())
        print("-" * 20)
