import utilities as u
import numpy as np
from deck import Deck
import enum
import showdown as sd
"""
LA SMALL BLIND NE CALL PAS LA BIG BLIND
"""

class Action(enum.Enum):
    FOLD = 1
    CHECK = 2
    BET_CALL = 3

class Game:
    def __init__(self, players, small_blind = 0.005, big_blind = 0.01, N = 20):
        self.deck                   = Deck() #deck de cartes
        self.players                = players #liste des joueurs
        self.stacks                 = {player: 1. for player in self.players} #dictionnaire : label = joueur
        self.cards                  = {player: np.zeros((4,13)) for player in self.players} #dictionnaire de np.array : label = joueur
        self.board                  = np.zeros((4,13)) #matrice des cartes visibles
        self.small_blind            = small_blind
        self.big_blind              = big_blind
        self.game_actions           = [[]] #Liste de listes de couples (joueur, action). (Pour l'instant on ne s'en occupe pas dans la prédiction)
        self.pot                    = 0. #pot courant dans une hand (actualisé après chaque bet round)
        self.current_bets           = {player: 0. for player in self.players} #bet courant de chaque joueur (re-initialisé après chaque bet round)
        self.max_current_bet        = 0. #bet maximal courant dans un bet round
        self.remaining_players      = list(players) #joueurs restant dans l'epoch courante (liste ordonnée par ordre de jeu à la prochaine hand)
        self.remaining_players_hand = list(players) #joueurs restant dans la hand courante
        self.N                      = N
        self.stacks_history = {player: [1] for player in self.players}
        return

    def reset_game(self):
        self.__init__(self.players, small_blind = self.small_blind, big_blind = self.big_blind)
        return

    def reset_hand(self):
        self.deck = Deck()
        self.cards = {player: np.zeros((4,13)) for player in self.remaining_players}
        self.board = np.zeros((4,13))
        self.game_actions = [[]]
        self.pot = 0.
        self.current_bets = {player: 0. for player in self.remaining_players}
        self.max_current_bet = 0.
        self.remaining_players_hand = list(self.remaining_players) #list() fait une copie
        return
    
    def display(self):
        for p in self.players:
            print('{} : {}'.format(p.name, self.stacks[p]))
        
    def play_game(self, N):
        """
        N est le nombre de parties qu'on veut jouer (N hands = 1 game). 1 reward par game.
        Renvoie un array contenant les rewards de chacun des joueurs.
        """
        i = 0
        while(i < N and len(self.remaining_players) > 1):
            s = self.play_hand()
            for player in self.players:
                self.stacks_history[player].append(s[player])
            self.remaining_players = u.rotate(self.remaining_players)
            self.reset_hand()
            i += 1
            print('---')
            self.display()
            print()
        return self.stacks_history, self.stacks

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
        if self.current_bets[player] < self.max_current_bet:
            conditional_policy.pop(Action.CHECK, None)
        if (self.current_bets[player] == self.max_current_bet and self.max_current_bet > 0) or len(self.remaining_players_hand) == 1: #Pas de raise
            return Action.CHECK
        if self.stacks[player] < .5 * self.pot:
            conditional_policy.pop(Action.BET_CALL, None)
        if self.max_current_bet == 0:
            conditional_policy.pop(Action.FOLD, None)
        if max(conditional_policy.values()) == 0:
            return np.random.choice(list(conditional_policy.keys()))
        return u.sample_distribution_from_dict(conditional_policy)

    def apply_action(self, player, action):
        """
        Applique l'action action par le joueur player a l'etat courant du jeu, renvoie s'il faut garder le joueur dans la main ou non.
        """
        self.game_actions[-1].append((player,action))
        if action == Action.BET_CALL:
            print(player.name+' bets/calls')
            if self.max_current_bet == 0:
                self.max_current_bet = .5 * self.pot
            self.stacks[player] -= self.max_current_bet - self.current_bets[player]
            self.current_bets[player] = self.max_current_bet
            return True
        if action == Action.CHECK:
            print(player.name+' checks')
            return True
        if action == Action.FOLD:
            print(player.name+' folds')
            return False

    def pay_blinds(self):
        players = self.remaining_players
        self.stacks[players[-2]] -= self.small_blind
        self.stacks[players[-1]] -= self.big_blind
        self.current_bets[players[-2]] = self.small_blind
        self.current_bets[players[-1]] = self.big_blind
        self.game_actions[-1].append((players[-2], Action.BET_CALL))
        self.game_actions[-1].append((players[-1], Action.BET_CALL))
        self.max_current_bet = self.big_blind
        print(players[-1].name+' pays big blind')
        print(players[-2].name+' pays small blind')
        
    def bet_round(self):
        player_index = 0
        all_played = False
        while (not all_played or not u.equal_bets(self.current_bets, self.remaining_players_hand)) and len(self.remaining_players_hand)>1:
            player = self.remaining_players_hand[player_index]
            if player_index == len(self.remaining_players_hand) - 1:
                all_played = True
            policy = player.get_policy(self.to_X(player))
            action = self.sample_policy(player, policy)
            keep_player = self.apply_action(player, action)
            if not keep_player:    
                self.remaining_players_hand.remove(player)
                player_index %= len(self.remaining_players_hand)
            else:
                player_index = (player_index + 1) % len(self.remaining_players_hand)
        self.pot += sum(self.current_bets.values())
        if(len(self.remaining_players_hand) < 2):
            self.stacks[self.remaining_players_hand[0]] += self.pot
            return False
        self.current_bets = {player : 0. for player in self.remaining_players_hand}
        self.max_current_bet = 0.
        self.game_actions.append([])          
        return True
    
    def play_hand(self):
        """
        Joue une main dans l'ordre défini par self.remaining_players.
        """
        for player in self.remaining_players:
            self.cards[player][self.deck.get_card()] = 1
            self.cards[player][self.deck.get_card()] = 1
        print("[Blinds]")
        self.pay_blinds()
        #print(self.remaining_players_hand)
        print("[Pre-flop]")
        if(self.bet_round()):
            self.remaining_players_hand = u.rotate(u.rotate(self.remaining_players_hand))
            for i in range(3):
                self.board[self.deck.get_card()] = 1
            print("[Post flop]")
            if(self.bet_round()):
                self.board[self.deck.get_card()] = 1
                print("[Post turn]")
                if(self.bet_round()):
                    self.board[self.deck.get_card()] = 1
                    print("[Post river]")
                    if(self.bet_round()):
                        print("[Showdown]")
                        a = {player : self.cards[player] for player in self.remaining_players_hand}
                        winners = sd.hand_winners(a, self.board)
                        for player in winners:
                            self.stacks[player] += self.pot/len(winners)
                        print('{} wins'.format([player.name for player in winners]))
        for player in self.remaining_players:
            if self.stacks[player] < self.big_blind: 
                self.remaining_players.remove(player)
        return self.stacks