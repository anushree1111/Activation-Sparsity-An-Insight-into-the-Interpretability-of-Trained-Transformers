from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import csv


def pad_sequence(token_tensor, max_len):
    """
    Pad the token tensor to have length max_len.
    """
    if len(token_tensor) < max_len:
        pad_size = (max_len - len(token_tensor),)
        pad_tensor = torch.zeros(pad_size, dtype=torch.long)
        padded_token_tensor = torch.cat((token_tensor, pad_tensor))
    else:
        padded_token_tensor = token_tensor[:max_len]
    return padded_token_tensor


def remove_quotes(s):
    if s[0] == s[-1] == '"':
        return s[1:-1]
    else:
        return s


if __name__ == "__main__":
    # Load the tokenizer
    tokenizer = T5Tokenizer.from_pretrained('t5-base')

    # Load the model
    model = T5ForConditionalGeneration.from_pretrained('t5-base')

    # Example inputs and outputs
    inputs = "translate English to French: Hello, how are you?"
    expected_output = "Bonjour comment allez-vous?"

    with open('RandomSents.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        input_ids = [tokenizer.encode(remove_quotes(row[0]), return_tensors='pt')[0] for row in reader]
        max_len = len(max(input_ids, key=len))
        print(f"Maximum length token: {max_len}")
        padded_tokens = [torch.tensor([list(pad_sequence(input_id, max_len))]) for input_id in input_ids]

        for index, padded_token in enumerate(padded_tokens):
            print(f"Index: {index}")
            generated_ids = model.generate(padded_token)
            generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            print("Generated text:", generated_text)


    '''
    # Tokenize the inputs and expected output
    input_ids = tokenizer.encode(inputs, return_tensors='pt')
    output_ids = tokenizer.encode(expected_output, return_tensors='pt')

    # Generate text from the inputs
    generated_ids = model.generate(input_ids)
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    # Print the generated text
    print("Generated text:", generated_text) '''
