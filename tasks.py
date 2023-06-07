import numpy as np


from clause import Clause, Question
from oracle import Oracle
from dynamic_actions import *
from collections import defaultdict
import random


def sample_question(oracle_start_state, oracle, random_actors, obj, question_idx=0):
    idx_dummy = [0]
    random.shuffle(random_actors)
    a1, a2, a3, a4, _ = random_actors
    questions = [Question(idx_dummy, ZeroQ(oracle, obj)),
                 Question(idx_dummy, FirstQ(oracle, a1, obj)),
                 Question(idx_dummy, SecondQ(oracle, a1, a2, obj)),
                 Question(idx_dummy, ThirdQ(oracle, a1, a2, a3, obj)),
                 Question(idx_dummy, FourthQ(oracle, a1, a2, a3, a4, obj))]
    return questions[question_idx]

#######################################
############## Chapters ###############
#######################################


def write_A2_chapter(
        start_state, oracle, obj, location, agent_ids, all_agents, movements=None, exist_tell=False, questions=None
):
    a1, a2 = all_agents[agent_ids[0]], all_agents[agent_ids[1]]
    outsiders = [agent for agent in all_agents if agent not in [a1, a2]]
    agent_ids = [aid+1 for aid in agent_ids]

    # Pick containers. The first element is the initial container of obj
    containers = [oracle.get_object_container(obj)]
    container_candidates = oracle.get_containers(location)[:]
    container_candidates.remove(containers[0])
    containers += random.sample(container_candidates, 2)

    # Fill in the chapter
    chapter = []

    # All selected agents enter the room and see the object
    chapter.extend([
        Clause(EnterAction(oracle, (a1, a2, location))),
        Clause(ObjectLocAction(oracle, obj, [a1, a2])),
    ])

    # a1
    chapter.extend([
        Clause(MoveAction(oracle, (a1, obj, containers[1]), [
               a2], move=movements[0])),
        Clause(ExitedAction(oracle, (a1)))
    ])
    # a2
    chapter.extend([
        Clause(MoveAction(
            oracle, (a2, obj, containers[2]), None, move=movements[1])),
        Clause(ExitedAction(oracle, (a2)))
    ])

    # tell actions has 3 different forms
    if exist_tell:
        tell_containers = random.sample(oracle.get_containers(location)[:], 2)
        tell_form = random.choice(
            range(3)) if outsiders else random.choice(range(2))
        match tell_form:
            case 0:
                chapter.extend([
                    Clause(PublicTellAction(
                        oracle, a1, obj, tell_containers[0], listeners=all_agents, belivers=outsiders)),
                    Clause(PrivateTellAction(oracle, a2, a1,
                           obj, tell_containers[1], trust=True)),
                ])
            case 1:
                chapter.extend([
                    Clause(PublicTellAction(
                        oracle, a2, obj, tell_containers[0], listeners=all_agents, belivers=[a1] + outsiders)),
                    Clause(PrivateTellAction(oracle, a1, a2, obj,
                           tell_containers[1], trust=False)),
                ])
            case 2:
                chapter.extend([
                    Clause(PrivateTellAction(oracle, a1, random.choice(outsiders),
                                             obj, tell_containers[0], trust=True))
                ])


