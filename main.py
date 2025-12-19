import sys
import ast
import traceback
from typing import Any, Optional
import requests

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.code = []
    
    def add_line(self, line: str):
        self.code.append("    " * self.indent_level + line)
    
    def indent(self):
        self.indent_level += 1
    
    def dedent(self):
        self.indent_level -= 1
    
    def get_code(self) -> str:
        return "\n".join(self.code)

class Debugger:
    def __init__(self):
        self.breakpoints = set()
        
    def set_breakpoint(self, filename: str, line: int):
        self.breakpoints.add((filename, line))
    
    def remove_breakpoint(self, filename: str, line: int):
        self.breakpoints.discard((filename, line))
        
    def debug(self, code: str):
        try:
            # Parse code into AST
            tree = ast.parse(code)
            
            # Add debugging statements
            for node in ast.walk(tree):
                if isinstance(node, ast.stmt):
                    lineno = getattr(node, 'lineno', None)
                    if (lineno is not None and 
                        ('debug.py', lineno) in self.breakpoints):
                        # Insert breakpoint
                        breakpoint()
            
            # Execute modified code
            exec(compile(tree, 'debug.py', 'exec'))
        except Exception as e:
            print("Error occurred during debugging:")
            print(traceback.format_exc())
            
class AICodeGenerator:
    def __init__(self):
        # Using the base starcoder model
        self.API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
        self.headers = {
            "Authorization": f"Bearer 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",  # Replace with your actual token
            "Content-Type": "application/json"
        }

    def generate_code(self, prompt: str) -> str:
        try:
            payload = {
                "inputs": f"// Write Python code for {prompt}\n",
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.2,  # Lower temperature for more focused output
                    "top_k": 50,
                    "top_p": 0.9,
                    "do_sample": True,
                    "num_return_sequences": 1,
                    "stop": ["```"]  # Stop generation at code block end
                }
            }
            
            response = requests.post(
                self.API_URL, 
                headers=self.headers, 
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Debug - Status Code: {response.status_code}")
                print(f"Debug - Response: {response.text}")
                return f"Error: API returned status code {response.status_code}"
            
            result = response.json()
            if isinstance(result, list) and result:
                generated_code = result[0].get('generated_text', '').strip()
                # Clean up the output
                if '```python' in generated_code:
                    generated_code = generated_code.split('```python')[1].split('```')[0]
                return generated_code
            
            return "Error: Invalid response format"
            
        except Exception as e:
            print(f"Debug - Exception: {str(e)}")
            return f"Error generating code: {str(e)}"
    
    def debug_code(self, prompt: str) -> str:
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.API_URL, 
                headers=self.headers, 
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()[0]["generated_text"].strip()
        except requests.exceptions.RequestException as e:
            return f"Error with API request: {str(e)}"
        except Exception as e:
            return f"Error analyzing code: {str(e)}"

def ask_question():
    # Initialize AI Code Generator (no API key needed)
    ai_gen = AICodeGenerator()
    while True:

        print("\n Enter your programming question (or 'Quit' to exit);")
        question = input(">>")

        if question.lower() in ['quit', 'exit', 'q']:
            break

        print("\nGenerating response.....")
        responce = ai_gen.generate_code(question)
        print("\nGenerated code:")
        print("-" * 50)
        print(responce)
        print("-" * 50)


