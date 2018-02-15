# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 16:28:50 2018

@author: petit
"""

import tensorflow as tf
import numpy as np
from player import Player

class AIPlayer(Player):
    '''
    Deep-Q network AI player
    '''

    def __init__(self, name, n_players=3, learning_rate = .1, gamma = 1.):
        Player.__init__(self, name)
        self.n_players = n_players
        #Initialize TensorFlow
        tf.reset_default_graph()
        #Define network inputs
        #Last row = stacks; bottom right = pot (always less than 13 players)
        self.input_layer = tf.placeholder(shape=[9,13], dtype=tf.float32)
        #Define the neural network for value function approximation
        self.layer_1_dim = 30
        self.layer_1 = tf.layers.dense(self.input_layer, self.layer_1_dim, activation=tf.nn.relu)
        self.layer_2_dim = 20
        self.layer_2 = tf.layers.dense(self.layer_1, self.layer_2_dim, activation=tf.nn.relu)
        self.output_layer_dim = 3
        self.output_layer = tf.layers.dense(self.layer_2, self.output_layer_dim)
        self.prediction = tf.argmax(self.output_layer,1)
        #Define the loss function
        self.real_q = tf.placeholder(shape=[1,3], dtype=tf.float32)
        self.loss = tf.reduce_sum(tf.square(self.real_q-self.output_layer))
        #Define the optimizer
        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
        self.update = optimizer.minimize(self.loss)
        self.init = tf.initialize_all_variables()
        self.sess = tf.Session()
        self.training = True
        return

    def enable_training(self):
        self.training=True
        return

    def disable_training(self):
        self.training=False
        return

    def get_policy(self, X):
        last_row = X[2].copy()
        last_row.resize((1,13))
        last_row[1,12] = x[3]
        feed_input = np.vstack((X[0],X[1], last_row))
        preferred_action, all_Q = self.sess.run([self.prediction, self.output_layer], feed_dict={self.input_layer: feed_input})
        policy = np.zeros(3); policy[preferred_action]=1.
        return policy
