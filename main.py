#!/usr/bin/env python3


# ___________________________________________ Libraries and Definitions ___________________________________________ #


# Learning libraries
import tensorflow as tf
import gym

# Math libraries
import numpy as np

# Time management libraries
import time

# Personal libraries
from HER import HER_Buffer
from HER_SAC_agent import HER_SAC_Agent


# ___________________________________________________ Parameters ___________________________________________________ #


# environment parameters
ENV_NAME = "FetchPush-v1"

# learning parameters
TRAINING_BATCH = 50000
RANDOM_EPISODES = 1000
HER_CAPACITY = 1000

# _____________________________________________________ Main _____________________________________________________ #


if __name__ == '__main__':

    # Environment initialization
    env = gym.make(ENV_NAME)
    obs_space = env.observation_space.shape
    actions_dim = env.action_space.shape[0]

    # Agent initialization
    her_buff = HER_Buffer(HER_CAPACITY)
    agent = HER_SAC_Agent(env, her_buff)

    # Training 
            

    # Random playing (useful for testing)
    #success = agent.random_play(RANDOM_BATCH)
    #if success:
    #    print("Goal achieved! Good job!")
    #else:
    #    print("Bad play...")
