import numpy as np


from clause import Clause, Question
from oracle import Oracle
from dynamic_actions import *
from collections import defaultdict
import random


def sample_question(oracle_start_state, oracle, agent1, agent2, obj, question):
    idx_dummy = [0]
    questions = [Question(idx_dummy, FirstQ(oracle, agent1, obj)),
                 Question(idx_dummy, FirstQ(oracle, agent2, obj)),
                 Question(idx_dummy, SecondQ(oracle, agent1, agent2, obj)),
                 Question(idx_dummy, ZeroQ(oracle, obj)),
                 Question(idx_dummy, MemoryAction(oracle_start_state, obj))
                 ]
    if question:
        if question == 'memory':
            return questions[-1]
        elif question == 'reality':
            return questions[3]
        elif question == 'belief':
            return questions[2]
        elif question == 'search':
            return questions[1]
    return np.random.choice(questions)

# -------------------------------- Chapters ---------------------------------- #


def write_A2_chapter(
        start_state, oracle, location, agent_ids, all_agents, movements=None, exist_tell=False, questions=None
):
    a1, a2 = all_agents[agent_ids[0]], all_agents[agent_ids[1]]
    outsiders = [agent for agent in all_agents if agent not in [a1, a2]]
    agent_ids = [aid+1 for aid in agent_ids]

    # Pick random object at location
    obj = np.random.choice(oracle.get_objects_at_location(location))

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

    if movements[0]:
        chapter.extend([
            Clause(MoveAction(oracle, (a1, obj, containers[1]), [a2]))
        ])
    chapter.extend([
        Clause(ExitedAction(oracle, (a1)))
    ])

    if movements[1]:
        chapter.extend([
            Clause(MoveAction(oracle, (a2, obj, containers[2]), None))
        ])
    chapter.extend([
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
        start_state, oracle, location, agent_ids, all_agents, movements=None, exist_tell=False, questions=None
):
    a1, a2, a3 = all_agents[agent_ids[0]
                            ], all_agents[agent_ids[1]], all_agents[agent_ids[2]]
    outsiders = [agent for agent in all_agents if agent not in [a1, a2, a3]]
    agent_ids = [aid+1 for aid in agent_ids]

    # Pick random object at location
    obj = np.random.choice(oracle.get_objects_at_location(location))

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

    if movements[0]:
        chapter.extend([
            Clause(MoveAction(oracle, (a1, obj, containers[1]), [a2, a3]))
        ])
    chapter.extend([
        Clause(ExitedAction(oracle, (a1)))
    ])

    if movements[1]:
        chapter.extend([
            Clause(MoveAction(oracle, (a2, obj, containers[2]), [a3]))
        ])
    chapter.extend([
        Clause(ExitedAction(oracle, (a2)))
    ])

    if movements[2]:
        chapter.extend([
            Clause(MoveAction(oracle, (a3, obj, containers[3]), None))
        ])
    chapter.extend([
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
        start_state, oracle, location, agent_ids, all_agents, movements=None, exist_tell=False, questions=None
):
    a1, a2, a3, a4 = all_agents[agent_ids[0]
                                ], all_agents[agent_ids[1]], all_agents[agent_ids[2]], all_agents[agent_ids[3]]
    outsiders = [
        agent for agent in all_agents if agent not in [a1, a2, a3, a4]]
    agent_ids = [aid+1 for aid in agent_ids]

    # Pick random object at location
    obj = np.random.choice(oracle.get_objects_at_location(location))

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

    if movements[0]:
        chapter.extend([
            Clause(MoveAction(oracle, (a1, obj, containers[1]), [a2, a3, a4]))
        ])
    chapter.extend([
        Clause(ExitedAction(oracle, (a1)))
    ])

    if movements[1]:
        chapter.extend([
            Clause(MoveAction(oracle, (a2, obj, containers[2]), [a3, a4]))
        ])
    chapter.extend([
        Clause(ExitedAction(oracle, (a2)))
    ])

    if movements[2]:
        chapter.extend([
            Clause(MoveAction(oracle, (a3, obj, containers[3]), [a4]))
        ])
    chapter.extend([
        Clause(ExitedAction(oracle, (a3)))
    ])

    if movements[3]:
        chapter.extend([
            Clause(MoveAction(oracle, (a4, obj, containers[4]), None))
        ])
    chapter.extend([
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
        start_state, oracle, location, agent_ids, all_agents, movements=None, exist_tell=False, questions=None
):
    a1, a2, a3, a4, a5 = all_agents[agent_ids[0]], all_agents[agent_ids[1]
                                                              ], all_agents[agent_ids[2]], all_agents[agent_ids[3]], all_agents[agent_ids[4]]
    agent_ids = [aid+1 for aid in agent_ids]

    # Pick random object at location
    obj = np.random.choice(oracle.get_objects_at_location(location))

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

    if movements[0]:
        chapter.extend([
            Clause(MoveAction(
                oracle, (a1, obj, containers[1]), [a2, a3, a4, a5]))
        ])
    chapter.extend([
        Clause(ExitedAction(oracle, (a1)))
    ])

    if movements[1]:
        chapter.extend([
            Clause(MoveAction(oracle, (a2, obj, containers[2]), [a3, a4, a5]))
        ])
    chapter.extend([
        Clause(ExitedAction(oracle, (a2)))
    ])

    if movements[2]:
        chapter.extend([
            Clause(MoveAction(oracle, (a3, obj, containers[3]), [a4, a5]))
        ])
    chapter.extend([
        Clause(ExitedAction(oracle, (a3)))
    ])

    if movements[3]:
        chapter.extend([
            Clause(MoveAction(oracle, (a4, obj, containers[4]), [a5]))
        ])
    chapter.extend([
        Clause(ExitedAction(oracle, (a4)))
    ])

    if movements[4]:
        chapter.extend([
            Clause(MoveAction(oracle, (a5, obj, containers[0]), None))
        ])
    chapter.extend([
        Clause(ExitedAction(oracle, (a5)))
    ])

    # tell actions has 4 different forms
    if exist_tell:
        tell_containers = random.sample(oracle.get_containers(location)[:], 2)
        tell_form = random.choice(range(4))
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


def write_true_belief_chapter(
    start_state, oracle, location, agent_ids, all_agents, questions=None
):
    """
    Creates list of clauses that constitute
    a true belief task.

    agent_ids: list that gives indices of agents
      in container. should be length 2.
    all_agents: list of all agents
    container: container to which the object is
      moved
    question: one of ['memory', 'reality', 'belief', 'search', None]
      if None, then pick randomly

    Warning: clauses will advance that state
    of the simulation, should clauses should
    be appended in order.
    """
    a1, a2 = all_agents[agent_ids[0]], all_agents[agent_ids[1]]
    agent_ids = [aid+1 for aid in agent_ids]

    # Pick random object at location
    obj = np.random.choice(oracle.get_objects_at_location(location))
    container_1 = oracle.get_object_container(obj)

    # Pick random container in locations
    container_candidates = oracle.get_containers(location)[:]
    container_candidates.remove(container_1)
    container_2 = np.random.choice(container_candidates)

    chapter = []

    # Move agents into location
    if oracle.get_location(a1) == location:
        chapter.extend([
            Clause([agent_ids[0]], LocationAction(oracle, (a1, location)))
        ])
    else:
        chapter.extend([
            Clause([agent_ids[0]], EnterAction(oracle, (a1, location)))
        ])

    if oracle.get_location(a2) == location:
        chapter.extend([
            Clause(agent_ids, LocationAction(oracle, (a2, location)))
        ])
    else:
        chapter.extend([
            Clause(agent_ids, EnterAction(oracle, (a2, location), [a1]))
        ])

    chapter.extend([
        Clause(agent_ids, ObjectLocAction(oracle, obj, [a1, a2])),
        Clause(agent_ids, MoveAction(oracle, (a1, obj, container_2), [a2])),
    ])

    for question in questions:
        chapter.append(
            sample_question(start_state, oracle, a1, a2, obj, question)
        )

    return chapter


def write_false_belief_chapter(
    start_state, oracle, location, agent_ids, all_agents, questions=None
):
    """
    Creates list of clauses that constitute
    a true belief task.

    agent_ids: list that gives indices of agents
      in container. should be length 2.
    all_agents: list of all agents
    container: container to which the object is
      moved

    Warning: clauses will advance that state
    of the simulation, should clauses should
    be appended in order.
    """
    a1, a2 = all_agents[agent_ids[0]], all_agents[agent_ids[1]]
    agent_ids = [aid+1 for aid in agent_ids]

    # pick random object at location
    obj = np.random.choice(oracle.get_objects_at_location(location))
    container_1 = oracle.get_object_container(obj)

    # pick random container in locations
    container_candidates = oracle.get_containers(location)[:]
    container_candidates.remove(container_1)
    container_2 = np.random.choice(container_candidates)

    chapter = []

    # move agents into location
    if oracle.get_location(a1) == location:
        chapter.extend(
            [Clause([agent_ids[0]], LocationAction(oracle, (a1, location)))])
    else:
        chapter.extend(
            [Clause([agent_ids[0]], EnterAction(oracle, (a1, location)))])

    if oracle.get_location(a2) == location:
        chapter.extend(
            [Clause(agent_ids, LocationAction(oracle, (a2, location)))])
    else:
        chapter.extend(
            [Clause(agent_ids, EnterAction(oracle, (a2, location), [a1]))])

    chapter.extend([
        Clause(agent_ids, ObjectLocAction(oracle, obj, [a1, a2])),
        Clause(agent_ids, ExitedAction(oracle, (a2))),
        Clause([agent_ids[0]], MoveAction(oracle, (a1, obj, container_2))),
        # Clause(agent_ids, EnterAction(oracle, (a2, location))), # closed container condition
        # TODO: fancy inheritance to copy start state
        # sample_question(start_state, oracle, a1, a2, obj, question)
    ])
    # JUST ONE QUESTION SPLITS A STRING TODO TODO
    for question in questions:
        chapter.append(sample_question(
            start_state, oracle, a1, a2, obj, question))

    return chapter


def write_second_order_false_belief_chapter(
    start_state, oracle, location, agent_ids, all_agents, questions=None
):
    """
    Creates list of clauses that constitute
    a true belief task.

    agent_ids: list that gives indices of agents
      in container. should be length 2.
    all_agents: list of all agents
    container: container to which the object is
      moved

    Warning: clauses will advance that state
    of the simulation, should clauses should
    be appended in order.
    """
    a1, a2 = all_agents[agent_ids[0]], all_agents[agent_ids[1]]
    agent_ids = [aid+1 for aid in agent_ids]

    # pick random object at location
    obj = np.random.choice(oracle.get_objects_at_location(location))
    container_1 = oracle.get_object_container(obj)

    # pick random container in locations
    container_candidates = oracle.get_containers(location)[:]
    container_candidates.remove(container_1)
    container_2 = np.random.choice(
        container_candidates)  # set would be more elegant

    chapter = []

    # move agents into location
    if oracle.get_location(a1) == location:
        chapter.extend(
            [Clause([agent_ids[0]], LocationAction(oracle, (a1, location)))])
    else:
        chapter.extend(
            [Clause([agent_ids[0]], EnterAction(oracle, (a1, location)))])

    if oracle.get_location(a2) == location:
        chapter.extend(
            [Clause(agent_ids, LocationAction(oracle, (a2, location)))])
    else:
        chapter.extend(
            [Clause(agent_ids, EnterAction(oracle, (a2, location), [a1]))])

    chapter.extend([
        Clause(agent_ids, ObjectLocAction(oracle, obj, [a1, a2])),
        Clause(agent_ids, ExitedAction(oracle, (a2))),
        Clause([agent_ids[0]], MoveAction(oracle, (a1, obj, container_2))),
        Clause([agent_ids[0]], ExitedAction(oracle, (a1))),
        Clause([agent_ids[1]], EnterAction(oracle, (a2, location))),
        # Clause([agent_ids[1]], PeekAction(oracle, (a2, container_2))), # closed container condition
        # Clause([agent_ids[0]], EnterAction(oracle, (a1, location), [a2])), # closed container condition
        # sample_question(start_state, oracle, a1, a2, obj, question)
    ])

    for question in questions:
        chapter.append(sample_question(
            start_state, oracle, a1, a2, obj, question))

    return chapter

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

    def generate_story(
        self, world, tasks_per_story, tasks, questions, num_agents=6,
        num_locations=3, statement_noise=0
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

        idx_support_dummy = [0]
        actors = world.get_actors()
        locations = world.get_locations()
        objects = world.get_objects()
        containers = world.get_containers()

        random_actors = np.random.choice(
            actors, size=num_agents, replace=False)
        random_locations = np.random.choice(
            locations, size=num_locations, replace=False)
        random_objects = np.random.choice(
            objects, size=num_locations*2, replace=False)
        random_containers = np.random.choice(
            containers, size=num_locations*2, replace=False)

        oracle = Oracle(random_actors, random_locations,
                        random_objects, random_containers)

        # Populate locations in the oracle with containers
        for i in range(len(random_locations)):
            location = random_locations[i]
            containers = random_containers[2*i:2*i+2]
            oracle.set_containers(location, list(containers))

        for i in range(len(random_objects)):
            oracle.set_object_container(
                random_objects[i], random_containers[i])

        start_state = oracle.locations.obj_containers.copy()

        chapters = {'tb': write_true_belief_chapter, 'fb': write_false_belief_chapter,
                    'sofb': write_second_order_false_belief_chapter}

        story = []
        for i in range(tasks_per_story):
            chapter = chapters[tasks[i]]
            location = np.random.choice(random_locations)
            agent_ids = np.random.choice(
                range(len(random_actors)), size=2, replace=False
            )
            story.extend(
                chapter(
                    start_state, oracle, location, agent_ids,
                    random_actors, [questions[i]]
                )
            )

        if statement_noise:
            noisy_story = []
            prev_i = 0
            noise = [i for i in range(len(story))
                     if np.random.rand() < statement_noise]
            for i in noise:
                noisy_story.extend(story[prev_i:i] +
                                   [Clause([], NoiseAction())])
                prev_i = i
            noisy_story.extend(story[prev_i:])

            return noisy_story

        return story

    def generate_story_qs_at_end(
        self, world, tasks_per_story, tasks, questions, num_agents=6,
        num_locations=3, statement_noise=0
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
            containers, size=num_locations*2, replace=False
        )

        # Create the oracle
        oracle = Oracle(
            random_actors, random_locations, random_objects, random_containers
        )

        # Populate locations in the oracle with containers
        for i in range(len(random_locations)):
            location = random_locations[i]
            containers = random_containers[2*i:2*i+2]
            oracle.set_containers(location, list(containers))

        # Populate containers with objects
        for i in range(len(random_objects)):
            oracle.set_object_container(
                random_objects[i], random_containers[i])

        # Need start state for memory question
        start_state = oracle.locations.obj_containers.copy()

        # Create story by task
        chapters = {'tb': write_true_belief_chapter,
                    'fb': write_false_belief_chapter,
                    'sofb': write_second_order_false_belief_chapter}
        story = []
        for i in range(tasks_per_story-1):
            chapter = chapters[tasks[i]]
            location = np.random.choice(random_locations)
            agent_ids = np.random.choice(
                range(len(random_actors)), size=2, replace=False
            )
            story.extend(
                chapter(
                    start_state, oracle, location, agent_ids, random_actors, []
                )
            )
        chapter = chapters[tasks[-1]]
        location = np.random.choice(random_locations)
        agent_ids = np.random.choice(
            range(len(random_actors)), size=2, replace=False
        )
        story.extend(
            chapter(
                start_state, oracle, location, agent_ids, random_actors, questions
            )
        )

        # At the end, at noise sentences randomly
        if statement_noise:
            noisy_story = []
            prev_i = 0
            noise = [i for i
                     in range(len(story)) if np.random.rand() < statement_noise
                     ]
            for i in noise:
                noisy_story.extend(
                    story[prev_i:i] + [Clause([], NoiseAction())]
                )
                prev_i = i
            noisy_story.extend(story[prev_i:])

            return noisy_story

        return story
