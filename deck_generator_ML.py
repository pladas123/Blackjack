import random

def deck_gen(num_decks):
    deck = []
    class suit_gen:
        def __init__(self):
            self.count = 2
            self.card_product()      
        def card_product(self):
            deck.append("a")        
            while self.count < 11:
                deck.append(int(self.count))
                self.count += 1
            deck.append(10)
            deck.append(10)
            deck.append(10)
    for j in range(0,4):
        s = suit_gen()
    unshuffled_deck = []
    for i in range(0,num_decks):
        unshuffled_deck += deck
    random.shuffle(unshuffled_deck)
    final_deck = unshuffled_deck
    #print(len(final_deck))
    return final_deck

if __name__ == "__main__":
    print(deck_gen(8))