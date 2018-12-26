import random

def deck_gen(num_decks):
    deck = []
    class suit_gen:
        def __init__(self, suit):
            self.count = 2
            self.prefix = suit[0]
            self.card_product()      
        def card_product(self):
            deck.append([self.prefix,"ace"])        
            while self.count < 11:
                deck.append([self.prefix,str(self.count)])
                self.count += 1
            deck.append([self.prefix,"jack"])
            deck.append([self.prefix,"queen"])
            deck.append([self.prefix,"king"])
    cb = suit_gen("clubs")
    sp = suit_gen("spades")
    dm = suit_gen("diamonds")
    hr = suit_gen("hearts")
    unshuffled_deck = []
    for i in range(0,num_decks):
        unshuffled_deck += deck
    random.shuffle(unshuffled_deck)
    final_deck = unshuffled_deck
    return final_deck

if __name__ == "__main__":
    deck_gen(8)