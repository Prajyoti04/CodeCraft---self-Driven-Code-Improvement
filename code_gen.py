import requests

def generate_code(prompt):
    """
    Generate code using Hugging Face's free code generation model
    
    Args:
        prompt (str): Description of the code you want to generate
        
    Returns:
        str: Generated code
    """
    try:
        # Using Hugging Face API (get your free token from huggingface.co)
        API_TOKEN = "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"
        API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
        
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        payload = {
            "inputs": f"# Python code to {prompt}\n\n",
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.7,
                "return_full_text": False
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            generated_code = response.json()[0]["generated_text"]
            return generated_code
        else:
            return f"Error: API returned status code {response.status_code}"
        
    except Exception as e:
        return f"Error generating code: {str(e)}"

def save_generated_code(code, filename):
    """
    Save the generated code to a file
    
    Args:
        code (str): Generated code to save
        filename (str): Name of the file to save the code to
    """
    try:
        with open(filename, 'w') as f:
            f.write(code)
        print(f"Code successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving code: {str(e)}")

if __name__ == "__main__":
    # Example usage
    prompt = input("Enter what you want the code to do: ")
    generated_code = generate_code(prompt)
    
    print("\nGenerated Code:")
    print("-" * 50)
    print(generated_code)
    print("-" * 50)
    
    # Option to save the code
    save_option = input("\nDo you want to save this code to a file? (y/n): ")
    if save_option.lower() == 'y':
        filename = input("Enter filename (with .py extension): ")
        save_generated_code(generated_code, filename)
