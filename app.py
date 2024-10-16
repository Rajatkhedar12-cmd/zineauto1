from flask import Flask, request, jsonify, render_template
import pandas as pd
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

# Load the code examples dataset
def load_code_data(filename='code_examples.csv'):
    try:
        data = pd.read_csv(filename)
        return data
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None

# Initialize GPT-2 model and tokenizer for code
def load_model():
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

# Load the model and dataset
model, tokenizer = load_model()
data = load_code_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    prompt = request.form['prompt']
    completion = generate_code_completion(prompt, model, tokenizer)
    return jsonify({'completion': completion})

if __name__ == "__main__":
    app.run(debug=True)
