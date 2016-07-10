import random
import numpy as np
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class qLearningAgent(Agent):
    """Q Learner for Smart Cab"""
    def __init__(self, env):
        super(qLearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.state = None
        self.last_state = None
        self.action = None
        self.last_action = None
        self.last_reward = 0
        self.alpha = 0.9
        self.gamma = 0.35
        self.epsilon = 0.001
        self.q_table = dict()
        self.ACTIONS = ['forward', 'left', 'right', None]

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.last_action = None
        self.state = None
        self.last_state = None
        self.epsilon = 0.001
        self.last_reward = 0
        self.alpha = 0.9
        self.gamma = 0.35

    def get_q(self, state, action):
        return self.q_table.get((state, action), 19.75)

    def get_value(self, state):
        best_q = -float('inf')
        for action in self.ACTIONS:
            if self.get_q(state, action) > best_q:
                best_q = self.get_q(state, action)
        return best_q

    def get_action_by_policy(self, state):
        best_action = None
        best_q = -float('inf')
        for action in self.ACTIONS:
            temp_value = self.get_q(state, action)
            if temp_value > best_q:
                best_q = temp_value
                best_action = action
            if temp_value == best_q:
                factor = random.random()
                if factor < 0.5:
                    best_q = temp_value
                    best_action = action
        return best_action

    def get_action(self, state):
        action = None
        factor = random.random()
        if factor < self.epsilon:
            # print "random"
            action = random.choice(self.ACTIONS)
        else:
            # print "policy"
            action = self.get_action_by_policy(state)
        return action
    
    def update_q_values(self, state, action, reward, future_state):
        if (state, action) not in self.q_table.keys():
            self.q_table[(state, action)] = 19.75
        else:
            temp = self.q_table[(state, action)]
            temp = ((1 - self.alpha) * temp) + ((self.alpha) * (reward + self.gamma * self.get_value(future_state) - temp))  
            self.q_table[(state, action)] = temp

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (str(inputs), self.next_waypoint, deadline)
        # TODO: Select action according to your policy
        action = self.get_action(self.state)

        # Execute action and get reward
        reward = self.env.act(self, action)
        # TODO: Learn policy based on state, action, reward
        if self.last_reward != None:
            self.update_q_values(self.last_state, self.last_action, self.last_reward, self.state)
        self.last_action = action
        self.last_state = self.state
        self.last_reward = reward
        # print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]