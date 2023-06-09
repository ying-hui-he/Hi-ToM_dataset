# ToMh Dataset

<img src=media/Picture1.png height=430>

### The `data_ToMh` folder

Contains ToMh data consisting of story-question pairs and the corresponding answers.
The names of subfolder branches have the following meanings:

- `Tell` / `No_Tell`: whether or not the stories contain communications among agents.
- `MC` / `CoT`: the prompting style. Multiple-choice prompting without explanation or chain-of-thought prompting.
- `length_n`: the story length. 1 chapter, 2 chapters or 3 chapters.
- `sample_n`: the numbering of different sample stories.
- `order_n`: the ToM order of the question. From 0 to 4.

### The `prompt_ToMh` folder

Contains prompt files that can be directly input to API.
The data in it are almost the same as `data_ToMh`, except that answers are eliminated.

### Generate new data and prompts

Run the script `generate_tomh.sh`.

### Test it with API

Change the code in `test_azure.py` if necessary, and run the script `run_API.sh`.
