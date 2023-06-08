import argparse
import logging
import glob
import numpy as np
import os
import sys
import random
import itertools

from stringify import stringify
from tasks import Specify_Tasks
from utils import is_file, mkdir_p, remove_extension
from world import World


def generate_story_with_specified_chapters(
    world_paths, output_dir_path, n, noise=0.1, train_noise=False, order=-1, num_chapter=-1, exist_tell_in_story=False, prompt='CoT', exist_answer=False
):
    """Generates stories with guarantee that each task is seen n times."""
    mkdir_p(output_dir_path)
    n = n[0]

    for world in world_paths:

        w = World()
        w.load(world)
        world_name = remove_extension(world)

        # Define task creator and task types
        task = Specify_Tasks()
        tasks_per_length = np.array([
            [('A5', True)],  # 1 chapter
            [('A5', False), ('A3', True)],  # 2 chapters
            [('A5', True), ('A3', False), ('A4', True)],  # 3 chapters
            [('A5', False), ('A3', True),
             ('A4', False), ('A2', True)],  # 4 chapters
        ])

        # If order and num_chapter are not specified
        orders = [0, 1, 2, 3, 4] if order == -1 else [order]
        num_chapters = [1, 2, 3, 4] if num_chapter == -1 else [num_chapter]
        for order_of_story in orders:
            for length_of_story in num_chapters:
                # Create folder to contain data
                folder_name = f'{order_of_story}_order_{length_of_story}_chapters'
                # logging.info("Creating New task in %s..." % folder_name)
                mkdir_p(os.path.join(output_dir_path, folder_name))

                for i in range(n):
                    fname = f'{order_of_story}order_{length_of_story}chap_{i}.txt'
                    path = os.path.join(output_dir_path, folder_name, fname)

                    with open(path, 'w', encoding='utf-8') as f:
                        story = task.generate_story_qs_at_end(
                            w, length_of_story, tasks_per_length[length_of_story -
                                                                 1], num_agents=5,
                            num_locations=3, statement_noise=0, order=order_of_story, exist_tell_in_story=exist_tell_in_story
                        )
                        if prompt == 'MC':
                            f.write(
                                'Read the following story and answer the multiple-choice question. Please provide answer without explanations.\n')
                        else:
                            f.write(
                                'Read the following story and answer the multiple-choice question. Think step-by-step, and provide detailed explanations.\n')
                        f.write('Story:\n')
                        f.write('\n'.join(stringify(story, exist_answer=exist_answer)))
                        f.write('Note: \n')


def parse_args(args):

    parser = argparse.ArgumentParser(
        description='Process command-line arguments.'
    )

    parser.add_argument(
        '-w', '--world_path', dest='world_paths', type=is_file, required=True,
        action='append', help='Path to a world definition file'
    )

    parser.add_argument(
        '-o', '--output_dir_path', dest='output_dir_path', type=mkdir_p,
        default='data_ToMh', help='Output directory path'
    )

    # parser.add_argument(
    #     '-b', '--babi_dir_path', dest='babi_dir_path', type=str, required=True,
    #     help='Path to directory containing the 20 bAbi task train + test data'
    # )

    parser.add_argument(
        '-l', '--logging', type=str, default='INFO', metavar='logging',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level'
    )

    parser.add_argument(
        '-n', '--num_stories', dest='num_stories_choices', type=int,
        action='append', required=True,
        help='Number of stories (examples) in a task)'
    )

    parser.add_argument(
        '-ptn', '--prob_test_noise', dest='test_noise', type=float,
        required=True, help='Probability of encountering random noise sentence'
    )

    parser.add_argument(
        '-tn', '--train_noise', dest='train_noise', type=bool, default=False,
        help='Whether or not to include noise at training time'
    )
    parser.add_argument(
        '-ord', '--order', dest='order', type=int, default=-1,
        help='The range of question orders'
    )
    parser.add_argument(
        '-len', '--length', dest='num_chapter', type=int, default=-1,
        help='The range of story lengths'
    )
    parser.add_argument(
        '-t', '--tell', dest='exist_tell', type=bool, default=False,
        help='Whether or not the story has communications between agents'
    )
    parser.add_argument(
        '-p', '--prompt', dest='prompt_type', type=str, default='CoT',
        choices=['MC', 'CoT'],
        help='The type of prompt chosen between MC and CoT'
    )
    parser.add_argument(
        '-a', '--answer', dest='exist_answer', type=bool, default=False,
        help='Whether or not the data has answers'
    )

    parsed = parser.parse_args(args)

    return parsed


def main(args=sys.argv[1:]):
    """Main function to generate all the story-question pairs."""
    args = parse_args(args)
    logging.basicConfig(
        level=args.logging, format='%(asctime)s\t%(levelname)-8s\t%(message)s'
    )
    folder_name = 'Tell/' if args.exist_tell else 'No_Tell/'
    folder_name += args.prompt_type

    output_dir_path = os.path.join(args.output_dir_path, folder_name) if args.exist_answer else os.path.join('prompt_ToMh', folder_name)
    generate_story_with_specified_chapters(
        world_paths=args.world_paths,
        output_dir_path=output_dir_path,
        n=args.num_stories_choices,
        noise=args.test_noise,
        train_noise=args.train_noise,
        order=args.order,
        num_chapter=args.num_chapter,
        exist_tell_in_story=args.exist_tell,
        prompt=args.prompt_type,
        exist_answer=args.exist_answer,
    )


if __name__ == "__main__":
    sys.exit(main())
