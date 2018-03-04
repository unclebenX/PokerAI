# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 16:28:50 2018

@author: petit
"""

import tensorflow as tf
import numpy as np
from player import Player
import utilities as u

class AIPlayer(Player):
    '''
    Policy gradient AI agent.
    '''

    def __init__(self, name, n_players=3, learning_rate = .1, gamma = 1.):
        Player.__init__(self, name)
        self.n_players = n_players
        #Initialize TensorFlow
        tf.reset_default_graph()
        
        #Define placeholders for actions and rewards
        self.picked_actions = tf.placeholder(tf.int8, name='picked_actions')
        self.rewards = tf.placeholder(tf.float32, name='rewards')
        
        #Define network inputs
        #Last row = stacks; bottom right = pot (always less than 13 players)
        self.input_layer = tf.placeholder(shape=[9,13], dtype=tf.float32)
        
        #Define the neural network for value function approximation
        self.layer_1_dim = 30
        self.layer_1 = tf.layers.dense(self.input_layer, self.layer_1_dim, activation=tf.nn.relu)
        self.layer_2_dim = 20
        self.layer_2 = tf.layers.dense(self.layer_1, self.layer_2_dim, activation=tf.nn.relu)
        self.output_layer_dim = 3
        self.output_layer = tf.layers.dense(self.layer_2, self.output_layer_dim, activation=tf.nn.sigmoid)
        
        #Define the loss function
        self.log_probs = tf.log(tf.gather(self.output_layer, self.picked_actions))
        self.loss = -tf.reduce_sum(tf.mul(self.log_probs, self.rewards))
        
        #Define the optimizer
        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
        self.training_op = self.optimizer.minimize(self.loss)
        self.init = tf.initialize_all_variables()
        self.sess = tf.Session()
        return
    
    def update(self, states, actions, rewards):
        self.sess.run([self.training_op], feed_dict={self.input_layer: states, self.picked_actions: u.get_indices(actions), self.rewards: rewards})
        return
    
    def get_policy(self, X):
        last_row = X[2].copy()
        last_row.resize((1,13))
        last_row[1,12] = X[3]
        feed_input = np.vstack((X[0],X[1], last_row))
        policy = self.sess.run([self.output_layer], feed_dict={self.input_layer: feed_input})
        return policy
