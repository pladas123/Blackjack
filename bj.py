import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

import hand_evaluation

def blackjack(players, op_count):
    x = 100
    y = round(1.452 * x)
    for p in players:
        eval_ = hand_evaluation.hand_eval(players, p)

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
        print("Current hand : " + str(eval_.running_soft))  

        active = True
        if eval_.running_soft == 21: # I.E. player is bust
            final_hand[p] = "BJ"
            print("Blackjack!")
            active_players.remove(eval_.player)
            active = False

        while active == True:

            # Insert strategy here

            action_ = input("Deal y/n : ")
            if action_ == "y":
                new_img2 = Image.open(deal(p))
                new_img2 = ImageTk.PhotoImage(new_img2.resize((x,y), Image.ANTIALIAS))
                panel_2.configure(image = new_img2)
                panel_2.image = new_img2
                root.update()

                eval_ = hand_evaluation.hand_eval(players,p)
                print(p + ' : ' + str(eval_.running_soft))

                if eval_.running_soft == 21 or eval_.running_hard == 21: # Blackjack
                    print("21!")
                    final_hand[p] = 21
                    active = False
                if eval_.running_hard > 21: # Bust
                    print("Bust!")
                    final_hand[p] = eval_.running_hard
                    active = False
            elif action_ == "n":
                print("Final hand : " + str(eval_.running_soft))
                higher_ = max(eval_.running_soft, eval_.running_hard) 
                final_hand[p] = int(higher_)
                active = False
            else:
                pass

if __name__ == "__main__":
    blackjack(1,2)