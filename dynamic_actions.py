import numpy as np
from itertools import combinations


class Action(object):

    def __init__(self, templates):
        self.templates = templates

    def render_declarative(self):
        assert 'declarative' in self.templates and \
            len(self.templates['declarative']) > 0
        return np.random.choice(self.templates['declarative'])

    def render_interrogative(self):
        assert 'interrogative' in self.templates and \
            len(self.templates['interrogative']) > 0, str(self.templates)
        return np.random.choice(self.templates['interrogative'])


class ExitAction(Action):

    def __init__(self):
        templates = {
            'declarative': [
                '%s exited the %s.',
                '%s left the %s.',
                '%s went out of the %s.',
            ],
        }
        super().__init__(templates)

#########################################
############### Questions ###############
#########################################

class ZeroQ(Action):

    def __init__(self, oracle, obj):
        
        fill = (obj, oracle.get_object_container(obj))
        templates = {
            'interrogative': [
                'Question: Where is the %s really?\nAnswer: %s' % fill,
            ]
        }
        super().__init__(templates)

class FirstQ(Action):

    def __init__(self, oracle, agent, obj):
        fill = (agent, obj, oracle.get_first_belief(agent, obj))
        templates = {
            'interrogative': [
                'Question: Where does %s think the %s is?\nAnswer: %s' % fill,
            ]
        }
        super().__init__(templates)
        
class SecondQ(Action):

    def __init__(self, oracle, a1, a2, obj):
        fill = (a1, a2, obj, oracle.get_second_belief(a1, a2, obj))
        templates = {
            'interrogative': [
                'Question: Where does %s think %s thinks the %s is?\nAnswer: %s' % fill,
            ]
        }
        super().__init__(templates)

class ThirdQ(Action):

    def __init__(self, oracle, a1, a2, a3, obj):
        fill = (a1, a2, a3, obj, oracle.get_third_belief(a1, a2, a3, obj))
        templates = {
            'interrogative': [
                'Question: Where does %s think %s thinks %s thinks the %s is?\nAnswer: %s' % fill,
            ]
        }
        super().__init__(templates)

class FourthQ(Action):

    def __init__(self, oracle, a1, a2, a3, a4, obj):
        fill = (a1, a2, a3, a4, obj, oracle.get_fourth_belief(a1, a2, a3, a4, obj))
        templates = {
            'interrogative': [
                'Question: Where does %s think %s thinks %s thinks %s thinks the %s is?\nAnswer: %s' % fill,
            ]
        }
        super().__init__(templates)
        
# class MemoryAction(Action):

#     def __init__(self, oracle_start_state, obj):
#         fill = (obj, oracle_start_state[obj])
#         templates = {
#             'interrogative': [
#                 'Where was the %s at the beginning?\t%s' % fill,
#             ]
#         }
#         super().__init__(templates)

# class LocationAction(Action):
#     def __init__(self, oracle, args):
#         """
#         Creaters string with args and modifies 
#         oracle in accordance with action.
#         """
#         if len(args) == 2:
#             statement = '%s is in the %s.' % args
#             a1, loc = args
#             # may be redundant
#             oracle.set_location(a1, loc)
#         else : # 2 people
#             statement = '%s and %s are in the %s.' % args
#             a1, a2, loc = args
#             # may be redundant
#             oracle.set_location(a1, loc)
#             oracle.set_location(a2, loc)
            
#         templates = {
#             'declarative': [
#                 statement,
#             ]
#         }
        
#         super().__init__(templates)

class ObjectLocAction(Action):

    def __init__(self, oracle, obj, observers):
        container = oracle.get_object_container(obj)
        templates = {
            'declarative': [
                'The %s is in the %s.' % (obj, container),
            ]
        }
        
        # set first beliefs
        for observer in observers:
            oracle.set_first_belief(observer, obj, container)
            
        # set second beliefs
        for observer1, observer2 in combinations(observers, 2):
            oracle.set_second_belief(observer1, observer2, obj, container)
                    
        # set third beliefs
        for observer1, observer2, observer3 in combinations(observers, 3):
            oracle.set_third_belief(observer1, observer2, observer3, obj, container)

        # set fourth beliefs
        for observer1, observer2, observer3, observer4 in combinations(observers, 4):
            oracle.set_fourth_belief(observer1, observer2, observer3, observer4, obj, container)
        super().__init__(templates)
        