def write_A3_chapter(
        start_state, oracle, obj, location, agent_ids, all_agents, movements=None, exist_tell=False, questions=None
):
    a1, a2, a3 = all_agents[agent_ids[0]
                            ], all_agents[agent_ids[1]], all_agents[agent_ids[2]]
    outsiders = [agent for agent in all_agents if agent not in [a1, a2, a3]]
    agent_ids = [aid+1 for aid in agent_ids]

    # Pick containers. The first element is the initial container of obj
    containers = [oracle.get_object_container(obj)]
    container_candidates = oracle.get_containers(location)[:]
    container_candidates.remove(containers[0])
    containers += random.sample(container_candidates, 3)

    # Fill in the chapter
    chapter = []

    # All selected agents enter the room and see the object
    chapter.extend([
        Clause(EnterAction(oracle, (a1, a2, a3, location))),
        Clause(ObjectLocAction(oracle, obj, [a1, a2, a3])),
    ])

    # a1
    chapter.extend([
        Clause(MoveAction(oracle, (a1, obj, containers[1]), [
               a2, a3], move=movements[0])),
        Clause(ExitedAction(oracle, (a1)))
    ])
    # a2
    chapter.extend([
        Clause(MoveAction(oracle, (a2, obj, containers[2]), [
               a3], move=movements[1])),
        Clause(ExitedAction(oracle, (a2)))
    ])
    # a3
    chapter.extend([
        Clause(MoveAction(
            oracle, (a3, obj, containers[3]), None, move=movements[2])),
        Clause(ExitedAction(oracle, (a3)))
    ])

    # tell actions has 4 different forms
    if exist_tell:
        tell_containers = random.sample(oracle.get_containers(location)[:], 2)
        tell_form = random.choice(
            range(4)) if outsiders else random.choice(range(2))
        match tell_form:
            case 0:
                # a2 lies to all, and a3 lies to a2
                chapter.extend([
                    Clause(PublicTellAction(
                        oracle, a2, obj, tell_containers[0], listeners=all_agents, belivers=[a1] + outsiders)),
                    Clause(PrivateTellAction(oracle, a3, a2,
                           obj, tell_containers[1], trust=True)),
                ])
            case 1:
                # a3 lies to all, and a1 lies to a3
                chapter.extend([
                    Clause(PublicTellAction(
                        oracle, a3, obj, tell_containers[0], listeners=all_agents, belivers=[a1, a2] + outsiders)),
                    Clause(PrivateTellAction(oracle, a1, a3, obj,
                           tell_containers[1], trust=False)),
                ])
            case 2:
                # a1 lies to all, but a3 tells the true location to an outside agent
                chapter.extend([
                    Clause(PublicTellAction(
                        oracle, a1, obj, tell_containers[0], listeners=all_agents, belivers=outsiders)),
                    Clause(PrivateTellAction(oracle, a3, random.choice(outsiders),
                           obj, oracle.get_object_container(obj), trust=True))
                ])
            case 3:
                # a2 lies to a3, but a3 tells the true location to an outside agent
                chapter.extend([
                    Clause(PrivateTellAction(oracle, a2, a3,
                           obj, tell_containers[0], trust=False)),
                    Clause(PrivateTellAction(oracle, a3, random.choice(outsiders),
                           obj, oracle.get_object_container(obj), trust=True))
                ])


def write_A4_chapter(
        start_state, oracle, obj, location, agent_ids, all_agents, movements=None, exist_tell=False, questions=None
):
    a1, a2, a3, a4 = all_agents[agent_ids[0]
                                ], all_agents[agent_ids[1]], all_agents[agent_ids[2]], all_agents[agent_ids[3]]
    outsiders = [
        agent for agent in all_agents if agent not in [a1, a2, a3, a4]]
    agent_ids = [aid+1 for aid in agent_ids]

    # Pick containers. The first element is the initial container of obj
    containers = [oracle.get_object_container(obj)]
    container_candidates = oracle.get_containers(location)[:]
    container_candidates.remove(containers[0])
    containers += random.sample(container_candidates, 4)

    # Fill in the chapter
    chapter = []

    # All selected agents enter the room and see the object
    chapter.extend([
        Clause(EnterAction(oracle, (a1, a2, a3, a4, location))),
        Clause(ObjectLocAction(oracle, obj, [a1, a2, a3, a4])),
    ])

    # a1
    chapter.extend([
        Clause(MoveAction(oracle, (a1, obj, containers[1]), [
               a2, a3, a4], move=movements[0])),
        Clause(ExitedAction(oracle, (a1)))
    ])
    # a2
    chapter.extend([
        Clause(MoveAction(oracle, (a2, obj, containers[2]), [
               a3, a4], move=movements[1])),
        Clause(ExitedAction(oracle, (a2)))
    ])
    # a3
    chapter.extend([
        Clause(MoveAction(oracle, (a3, obj, containers[3]), [
               a4], move=movements[2])),
        Clause(ExitedAction(oracle, (a3)))
    ])
    # a4
    chapter.extend([
        Clause(MoveAction(
            oracle, (a4, obj, containers[4]), None, move=movements[3])),
        Clause(ExitedAction(oracle, (a4)))
    ])

    # tell actions has 4 different forms
    if exist_tell:
        tell_containers = random.sample(oracle.get_containers(location)[:], 2)
        tell_form = random.choice(
            range(4)) if outsiders else random.choice(range(2))
        match tell_form:
            case 0:
                # a2 lies to all, and a3 lies to a2
                chapter.extend([
                    Clause(PublicTellAction(
                        oracle, a2, obj, tell_containers[0], listeners=all_agents, belivers=[a1] + outsiders)),
                    Clause(PrivateTellAction(oracle, a4, a3,
                           obj, tell_containers[1], trust=True)),
                ])
            case 1:
                # a3 lies to all, and a1 lies to a4
                chapter.extend([
                    Clause(PublicTellAction(
                        oracle, a3, obj, tell_containers[0], listeners=all_agents, belivers=[a1, a2] + outsiders)),
                    Clause(PrivateTellAction(oracle, a1, a4, obj,
                           tell_containers[1], trust=False)),
                ])
            case 2:
                outsider = random.choice(outsiders)
                # a1 lies to all, but a4 tells the true location to an outside agent
                chapter.extend([
                    Clause(PublicTellAction(
                        oracle, a1, obj, tell_containers[0], listeners=all_agents, belivers=outsiders)),
                    Clause(PrivateTellAction(oracle, a4, outsider,
                           obj, oracle.get_object_container(obj), trust=True))
                ])
            case 3:
                outsider = random.choice(outsiders)
                # a2 lies to a3, but a4 tells the true location to an outside agent
                chapter.extend([
                    Clause(PrivateTellAction(oracle, a2, a3,
                           obj, tell_containers[0], trust=False)),
                    Clause(PrivateTellAction(oracle, a4, outsider,
                           obj, oracle.get_object_container(obj), trust=True))
                ])


