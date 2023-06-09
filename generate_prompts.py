import os
import sys
import itertools


def main():
    input_folder = 'data_ToMh'
    output_folder = 'prompt_ToMh'
    lengths = [1, 2, 3]
    orders = [0, 1, 2, 3, 4]
    prompts = ['CoT', 'MC']
    tells = ['No_Tell', 'Tell']
    for tell, prompt, length, order, sample_num in itertools.product(tells, prompts, lengths, orders, range(1, 21)):
        input_fn = os.path.join(input_folder, tell, prompt, f'length_{length}', f'sample_{sample_num}',
                                f'order_{order}.txt')
        output_fn = os.path.join(output_folder, tell, prompt, f'length_{length}', f'sample_{sample_num}',
                                 f'order_{order}.txt')
        with open(input_fn, 'r') as file:
            lines = file.readlines()
            new_lines = [line for line in lines if line ==
                         '\n' or line.split()[0] != 'Answer:']
        if not os.path.exists(os.path.join(output_folder, tell, prompt, f'length_{length}', f'sample_{sample_num}')):
            os.makedirs(os.path.join(output_folder, tell, prompt,
                        f'length_{length}', f'sample_{sample_num}'))
        with open(output_fn, 'w') as file:
            file.writelines(new_lines)



if __name__ == "__main__":
    sys.exit(main())