class ExitedAction(Action):

    def __init__(self, oracle, agent):
        fill = (agent, oracle.get_location(agent))
        
        templates = {
            'declarative': [
                '%s exited the %s and stayed in the waiting room.' % fill,
            ]
        }
        oracle.set_location(agent, None)
        super().__init__(templates)

class MoveAction(Action):

    def __init__(self, oracle, args, observers=None):
        templates = {
            'declarative': [
                '%s moved the %s to the %s.' % args,
            ]
        }
        
        agent, obj, container = args
        oracle.set_object_container(obj, container)
        
        if not observers:
            observers = []
        observers.append(agent)
        
        # set first beliefs
        for observer in observers:
            oracle.set_first_belief(observer, obj, container)
            
        # set second beliefs
        for observer1, observer2 in combinations(observers, 2):
            oracle.set_second_belief(observer1, observer2, obj, container)
                    
        # set third beliefs
        for observer1, observer2, observer3 in combinations(observers, 3):
            oracle.set_third_belief(observer1, observer2, observer3, obj, container)

        # set fourth beliefs
        for observer1, observer2, observer3, observer4 in combinations(observers, 4):
            oracle.set_fourth_belief(observer1, observer2, observer3, observer4, obj, container)
                    
        super().__init__(templates)
        
# class PeekAction(Action):

#     def __init__(self, oracle, args, observers=None):
#         templates = {
#             'declarative': [
#                 '%s looked in the %s.' % args,
#             ]
#         }
        
#         agent, container = args
#         contents = oracle.get_container_obj(container)
        
        
#         if not observers:
#             observers = []
        
#         observers.append(agent)
#         # set direct beliefs
#         for observer in observers:
#             for obj in contents:
#                 oracle.set_first_belief(observer, obj, container)
         
        
#         # set indirect beliefs
#         for observer1 in observers:
#             for observer2 in observers:
#                 if observer1 != observer2:
#                     for obj in contents:
#                         oracle.set_second_belief(observer1, observer2, obj, container)
        
                    
#         super().__init__(templates)

class PublicTellAction(Action):

    def __init__(self, oracle, a1, obj, container, observers=None):
        templates = {
            'declarative': [
                '%s publicly claimed that %s is in the %s.'% (a1, obj, container),
            ]
        }
        
        container = oracle.get_object_container(obj)
        oracle.set_first_belief(a2, obj, container)
        oracle.set_second_belief(a2, a1, obj, container)
        super().__init__(templates)

class PrivateTellAction(Action):

    def __init__(self, oracle, a1, a2, obj, container):
        templates = {
            'declarative': [
                '%s privately told %s that the %s is actually in the %s.'% (a1, a2, obj, container),
            ]
        }

        # container = oracle.get_object_container(obj)
        oracle.set_first_belief(a2, obj, container)
        oracle.set_second_belief(a2, a1, obj, container)
        super().__init__(templates)
        
class EnterAction(Action):

    def __init__(self, oracle, args, observers=None, no_world_adjust=False):
        templates = {
            'declarative': [
                '%s entered the %s.' % args,
            ]
        }
        
        agent, location = args
        oracle.set_location(agent, location)
        # assume all containers are not enclosed
        # agent knows location of everything
        objs = oracle.get_objects_at_location(location)
        if not observers:
            observers=[]
        observers.append(agent)
        
        if not no_world_adjust:
            for obj in objs:
                container = oracle.get_object_container(obj)
                oracle.set_first_belief(agent, obj, container)
                for observer1 in observers:
                    for observer2 in observers:
                        if observer1 != observer2:
                            oracle.set_second_belief(observer1, observer2, obj, container)

        super().__init__(templates)
        
class NoiseAction(Action):

    def __init__(self):
        templates = {
            'declarative': [
                'Phone rang.',
            ]
        }
        super().__init__(templates)

    
