lookup_table = {"c" : "clubs", "s" : "spades", "d" : "diamonds", "h" : "hearts"}

def beautify(card_raw):
    suit = lookup_table[card_raw[0]]
    num = card_raw[1]
    if num in ["jack", "queen", "king"]:
        title = num + '_of_' + suit + "2.png"
    else:
        title = num + '_of_' + suit + ".png"
    return title

class hand_eval():
    def __init__(self, hand_set, player, *args):
        self.player = player
        self.hand = hand_set[player]            
        self.running_soft = 0
        self.running_hard = 0
        self.arg_ = args[0]
        self.basic_summary()        

    def basic_summary(self): 
        ml = self.arg_
        #print("ML : " + str(ml))
        for count, i in enumerate(self.hand,0):
            if int(ml) == 1:
                self.candidate_card = self.hand[count]
            else:
                self.candidate_card = self.hand[count][1]
            if self.candidate_card in ["jack","queen","king"]:
                self.running_soft += 10
                self.running_hard += 10      
            elif self.candidate_card == "ace" or self.candidate_card == "a":
                self.running_soft += 11
                self.running_hard += 1   
            else:
                self.running_soft += int(self.candidate_card)
                self.running_hard += int(self.candidate_card)

    def hand_summary(self):
        out_list = []
        for count, i in enumerate(self.hand,0):
            self.candidate_card = self.hand[count]
            out_list.append(beautify(self.candidate_card))
        return out_list

if __name__ == "__main__":
    h = hand_eval(p1)
