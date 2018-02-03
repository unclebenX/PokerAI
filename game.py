import utilities as u
import numpy as np
from deck import Deck
import enum

class Action(enum.Enum):
    FOLD = 1
    CHECK = 2
    BET_CALL = 3

class Game:
    deck = None
    players = None #liste de joueurs
    stacks = None #Dictionnaire : label = joueur
    cards = None #Dictionnaire de np.array : label = joueur
    board = None #Une seule matrice
    small_blind = None
    big_blind = None
    game_actions = None #Liste de listes de couples (joueur, action). (Pour l'instant on ne s'en occupe pas dans la prédiction)
    pot = None
    current_bet = None #A chaque tour, on ajoute le current bet au pot (fois le nombre de joueurs restants, vu qu'il n'y a pas de raise et donc de fold possible apres qu'un joueur ait bet)
    remaining_players = None
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
        self.current_bet = 0.
        self.remaining_players = []
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
        self.current_bet = 0.
        self.remaining_players = []
        return

    def play_game(self, N):
        """
        N est le nombre de parties qu'on veut jouer. 1 reward par epoch.
        Renvoie un array contenant les rewards de chacun des joueurs.
        """
        order = list(self.players)
        cumulative_reward = np.zeros(len(self.players))
        for i in range(N):
            cumulative_reward += self.play_hand(order)
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
        conditional_policy = {Action.FOLD: pi[0], Action.CHECK: pi[1], Action.BET_CALL: pi[2]}
        last_actions = zip(self.game_actions[-1])[1]
        if Action.BET_CALL in last_actions:
            conditional_policy.pop(Action.CHECK, None)
        if self.stacks[player] < .5 * self.pot:
            conditional_policy.pop(Action.BET_CALL, None)
        if max(conditional_policy.keys()) == 0:
            return random.choice(list(conditional_policy.values()))
        return u.sample_distribution_from_dict(conditional_policy)

    def apply_action(self, player, action):
        '''
        Applique l'action action par le joueur player a l'etat courant du jeu.
        '''
        self.game_actions[-1].append((player,action))
        if action == Action.BET_CALL:
            if self.current_bet == 0:
                self.current_bet = .5 * self.pot
            self.stacks[player] -= self.current_bet
        if action == Action.FOLD:
            self.remaining_players.remove(player)
        return

    def play_hand(self, order):
        """
        order est une liste d'objets de classe "AI" qui vont jouer successivement.
        Joue une main dans cet ordre.
        """
        self.remaining_players = list(order)
        '''
        Ecrire les differents tours de bet.
        '''
        pass
