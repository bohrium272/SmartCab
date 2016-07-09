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
        self.alpha = 0.5
        self.gamma = 0.35
        self.epsilon = 0.0
        self.q_table = dict()
        self.ACTIONS = ['forward', 'left', 'right', None]

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.last_action = None
        self.state = None
        self.last_state = None
        self.epsilon = 0.0

    def get_q(self, state):
        return self.q_table.get((state, action), 0.0)

    def get_action_by_policy(self, state):
        best_action = None

    def get_action(self, state):
        action = None
        factor = random.random()
        if factor < 0.5:
            #TO-DO: Choose a random action
            action = random.choice(self.ACTIONS)
        else:
            #TO-DO: Choose action according to policy
            return get_action_policy(self, state)

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (inputs, self.next_waypoint, action)
        # TODO: Select action according to your policy
        action = self.get_action(self, state)

        # Execute action and get reward
        reward = self.env.act(self, action)
        # TODO: Learn policy based on state, action, reward
        if self.last_reward != None:
            self.update_q_values(self.last_state, self.last_action, self.last_reward, self.state)
        self.last_action = action
        self.last_state = self.state
        self.last_reward = reward
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


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