from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the trained model and tokenizer
def load_trained_model(model_path="./custom_model"):
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)
    return model, tokenizer

# Generate text completion using the trained model
def generate_completion(prompt, model, tokenizer):
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(inputs["input_ids"], max_length=50, no_repeat_ngram_size=2)
    return tokenizer.decode(output[0], skip_special_tokens=True)

if __name__ == "__main__":
    model, tokenizer = load_trained_model()  # Load the trained model
    prompt = input("Enter your prompt: ")
    completion = generate_completion(prompt, model, tokenizer)
    print("Generated Completion:", completion)
