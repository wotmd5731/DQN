# -*- coding: utf-8 -*-


import random
import numpy as np
import time
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
#import torchvision.transforms as T
import sys


import argparse
from argument import get_args
args = get_args('DQN_rlfa')

args.game = 'MountainCar-v0'
args.max_step = 200
args.action_space =3 
args.state_space = 2
args.memory_capacity = 1000000
args.learn_start = 1000000
args.render= True
from env import Env
env = Env(args)

from memory import ReplayMemory 
memory = ReplayMemory(args)

#args.memory_capacity = 1000
#args.learn_start = 1000
#args.render= True
from agent import Agent
agent = Agent(args)



"""
define test function
"""
from plot import _plot_line
current_time = time.time()
Ts, Trewards, Qs = [], [], []
def test(main_episode):
    global current_time
    prev_time = current_time
    current_time = time.time()
    T_rewards, T_Qs = [], []
    Ts.append(main_episode)
    total_reward = 0
    
    episode = 0
    while episode < args.evaluation_episodes:
        episode += 1
        T=0
        reward_sum=0
        state = env.reset()
        while T < args.max_step:
            T += 1
            if args.render:
                env.render()
                
            action = agent.get_action(state,evaluate=True)
            next_state , reward , done, _ = env.step(action)
            state = next_state
    
            total_reward += reward
            reward_sum += reward
            if done:
                break
        T_rewards.append(reward_sum)
    ave_reward = total_reward/args.evaluation_episodes
    # Append to results
    Trewards.append(T_rewards)
#        Qs.append(T_Qs)
    
    # Plot
    _plot_line(Ts, Trewards, 'rewards_'+args.name+args.game, path='results')
#        _plot_line(Ts, Qs, 'Q', path='results')
    
    # Save model weights
#        main_dqn.save('results')
    print('episode: ',main_episode,'Evaluation Average Reward:',ave_reward, 'delta time:',current_time-prev_time)
#            if ave_reward >= 300:
#                break
    



random_max_loop = 10

global_count = 0
episode = 0
max_reward=-100000000000000
while True:
    done = 0
    episode += 1
    T=0
    state = env.reset()
    t_reward =0
    
    while T < args.max_step:
        action = random.randrange(0,args.action_space)
        for ii in range(random.randint(1,random_max_loop)):
            next_state , reward , done, _ = env.step(action)
            t_reward += reward
            memory.push([state, action, reward, next_state, done])
            state = next_state
            T += 1
            global_count += 1
            if done :
                break
        if done :
            break
    
    max_reward = max(t_reward,max_reward)
    print("\r push : %d/%d  max reward %d "%(global_count,args.learn_start, max_reward),end='\r',flush=True)
#    print("push : %d/%d  max reward %d "%(global_count,args.learn_start, max_reward))
#    print("\r push : ",global_count,'/',args.learn_start,end='\r',flush=True)

    if global_count > args.learn_start:
        break

print('')

"""
main loop
"""
global_count = 0
episode = 0



while episode < args.max_episode_length:
    episode += 1
    T=0
    done = 0
    state = env.reset()
#    args.epsilon -= 0.8/args.max_episode_length
    while T < args.max_step:
        T += 1
        global_count += 1
        
#        action = random.randrange(0,args.action_space)
        action = agent.get_action(state)
        for ii in range(random.randint(1,random_max_loop)):
            next_state , reward , done, _ = env.step(action)
            if args.reward_clip > 0:
                reward = max(min(reward, args.reward_clip), -args.reward_clip)  # Clip rewards
     
            memory.push([state, action, reward, next_state, done])
            state = next_state
            
            if global_count % args.replay_interval == 0 :
                agent.basic_learn(memory)
            if global_count % args.target_update_interval == 0 :
                agent.target_dqn_update()
            if done :
                break 
        if done :
            break
    if episode % args.evaluation_interval == 0 :
        test(episode)
