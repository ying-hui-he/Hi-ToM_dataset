# Hi-ToM Dataset

This is the dataset for the paper ["Hi-ToM: A Benchmark for Evaluating Higher-Order Theory of Mind Reasoning in Large Language Models"](https://arxiv.org/abs/2310.16755).

<img src=media/Picture1.png height=430>

### The `Hi-ToM_data` folder

Contains ToMh data consisting of story-question pairs and the corresponding answers.
The names of subfolder branches have the following meanings:

- `Tell` / `No_Tell`: whether or not the stories contain communications among agents.
- `MC` / `CoT`: the prompting style. `MC` corresponds to Vanilla Prompting (VP) in the paper, while `CoT` stands for Chain-of-Thought Prompting (CoTP).
- `length_n`: the story length, i.e. the number of chapters in a story. From 1 to 3.
- `sample_n`: the numbering of different sample stories.
- `order_n`: the ToM order of the question. From 0 to 4.

### The `Hi-ToM_prompt` folder

Contains prompt files that can be directly input to API.
The data in it are almost the same as `Hi-ToM_data`, except that answers are eliminated.

### Generate new data and prompts

Run the script `generate_tomh.sh`.
