import utilities as u
import numpy as np
from deck import Deck

class Game:
    deck = None
    players = None
    stacks = None #Dictionnaire : label = joueur
    cards = None #Dictionnaire de np.array : label = joueur
    board = None #Une seule matrice
    small_blind = None
    big_blind = None
    game_actions = None #Liste de listes d'actions. (Pour l'instant on ne s'en occupe pas dans prédiction)
    pot = None
    N = None
    
    def __init__(self, players, small_blind = 0.005, big_blind = 0.01, N = 20):
        self.deck = Deck()
        self.players = players
        self.stacks = {player: 1. for player in self.players}
        self.cards = {player: np.zeros((4,13)) for player in self.players}
        self.board = np.zeros((4,13))
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.game_actions = []
        self.pot = 0.
        self.N = N
        return
    
    def reset_game(self):
        self.__init__(self.players, small_blind = self.small_blind, self.big_blind=small_blind)
        return
    
    def reset_hand(self):
        self.deck = Deck()
        self.cards = {player: np.zeros((4,13)) for player in self.players}
        self.board = np.zeros((4,13))
        self.game_actions = []
        self.pot = 0.
        return
    
    def play_game(self, N):
        """
        N est le nombre de parties qu'on veut jouer. 1 reward par epoch.
        Renvoie un array contenant les rewards de chacun des joueurs.
        """
        order = list(self.players)
        for i in range(N):
            self.play_hand(order)
            self.reset_hand()
            order = u.rotate(order)
        return self.stacks
        
    def to_X(self, player):
        """
        Retourne l'état du jeu pour le joueur i.
        X est un tuple (cartes du joueur, cartes sur la table, stacks, pot)
        """
        stacks = np.array([self.stacks[p] for p in self.players])
        return (self.cards[player], self.board, stacks, self.pot)
        
    def sample_policy(self, player, pi):
        """
        Sample une policy sur l'ensemble des actions possibles.
        Pi = np.array([proba_fold, proba_check, proba_bet/call])
        """
        last_actions = self.game_actions[-1]
        
        pass
        
    def apply_action(self, player, action):
        """
        Applique l'action "action" par le joueur "player".
        """
        pass
    
    def play_hand(self, order):
        """
        order est une liste d'objets de classe "AI" qui vont jouer successivement.
        Joue une main dans cet ordre.
        """