def write_A5_chapter(
        start_state, oracle, obj, location, agent_ids, all_agents, movements=None, exist_tell=False, questions=None
):
    a1, a2, a3, a4, a5 = all_agents[agent_ids[0]], all_agents[agent_ids[1]
                                                              ], all_agents[agent_ids[2]], all_agents[agent_ids[3]], all_agents[agent_ids[4]]
    agent_ids = [aid+1 for aid in agent_ids]

    # Pick containers. The first element is the initial container of obj
    containers = [oracle.get_object_container(obj)]
    container_candidates = oracle.get_containers(location)[:]
    container_candidates.remove(containers[0])
    containers += random.sample(container_candidates, 4)

    # Fill in the chapter
    chapter = []

    # All selected agents enter the room and see the object
    chapter.extend([
        Clause(EnterAction(oracle, (a1, a2, a3, a4, a5, location))),
        Clause(ObjectLocAction(oracle, obj, [a1, a2, a3, a4, a5])),
    ])

    # a1
    chapter.extend([
        Clause(MoveAction(oracle, (a1, obj, containers[1]), [
               a2, a3, a4, a5], move=movements[0])),
        Clause(ExitedAction(oracle, (a1)))
    ])
    # a2
    chapter.extend([
        Clause(MoveAction(oracle, (a2, obj, containers[2]), [
               a3, a4, a5], move=movements[1])),
        Clause(ExitedAction(oracle, (a2)))
    ])
    # a3
    chapter.extend([
        Clause(MoveAction(oracle, (a3, obj, containers[3]), [
               a4, a5], move=movements[2])),
        Clause(ExitedAction(oracle, (a3)))
    ])
    # a4
    chapter.extend([
        Clause(MoveAction(oracle, (a4, obj, containers[4]), [
               a5], move=movements[3])),
        Clause(ExitedAction(oracle, (a4)))
    ])
    # a5
    chapter.extend([
        Clause(MoveAction(
            oracle, (a5, obj, containers[0]), None, move=movements[4])),
        Clause(ExitedAction(oracle, (a5)))
    ])

    # tell actions has 3 different forms
    if exist_tell:
        tell_containers = random.sample(oracle.get_containers(location)[:], 2)
        tell_form = random.choice(range(3))
        match tell_form:
            case 0:
                # a3 lies to all, and a5 lies to a3
                chapter.extend([
                    Clause(PublicTellAction(
                        oracle, a3, obj, tell_containers[0], listeners=all_agents, belivers=[a1, a2])),
                    Clause(PrivateTellAction(oracle, a5, a3,
                           obj, tell_containers[1], trust=True)),
                ])
            case 1:
                # a4 lies to all, but a5 tells the true location to a1
                chapter.extend([
                    Clause(PublicTellAction(
                        oracle, a4, obj, tell_containers[0], listeners=all_agents, belivers=[a1, a2, a3])),
                    Clause(PrivateTellAction(oracle, a5, a1, obj,
                           oracle.get_object_container(obj), trust=True)),
                ])
            case 2:
                # a3 lies a1, and a2 lies to a4
                chapter.extend([
                    Clause(PrivateTellAction(oracle, a3, a1,
                           obj, tell_containers[0], trust=True)),
                    Clause(PrivateTellAction(oracle, a2, a4,
                           obj, tell_containers[1], trust=False))
                ])


