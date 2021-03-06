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

    def __init__(self, name, n_players=3, learning_rate = .01):
        Player.__init__(self, name)
        self.n_players = n_players
        #Initialize TensorFlow
        tf.reset_default_graph()
        tf.set_random_seed(1234)
        
        #Define placeholders for actions and rewards
        self.picked_actions = tf.placeholder(tf.int32, name='picked_actions')
        self.rewards = tf.placeholder(tf.float32, name='rewards')
        
        #Define network inputs
        #Last row = stacks; bottom right = pot (always less than 13 players)
        self.input_layer = tf.placeholder(shape=[None,117], dtype=tf.float32)
        
        #Define the neural network for value function approximation
        reg = 0.1
        self.layer_1_dim = 100
        self.layer_1 = tf.layers.dense(self.input_layer, self.layer_1_dim, activation=tf.nn.relu, kernel_regularizer = tf.contrib.layers.l1_regularizer(reg))
        self.layer_2_dim = 100
        self.layer_2 = tf.layers.dense(self.layer_1, self.layer_2_dim, activation=tf.nn.relu, kernel_regularizer = tf.contrib.layers.l1_regularizer(reg))
        self.output_layer_dim = 3
        self.output_layer = tf.layers.dense(self.layer_2, self.output_layer_dim, activation=tf.nn.sigmoid, kernel_regularizer = tf.contrib.layers.l1_regularizer(reg))
        
        #Define the loss function
        self.reg_loss = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
        self.log_probs = tf.log(tf.clip_by_value(tf.gather(self.output_layer, self.picked_actions, axis=1), 1e-10, 1.))
        self.loss = -tf.reduce_sum(tf.multiply(self.log_probs, self.rewards)) + self.reg_loss
        
        #Define the optimizer
        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
        self.training_op = self.optimizer.minimize(self.loss)
        self.init = tf.initialize_all_variables()
        self.sess = tf.Session()
        
        init = tf.initialize_all_variables()
        self.sess.run(init)
        self.exploration_probability = .1
        return
    
    def train(self, states, actions, rewards):
        rewards = (rewards - np.mean(rewards))/np.std(rewards)
        self.sess.run([self.training_op], feed_dict={self.input_layer: states, self.picked_actions: u.get_indices(actions), self.rewards: rewards})
        return
    
    def get_policy(self, X):
        if np.random.rand()< .1 + self.exploration_probability:
            return np.array([.2, .4, .4])
        
        feed_input = u.pack_X(X)
        #print(feed_input)
        policy = self.sess.run([self.output_layer], feed_dict={self.input_layer: [feed_input]})
        print('Policy: ' + str(policy[0][0]))
        return policy[0][0]
