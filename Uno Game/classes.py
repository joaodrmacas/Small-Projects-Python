import random
import os

class Card:
    all = []
    def __init__(self,name,color="Special") -> None:
        self.name = name
        self.color = color

        self.all.append(self)
    
    def __repr__(self) -> str:
        return f"({self.color}-{self.name})"
class Deck:

    def __init__(self) -> None:
        self.deck = []

    def start_deck(self):
        colors = ["Red","Blue","Green","Yellow"]
        names = {"0":1,"1":2,"2":2,"3":2,"4":2,"5":2,"6":2,"7":2,"8":2,"9":2,"Skip":2,"Draw":2,"Reverse":2}
        special = {"Wild":4, "Draw":4}
        for color in colors:
            for name in names:
                for i in range(names.get(name)):
                    self.deck.append(Card(name,color))
        for card in special:
            for i in range(special.get(card)):
                self.deck.append(Card(card))

    def reset_deck(self):
        self.deck = []

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def receive_card(self,card):
        return self.deck.append(card)

    def cards_in_deck(self):
        return len(self.deck) 

    def create_hand(self):
        l = []
        for i in range(7):
            l.append(self.deal_card())
        return l    
class Player:
    def __init__(self,name,hand) -> None:
        self.name = name
        self.hand = hand

    def __repr__(self) -> str:
        return f"has {len(self.hand)} cards left"

    def cards_in_hand(self):
        return len(self.hand)
    
    def add_card(self,card):
        if self.name=="user":
            print("Drawing a card..")
        self.hand.append(card)

    def del_card(self,card_del):
        for i in range(len(self.hand)):
            if self.hand[i] == card_del:
                del self.hand[i]
                return