#######################################
############### Tasks #################
#######################################

class Task(object):

    def __init__(self,
                 num_questions=5,
                 exit_prob=1.,
                 informant_prob=1.,
                 search_prob=1.,
                 test_cond='first order'):

        self.num_questions = num_questions

        self.search_prob = search_prob

        self.exit_inform_probs = [1 - exit_prob,
                                  exit_prob * (1 - informant_prob),
                                  exit_prob * informant_prob]
        assert sum(self.exit_inform_probs) == 1

        assert test_cond in ['first order',
                             'second order',
                             'reality',
                             'memory'], \
            "Invalid test condition: %s" % test_cond
        self.test_cond = test_cond

    def generate_story(self, world):
        raise NotImplementedError("Abstract method.")


class Specify_Tasks(Task):
    def generate_story_qs_at_end(
        self, world, tasks_per_story, tasks, num_agents=5,
        num_locations=3, statement_noise=0, order=0, exist_tell_in_story=False
    ):
        """
        Allows user to specify chapter and question for each task in story.

        :tasks: list with length of tasks per story. Each entry is a string in
        the set {'tb','fb','sofb'}

        :questions: list with length of tasks per story. Each entry is a string
        in the set {'memory', 'reality', 'belief', 'search'}

        :statement_noise: probability of encountering noise sentence like 'The
        dog ran through the kitchen.'
        """

        # Fetch agents and objects and select a random subset
        idx_support_dummy = [0]
        actors = world.get_actors()
        locations = world.get_locations()
        objects = world.get_objects()
        containers = world.get_containers()

        random_actors = np.random.choice(
            actors, size=num_agents, replace=False
        )
        random_locations = np.random.choice(
            locations, size=num_locations, replace=False
        )
        random_objects = np.random.choice(
            objects, size=num_locations*2, replace=False
        )
        random_containers = np.random.choice(
            containers, size=num_locations*5, replace=False
        )

        # Create the oracle
        oracle = Oracle(
            random_actors, random_locations, random_objects, random_containers
        )

        # Populate locations in the oracle with containers
        for i, random_location in enumerate(random_locations):
            location = random_location
            containers = random_containers[5*i:5*i+5]
            oracle.set_containers(location, list(containers))

        # Populate containers with objects
        for i, random_object in enumerate(random_objects):
            oracle.set_object_container(
                random_object, random_containers[i])

        # Need start state for memory question
        start_state = oracle.locations.obj_containers.copy()

        # Create story by task
        chapters = {'A2': write_A2_chapter,
                    'A3': write_A3_chapter,
                    'A4': write_A4_chapter,
                    'A5': write_A5_chapter}
        story = []
        obj_pool = []
        obj_in_question = None

        for i in range(tasks_per_story):
            chapter = chapters[tasks[i][0]]
            location = np.random.choice(random_locations)
            obj = np.random.choice(oracle.get_objects_at_location(location))
            # Use the obj in the first chap as the target
            if i == 0:
                obj_in_question = obj
            obj_pool.append(obj)
            agent_ids = list(range(5))
            random.shuffle(agent_ids)

            # Randomly choose movements for each agent
            agent_num = int(tasks[i][0][1])
            bools = [True, False]
            movements = [random.choice(bools) for _ in range(agent_num)]
            exist_tell_in_chapter = tasks[i][1] if exist_tell_in_story else False
            story.extend(
                chapter(
                    start_state, oracle, obj, location, agent_ids, random_actors, movements=movements, exist_tell=exist_tell_in_chapter
                )
            )

        story.extend(sample_question(start_state, oracle,
                     random_actors, obj_in_question, question_idx=order))

        # Generate choices of containers
        choices = ', '.join(f'{chr(65+i)}. {container}' for i,
                            container in enumerate(random_containers))
        story.extend('Choices: ' + choices + '\n')

        # At the end, add noise sentences randomly
        if statement_noise:
            noisy_story = []
            prev_i = 0
            noise = [i for i
                     in range(len(story)) if np.random.rand() < statement_noise
                     ]
            for i in noise:
                noisy_story.extend(
                    story[prev_i:i] + [Clause(NoiseAction())]
                )
                prev_i = i
            noisy_story.extend(story[prev_i:])

            return noisy_story

        return story
