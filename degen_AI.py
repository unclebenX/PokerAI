# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 16:28:50 2018

@author: petit
"""

import tensorflow as tf
import numpy as np
from player import Player
import utilities as u

class DegenAIPlayer(Player):
    '''
    Policy gradient AI agent.
    '''

    def __init__(self, name, n_players=3, learning_rate = .1, gamma = 1.):
        Player.__init__(self, name)
        self.n_players = n_players
        #Initialize TensorFlow
        tf.reset_default_graph()
        
        #Define a placeholder for rewards
        self.rewards = tf.placeholder(tf.float32, name='rewards')
        
        #Define network inputs
        #Last row = stacks; bottom right = pot (always less than 13 players)
        self.input_layer = tf.placeholder(shape=[None,117], dtype=tf.float32)
        
        #Define the neural network for value function approximation
        self.layer_1_dim = 30
        self.layer_1 = tf.layers.dense(self.input_layer, self.layer_1_dim, activation=tf.nn.relu)
        self.layer_2_dim = 30
        self.layer_2 = tf.layers.dense(self.layer_1, self.layer_2_dim, activation=tf.nn.relu)
        self.output_layer_dim = 1
        self.output_layer = tf.layers.dense(self.layer_2, self.output_layer_dim)
        
        #Define the loss function
        self.loss = tf.reduce_sum(tf.square(self.rewards-self.output_layer))
        
        #Define the optimizer
        self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
        self.training_op = self.optimizer.minimize(self.loss)
        self.init = tf.initialize_all_variables()
        self.sess = tf.Session()
        
        init = tf.initialize_all_variables()
        self.sess.run(init)
        self.exploration_probability = .9
        return
    
    def train(self, states, actions, rewards):
        self.sess.run([self.training_op], feed_dict={self.input_layer: states, self.rewards: rewards})
        return
    
    def get_baseline(self, states):
        return self.sess.run([self.output_layer], feed_dict={self.input_layer: states})
    
    def get_policy(self, X):
        '''
        Degen policy to explore the cards' value.
        '''
        return np.array([0., 0., 1.])
