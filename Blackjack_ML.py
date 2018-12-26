import time
import threading
import multiprocessing
import random
import re

import matplotlib.pyplot as plt

import deck_generator_ML
import hand_evaluation
import bj
import strategy

n_players = 1
n_decks = 8
start_deck = deck_generator_ML.deck_gen(n_decks)
reg_n = 4*n_decks
reg_ten = 16*n_decks
max_penetration = 0.80
op_count = [reg_n]*9
op_count.append(reg_ten)

lookup_table = {"c" : "clubs", "s" : "spades", "d" : "diamonds", "h" : "hearts"}
dealer = {"d":[]}

players = {}
wealth = {}
bets = {}
final_hand = {}

wealth_track = []

for p in range(1,n_players+1):
    key = 'p' + str(p)
    players[key] = []
    wealth[key] = 1000000
    bets[key] = "1"
    final_hand[key] = []

def reset():
    dealer["d"] = []
    for p in range(1,n_players+1):
        key = 'p' + str(p)
        players[key] = []
        final_hand[key] = []

def bet(player):
    #print("Wealth remaining : " + str(wealth[player]))
    p_bet = 1
    if p_bet <= wealth[player]:
        wealth[player] -= (p_bet)
        bets[player] = (p_bet)
        #print("Wealth remaining : " + str(wealth[player]))
    else:
        bets[player] = 0

def count(card):
    if str(card) == "a":
        op_count[0] -= 1
    else:
        op_count[int(card)-1] -= 1
    
def deal(player):
    hand_current = players[player]
    c_draw = start_deck.pop()
    count(c_draw)
    players[player].append(c_draw)
    
def deal_start():
    for p in players:
        deal(p)
        #print("Cards remaining : " + str(len(start_deck)))

def dealer_cards():
    dealer_current = dealer["d"]
    d_draw = start_deck.pop()
    count(d_draw)
    dealer["d"].append(d_draw)

def dealer_strat():
    dealer["final"] = 0
    def dealer_eval():
        running_total_hard = 0
        running_total_soft = 0
        dealer_hand = dealer["d"]
        for d_card in dealer_hand:
            if d_card == "a":
                running_total_soft += 11
                running_total_hard += 1
            else:
                running_total_hard += int(d_card)   
                running_total_soft += int(d_card)
        if running_total_soft > 21 and running_total_hard < 21:
            dealer["final"] = running_total_hard
        elif running_total_soft < 21:
            dealer["final"] = running_total_soft
        else:
            dealer["final"] = running_total_soft
    while dealer["final"] < 17:
        dealer_eval()
        dealer_cards()
    #print("Dealer final : " + str(dealer["final"]))
        

class round_():
    def __init__(self, dealer_draw):
        self.dealer_draw = dealer_draw
        self.operations()

    def operations(self):

        for p in players:
            eval_ = hand_evaluation.hand_eval(players, p,('1'))

            #print("************************")
            #print(op_count)

            active = True # Alternatively use 'active_players' dict to allow for players to sit out

            if eval_.running_soft == 21: # I.E. player has blackjack, no need to continue
                final_hand[p] = "BJ"
                #print("Blackjack!")
                active = False

            while active == True:
                #print("Current hand : " + str(eval_.running_hard) + " / " + str(eval_.running_soft)) 
                strat_set = strategy.strategy_set_basic
                d_card = dealer["d"][0]
                #print("Dealer : " + str(d_card))
                if d_card == 'a':
                    strat_play = strat_set[eval_.running_hard][0]
                else:
                    strat_play = strat_set[eval_.running_hard][int(d_card)-1]
                if strat_play == 1:
                    action_ = "hit"
                else:
                    action_ = "stand"

                if action_ == "hit":
                    deal(p)
                    eval_ = hand_evaluation.hand_eval(players,p,('1'))
                    if eval_.running_soft < 21:
                        pass
                        #print(p + ' : ' + str(eval_.running_hard) + " / " + str(eval_.running_soft))
                    elif eval_.running_soft == 21 or eval_.running_hard == 21: # 21
                        #print("21!")
                        final_hand[p] = 21
                        active = False
                    elif eval_.running_hard > 21: # Bust
                        #print("Bust!")
                        final_hand[p] = eval_.running_hard
                        active = False
                    else:
                        pass
                        #print(p + ' : ' + str(eval_.running_hard))                        
                elif action_ == "stand":
                    #print("Final hand : " + str(eval_.running_soft))
                    higher_ = max(eval_.running_soft, eval_.running_hard) 
                    final_hand[p] = int(higher_)
                    active = False
                else:
                    print("Error in evaluation module!")

def payout(dealer_final):
    for count,p in enumerate(players,0):
        wealth_player = wealth[p]
        if dealer_final > 21:
            if str(final_hand[p]) == "BJ":
                wealth[p] = int(wealth_player) + (5/2)*int(bets[p])
            elif int(final_hand[p]) < 21:
                wealth[p] = int(wealth_player) + 2*int(bets[p])
            else:
                pass
        elif str(dealer_final) == "BJ":
            if str(final_hand[p]) == "BJ":
                wealth[p] = int(wealth_player) + int(bets[p])
            else:
                pass
        elif int(dealer_final) == 21:
            if str(final_hand[p]) == "BJ":
                wealth[p] = int(wealth_player) + (5/2)*int(bets[p])
            elif int(final_hand[p]) == 21:
                wealth[p] = int(wealth_player) + int(bets[p])
            else:
                pass
        else:
            if str(final_hand[p]) == "BJ":
                wealth[p] = int(wealth_player) + (5/2)*int(bets[p])
            elif int(final_hand[p]) <= 21:
                if final_hand[p] > dealer_final:
                    wealth[p] = int(wealth_player) + int(bets[p])
                else:
                    pass
            else:
                pass

class play():
    def __init__(self):
        self.deck = deck_generator_ML.deck_gen(n_decks)
        self.run_()
        self.wealth_track = []

    def run_(self):
        play_count = 0
        while play_count < 100000:
            while len(self.deck) > 400:
                for p in players:
                    bet(p)
                deal_start()
                deal_start()
                iw = round_(str(dealer_cards()))
                dealer_cards()
                dealer_strat()
                #print("Final hands : " + str(final_hand) +
                        #", Total bets : " + str(bets) +
                        #", Wealth : " + str(wealth))
                wealth_track.append(int(wealth[p]))
                dealer_stand = int(dealer["final"])
                payout(dealer_stand)
                reset()
            self.deck = deck_generator_ML.deck_gen(n_decks)
            play_count += 1

if __name__ == "__main__":

    processes = [ ]
    for i in range(1,5):
        i = multiprocessing.Process(target=play)
        processes.append(i)
        i.start()
    for one_process in processes:
        one_process.join()
    plt.plot(wealth_track)
    plt.ylabel("Wealth")
    plt.xlabel("Hand")
    plt.show()
    print(wealth["p1"]/1000000)