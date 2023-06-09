import os
import openai

def record_progress(filename):
    with open('progress.txt', 'a') as f:
        f.write(filename + '\n')

def is_processed(filename):
    with open('progress.txt', 'r') as f:
        processed_files = f.read().splitlines()
    return filename in processed_files

openai.api_type = "azure"
openai.api_base = "https://openaiserviceforclausaeu.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

test_dirs = os.listdir("prompt_ToMh")
for test_dir in test_dirs:
    test_fns = os.listdir(f"prompt_ToMh/{test_dir}")
    for test_fn in test_fns:
        full_path = f"prompt_ToMh/{test_dir}/{test_fn}"
        if is_processed(full_path):
            continue
        print(test_fn)
        print(f"path: {full_path}")
        with open(full_path, 'r') as f:
            input = f.readlines()
        input = "\n".join([inp.strip() for inp in input])
        response = openai.ChatCompletion.create(
          engine="gpt4-32k",
          messages=[
            {"role":"system","content":"You are an AI assistant that helps people find information."},
            {"role":"user","content": input}
          ],
          temperature=0,
          max_tokens=800,
          top_p=0,
          frequency_penalty=0,
          presence_penalty=0,
          stop=None)
        print(response)
        record_progress(full_path)
