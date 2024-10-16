import pandas as pd
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the code examples dataset
def load_code_data(filename='code_examples.csv'):
    try:
        data = pd.read_csv(filename)
        print(f"Loaded {len(data)} code examples from {filename}")
        return data
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None

# Initialize GPT-2 model and tokenizer for code
def load_model():
    print("Loading GPT-2 model for code...")
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2').to(
        torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    )
    return model, tokenizer

# Generate code autocompletion using GPT-2
def generate_code_completion(prompt, model, tokenizer, max_length=50):
    inputs = tokenizer(prompt, return_tensors='pt').to(model.device)
    output = model.generate(
        inputs['input_ids'], 
        max_length=max_length, 
        num_return_sequences=1, 
        no_repeat_ngram_size=2, 
        early_stopping=True
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Main function to load code data, initialize model, and generate code completion
def main():
    data = load_code_data()  # Load code examples from CSV
    if data is None:
        return  # Stop execution if no data is found

    model, tokenizer = load_model()  # Load GPT-2 model and tokenizer

    # Example: Use the first code snippet as a prompt
    prompt = data['code'].iloc[0] if not data.empty else "print('Hello, World!')"
    print("Prompt:", prompt)

    # Generate and display the completion
    completion = generate_code_completion(prompt, model, tokenizer)
    print("Generated Code Completion:", completion)

if __name__ == "__main__":
    main()
