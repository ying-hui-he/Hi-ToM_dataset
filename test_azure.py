import os
import logging
import itertools
import openai


def record_progress(filename):
    with open('progress.txt', 'a') as f:
        f.write(filename + '\n')


def is_processed(filename):
    try:
        with open('progress.txt', 'r') as f:
            processed_files = f.read().splitlines()
        return filename in processed_files
    except FileNotFoundError:
        with open('progress.txt', 'w') as f:  # Creates the file if it doesn't exist
            pass
        return False


openai.api_type = "azure"
openai.api_base = "https://openaiserviceforclausaeu.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

input_folder = 'prompt_ToMh'
output_folder = 'API_responses'
lengths = [1, 2, 3]
orders = [0, 1, 2, 3, 4]
prompts = ['CoT', 'MC']
tells = ['No_Tell', 'Tell']

for tell, prompt, length, order, sample_num in itertools.product(tells, prompts, lengths, orders, range(1, 21)):
    input_fn = os.path.join(input_folder, tell, prompt, f'length_{length}', f'sample_{sample_num}',
                            f'order_{order}.txt')
    output_fn = os.path.join(output_folder, tell, prompt, f'length_{length}', f'sample_{sample_num}',
                             f'order_{order}.txt')
    if is_processed(input_fn):
        continue
    logging.info(f'Testing file: {input_fn}')
    with open(input_fn, 'r') as f:
        input = f.readlines()
    input = "\n".join([inp.strip() for inp in input])

    # TODO modify the used model?
    response = openai.ChatCompletion.create(
        engine="gpt4-8k",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps people find information."},
            {"role": "user", "content": input}
        ],
        temperature=0,
        max_tokens=2000,
        top_p=0,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    print(response)
    if not os.path.exists(os.path.join(output_folder, tell, prompt, f'length_{length}', f'sample_{sample_num}')):
        os.makedirs(os.path.join(output_folder, tell, prompt, f'length_{length}', f'sample_{sample_num}'))
    with open(output_fn, 'w') as f:
        f.writelines(response)
    record_progress(input_fn)
