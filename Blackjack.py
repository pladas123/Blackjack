import time
import random
import re

import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

import deck_generator
import hand_evaluation
import bj

n_players = 1
n_decks = 8
start_deck = deck_generator.deck_gen(n_decks)
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

for p in range(1,n_players+1):
    key = 'p' + str(p)
    players[key] = []
    wealth[key] = 100
    bets[key] = "0"
    final_hand[key] = []

def bet(player):
    print("Wealth remaining : " + str(wealth[player]))
    p_bet = int(input("Bet value : "))
    if p_bet <= wealth[player]:
        wealth[player] -= (p_bet)
        bets[player] = (p_bet)
        print("Wealth remaining : " + str(wealth[player]))
    else:
        bets[player] = 0

def count(card):
    if card[1] == "ace":
        op_count[0] -= 1
    elif card[1] in ["jack","queen","king"]:
        op_count[9] -= 1
    else:
        op_count[int(card[1])-1] -= 1
    
def deal(player):
    hand_current = players[player]
    c_draw = start_deck.pop()
    count(c_draw)
    players[player].append(c_draw)
    deal_out = hand_evaluation.beautify(c_draw)
    return deal_out
    
def deal_start(): 
    for p in players:
        deal(p)
        print("Cards remaining : " + str(len(start_deck)))

def dealer_cards():
    dealer_current = dealer["d"]
    d_draw = start_deck.pop()
    count(d_draw)
    dealer["d"].append(d_draw)
    dealer_out = hand_evaluation.beautify(d_draw)
    return dealer_out

def dealer_strat():
    dealer["final"] = 0
    def dealer_eval():
        running_total_hard = 0
        running_total_soft = 0
        dealer_hand = dealer["d"]
        for d_card in dealer_hand:
            if d_card[1] == "ace":
                running_total_soft += 11
                running_total_hard += 1
            elif d_card[1] in ["jack","queen","king"]:
                running_total_soft += 10
                running_total_hard += 10
            else:
                running_total_hard += int(d_card[1])   
                running_total_soft += int(d_card[1])
        if running_total_soft < 21 and running_total_hard > 21:
            dealer["final"] = running_total_soft
        elif running_total_soft > 21 and running_total_hard < 21:
            dealer["final"] = running_total_soft
        else:
            dealer["final"] = running_total_hard
    while dealer["final"] < 17:
        dealer_cards()
        dealer_eval()
    print(dealer["final"])
        

class interface_window():
    def __init__(self, dealer_draw):
        self.dealer_draw = dealer_draw
        self.operations()

    def operations(self):
        root = Tk()

        img_dealer = Image.open(self.dealer_draw)
        panel_dealer = Label(root)
        img_dealer = ImageTk.PhotoImage(img_dealer.resize((x,y), Image.ANTIALIAS))
        panel_dealer.configure(image = img_dealer)
        panel_dealer.image = img_dealer

        panel_0 = Label(root)
        panel_1 = Label(root)
        panel_2 = Label(root)
        panel_3 = Label(root)

        panel_dealer.grid(row = 0, columnspan = 4)
        panel_0.grid(row = 1, column = 0)
        panel_1.grid(row = 1, column = 1)
        panel_2.grid(row = 1, column = 2)
        panel_3.grid(row = 1, column = 3)

        for p in players:
            eval_ = hand_evaluation.hand_eval(players, p, ('0'))

            new_images = eval_.hand_summary()
            new_img0 = Image.open(new_images[0])
            new_img0 = ImageTk.PhotoImage(new_img0.resize((x,y), Image.ANTIALIAS))
            panel_0.configure(image = new_img0)
            panel_0.image = new_img0
            new_img1 = Image.open(new_images[1])
            new_img1 = ImageTk.PhotoImage(new_img1.resize((x,y), Image.ANTIALIAS))
            panel_1.configure(image = new_img1)
            panel_1.image = new_img1
            new_img2 = Image.open("red_joker.png")
            new_img2 = ImageTk.PhotoImage(new_img2.resize((x,y), Image.ANTIALIAS))
            panel_2.configure(image = new_img2)
            panel_2.image = new_img2
            root.update()

            print("************************")
            print(op_count)
            print("Player : " + p)    
            print("Current hand : " + str(eval_.running_hard) + " / " + str(eval_.running_soft)) 

            active = True
            if eval_.running_soft == 21: # I.E. player is bust
                final_hand[p] = "BJ"
                print("Blackjack!")
                active = False

            while active == True:
                action_ = input("hit/stand : ")
                if action_ == "hit":
                    new_img2 = Image.open(deal(p))
                    new_img2 = ImageTk.PhotoImage(new_img2.resize((x,y), Image.ANTIALIAS))
                    panel_2.configure(image = new_img2)
                    panel_2.image = new_img2
                    root.update()

                    eval_ = hand_evaluation.hand_eval(players,p,('0'))
                    if eval_.running_soft < 21:
                        print(p + ' : ' + str(eval_.running_hard) + " / " + str(eval_.running_soft))
                    elif eval_.running_soft == 21 or eval_.running_hard == 21: # 21
                        print("21!")
                        final_hand[p] = 21
                        active = False
                    elif eval_.running_hard > 21: # Bust
                        print("Bust!")
                        final_hand[p] = eval_.running_hard
                        active = False
                elif action_ == "stand":
                    print("Final hand : " + str(eval_.running_soft))
                    higher_ = max(eval_.running_soft, eval_.running_hard) 
                    final_hand[p] = int(higher_)
                    active = False
                else:
                    pass
                time.sleep(2)

if __name__ == "__main__":
    for p in players:
        bet(p)
    deal_start()
    deal_start()
    x = 100
    y = round(1.452 * x)
    iw = interface_window(str(dealer_cards()))
    dealer_cards()
    dealer_strat()
    dealer_final = int(dealer["final"])
    print("Final hands : " + str(final_hand))
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
    print("Total bets : " + str(bets))
    print("Wealth : " + str(wealth))