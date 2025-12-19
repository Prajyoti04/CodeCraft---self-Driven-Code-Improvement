import requests

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
API_TOKEN = "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"  # Replace with your token
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def fix_code(code_with_bug):
    """
    Attempts to fix bugs in the provided code using AI
    
    Args:
        code_with_bug (str): The buggy code to fix
    Returns:
        str: Fixed code or error message
    """
    try:
        prompt = f"""
Fix bugs in this Python code and explain the fixes:

{code_with_bug}
"""
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 512, 
                "temperature": 0.1,    
                "return_full_text": False,
                "do_sample": False,
                "stop": ["\"\"\"\"", "Explain", "Here's",]
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            fixed_code = response.json()[0]["generated_text"].strip()
            
            if "```" in fixed_code:
                # Split by code blocks and get only code content
                blocks = fixed_code.split("```")
                for block in blocks:
                    # Remove 'python' or 'py' prefix if present
                    clean_block = block.replace("python", "").replace("py", "").strip()
                    # If block contains actual code (not explanations), use it
                    if clean_block and not clean_block.lower().startswith(('here', 'the', 'this', 'fixed')):
                        return clean_block
            
            # If no code blocks found, return the cleaned response
            return fixed_code
        else:
            return f"Error: API returned status code {response.status_code}"
            
    except Exception as e:
        return f"Error fixing code: {str(e)}"

if __name__ == "__main__":
    print("Paste your code below (Ctrl+D or Ctrl+Z to finish):")
    code_lines = []
    
    try:
        while True:
            line = input()
            code_lines.append(line)
    except EOFError:
        code_to_fix = "\n".join(code_lines)
        
    if code_to_fix.strip():
        print("\nAttempting to fix bugs...")
        fixed_code = fix_code(code_to_fix)
        
        print("\nFixed Code:")
        print("-" * 50)
        print(fixed_code)
        print("-" * 50)
        
        save_option = input("\nDo you want to save the fixed code to a file? (y/n): ")
        if save_option.lower() == 'y':
            filename = input("Enter filename (with .py extension): ")
            try:
                with open(filename, 'w') as f:
                    f.write(fixed_code)
                print(f"Fixed code saved to {filename}")
            except Exception as e:
                print(f"Error saving file: {str(e)}")
    else:
        print("No code was provided.")