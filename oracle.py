"""
The Oracle class keeps track of all object
and agent locations as well as a map of
beliefs about object and agent locations.
"""
import copy

class LocationMap(object):

    def __init__(self, agents, locations, objects, containers):
        
        # Maps agents to their locations.
        self.locations = {agent : None for agent in agents}
        
        # Maps agents to their locations.
        self.container_locations = {container : None for container in containers}
        
        # Maps locations to their containers
        self.containers = {location : None for location in locations}
        
        # Maps containers to the objects they hold
        self.container_objs = {container : [] for container in containers}
        
        # Maps objects to their containers
        self.obj_containers = {obj : None for obj in objects}
        
class MemoryMap(object):
    
    def __init__(self, agents, objects):
        
        zero_dict = {obj : None for obj in objects}
        first_dict = {agent : copy.deepcopy(zero_dict) for agent in agents}
        second_dict = {agent : copy.deepcopy(first_dict) for agent in agents}
        third_dict = {agent : copy.deepcopy(second_dict) for agent in agents}
        fourth_dict = {agent : copy.deepcopy(third_dict) for agent in agents}
        
        # Dictionary of dictionaries mapping
        # agents to objects to containers. Represents
        # agents' belief about location of containers.
        self.first_belief = copy.deepcopy(first_dict)
        
        # Dictionary of dictionaries of dictionaries
        # mapping agents to direct belief dictionaries.
        # Represents agents' belief about other agents'
        # beliefs about location of containers.
        self.second_belief = copy.deepcopy(second_dict)
        self.third_belief = copy.deepcopy(third_dict)
        self.fourth_belief = copy.deepcopy(fourth_dict)

class Oracle(object):

    def __init__(self, agents, locations, objects, containers):
        self.memory_map = MemoryMap(agents, objects)
        self.locations = LocationMap(agents, locations, objects, containers)
        
    #########################################
    ################ Beliefs ################
    #########################################
    
    def get_first_belief(self, agent, obj):
        beliefs = self.memory_map.first_belief
        return beliefs[agent][obj]
    
    def set_first_belief(self, agent, obj, container):
        beliefs = self.memory_map.first_belief
        beliefs[agent][obj] = container
    
    def get_second_belief(self, a1, a2, obj):
        second_belief = self.memory_map.second_belief
        return second_belief[a1][a2][obj]
            
    def set_second_belief(self, a1, a2, obj, container):
        second_belief = self.memory_map.second_belief
        second_belief[a1][a2][obj] = container

    def get_third_belief(self, a1, a2, a3, obj):
        third_belief = self.memory_map.third_belief
        return third_belief[a1][a2][a3][obj]
            
    def set_third_belief(self, a1, a2, a3, obj, container):
        third_belief = self.memory_map.third_belief
        third_belief[a1][a2][a3][obj] = container
    
    def get_fourth_belief(self, a1, a2, a3, a4, obj):
        fourth_belief = self.memory_map.fourth_belief
        return fourth_belief[a1][a2][a3][a4][obj]
            
    def set_fourth_belief(self, a1, a2, a3, a4, obj, container):
        fourth_belief = self.memory_map.fourth_belief
        fourth_belief[a1][a2][a3][a4][obj] = container
    
    #########################################
    ############### Locations ###############
    #########################################
    
    def get_location(self, agent):
        return self.locations.locations[agent]
    
    def set_location(self, agent, location):
        self.locations.locations[agent] = location
        
    def get_containers(self, location):
        # Returns a list of containers at location
        return self.locations.containers[location]
    
    def set_containers(self, location, containers):
        # May need to change to move containers bt locs
        # Containers is a list of containers at location
        for container in containers:
            self._set_container_location(container, location)
        self.locations.containers[location] = containers
        
    def get_objects_at_location(self, location):
        objects = []
        for container in self.get_containers(location):
            objects.extend(self.get_container_obj(container))
        return objects
       
    def get_container_location(self, container):
        return self.locations.container_locations[container]
    
    def _set_container_location(self, container, location):
        self.locations.container_locations[container] = location
        
    def get_container_obj(self, container):
        # get list of objects in container
        return self.locations.container_objs[container]
    
    def _add_container_obj(self, container, obj):
        self.locations.container_objs[container].append(obj)
        
    def _remove_container_obj(self, container, obj):
        self.locations.container_objs[container].remove(obj)
    
    def get_object_container(self, obj):
        # get container that holds object
        return self.locations.obj_containers[obj]
    
    def set_object_container(self, obj, container):
        # set container that holds object
        prev_container = self.get_object_container(obj)
        if prev_container:
            self._remove_container_obj(prev_container, obj)
        self._add_container_obj(container, obj)
        self.locations.obj_containers[obj] = container
    
            