#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 12:41:33 2018

@author: shunling
"""






from textwrap import dedent

import pickle
import random
from isolation import Isolation, Agent, fork_get_action, play

NUM_ROUNDS = 300

depth_limit = 6


def ABSearch(state,depth):
    def my_moves(state):
        own_loc = state.locs[state.player()]
        opp_loc = state.locs[1 - state.player()]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

    def min_value(state,alpha,beta,depth):
        if state.terminal_test(): return state.utility(state.player())
        if depth <= 0: return my_moves(state)

        v = float("inf")
        for a in state.actions():
            v = min(v, max_value(state.result(a),alpha,beta,depth-1))
            if v <=alpha:
                return v
            beta = min(beta,v)
        return v

    def max_value(state,alpha,beta,depth):
        if state.terminal_test(): return state.utility(state.player())
        if depth <= 0: return my_moves(state)
        
        v = float("-inf")
        for a in state.actions():  
            v = max(v, min_value(state.result(a),alpha,beta,depth-1))
            if v >= beta:
                return v
            alpha = max(v,alpha)
     
        return v
        
        
    alpha = float("-inf")
    beta = float("inf")
    best_score = float("-inf")
    best_move = None
        

    for a in state.actions():
        v = min_value(state.result(a),alpha,beta,depth-1)
        alpha = max(v,alpha)
        if v > best_score:
            best_score = v
            best_move = a
        #print(best_move)
    return best_move


###############################################################################

def build_table(num_rounds=NUM_ROUNDS):
    # Builds a table that maps from game state -> action
    # by choosing the action that accumulates the most
    # wins for the active player. (Note that this uses
    # raw win counts, which are a poor statistic to
    # estimate the value of an action; better statistics
    # exist.)
    from collections import defaultdict, Counter
    book = defaultdict(Counter)
    for _ in range(num_rounds):
        state = Isolation()
        build_tree(state, book)
    openbook = {k: max(v, key=v.get) for k, v in book.items()}
    return openbook

def build_tree(state, book, depth=depth_limit):
    if depth <= 0 or state.terminal_test():
        return -simulate(state)
    action = random.choice(state.actions())

    #action = ABSearch(state,depth=depth_limit)
    reward = build_tree(state.result(action), book, depth - 1)
    book[state][action] += reward
    return -reward


def simulate(state):
    player_id = state.player()
    while not state.terminal_test():
        state = state.result(random.choice(state.actions()))
    return -1 if state.utility(player_id) < 0 else 1

book = build_table()


print(book[Isolation(board=41523161203939122082683632224299007, ply_count=0, locs=(None, None))])

with open("data.pickle", 'wb') as f:
    pickle.dump(book, f)
