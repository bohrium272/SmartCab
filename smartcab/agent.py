import random
import numpy as np
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.last_reward = 0
        self.last_action = None
        self.state = 'Random'
        self.APLHA = 1
        self.GAMMA = 2

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.last_reward = 0
        self.last_action = None
        self.state = 'Random'

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        available_actions = []
        # TODO: Update state
        if inputs['light'] == 'red':
            """
                Red Light means :
                    Left when no oncoming traffic
                    No action
            """
            if inputs['oncoming'] != 'left':
                available_actions = [None, 'right']
        else:
            """
                Green Light means :
                    Left only if no forward oncoming traffic
                    Perform atleast some action
            """        
            available_actions = ['right', 'left', 'forward']
            if inputs['oncoming'] == 'forward':
                available_actions.remove('left')
        # TODO: Select action according to your policy
        
        action = None
        if available_actions != []:# and self.state == 'Random':
            action = random.choice(available_actions)
        # elif available_actions != [] and self.state == 'Static':
        #     action = self.last_action

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        # if action != None:
        #     if reward > self.last_reward:
        #         self.state = 'Static'
        #     else:
        #         self.state = 'Random'
        self.last_action = action
        self.last_reward = reward

        # print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
