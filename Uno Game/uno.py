from classes import *

def check_win(user,pc):
    if user.cards_in_hand()==0:
        return False,user
    if pc.cards_in_hand()==0:
        return False,pc
    else:
        return True,user
def card_effect(deck,discard,card,p1,p2):
    def change_color():
        colors = ["Red","Yellow","Green","Blue"]
        color = colors[random.randrange(4)]
        print("Changing color to..",color)
        return color
        
    if card.name=="Skip" or card.name=="Reverse":
        return p1
    elif card.name=="Draw":
        if card.color=="Special":
            if p1.name=="user":
                color = input("What color do u want to change to?\n> ")
            elif p1.name=="pc":
                color = change_color()
            card.color = color
            for i in range(4):
                if deck.cards_in_deck()!=0:
                    p2.add_card(deck.deal_card())
                elif deck.cards_in_deck()==0 and discard.cards_in_deck()==0:
                    break
                else:
                    deck,discard = discard_to_deck(deck,discard)
                    p2.add_card(deck.deal_card())
        else:
            for i in range(2):
                if deck.cards_in_deck()!=0:
                    p2.add_card(deck.deal_card())
                elif deck.cards_in_deck()==0 and discard.cards_in_deck()==0:
                    break
                else:
                    deck,discard = discard_to_deck(deck,discard)
                    p2.add_card(deck.deal_card())
        return p2
    elif card.name=="Wild":
        if p1.name == "user":
            color = input("What color do u want to change to? (Blue,Red,Yellow,Green)\n> ")
        elif p1.name=="pc":
            color = change_color()
        card.color = color
    return p2
def clear():
    return os.system('cls')
def discard_to_deck(deck,discard):
    deck.deck = discard.deck
    deck.shuffle()
    discard.reset_deck()
    return deck,discard
def random_start(p1,p2):
    i = random.randrange(2)
    if i==0:
        return p1
    return p2
def play_card(player,card_on_pile,deck,discard):
    if player.name=="user":
        print("The card on top is:", card_on_pile, "\n")
        print("Your cards are:")
        for i in range(len(player.hand)):
            print(f"{i+1} -> {player.hand[i]}")
        print()
        try:
            index = input("Type the number of the card you want to select, (type 's' if u need to seek for a new one):\n> ")
            if 1<=int(index)<=len(player.hand):
                index=int(index)-1
            else:
                print("Type a number from the list")
                return -1
        except ValueError:
            if index=="s":
                if deck.cards_in_deck()!=0:
                    player.add_card(deck.deal_card())
                elif deck.cards_in_deck()==0 and discard.cards_in_deck()==0:
                    print("Play a card!!!")
                    return -1
                else:
                    deck,discard = discard_to_deck(deck,discard)
                    player.add_card(deck.deal_card())
                return -1
            print("Type a number from the list.")
            return -1
        card = player.hand[int(index)]
        if is_card_valid(card,card_on_pile):
            player.del_card(card)
            return card
        else:
            return -1
    elif player.name=="pc":
        print("PC",player)
        return pc_turn(player,card_on_pile,deck,discard)
    else:
        raise Exception("...")
def non_turn(turn,user,pc):
    if turn==user:
        return pc
    else:
        return user
def is_card_valid(card_selected,card_on_pile):
    if card_selected.color==card_on_pile.color or card_selected.color=="Special"\
        or card_selected.name==card_on_pile.name:
        return True
    return False
def card_choice(pc,card_on_pile,deck,discard):
    valid = []
    for card in pc.hand:
        if is_card_valid(card,card_on_pile):
            valid.append(card)
    if len(valid)==0:
        if deck.cards_in_deck()!=0:
            pc.add_card(deck.deal_card())
        else:
            deck,discard = discard_to_deck(deck,discard)
            pc.add_card(deck.deal_card())
        return -1
    return valid[random.randrange(len(valid))]
def pc_turn(pc,card_on_pile,deck,discard):
    card = -1
    while card==-1:
        card = card_choice(pc,card_on_pile,deck,discard)
    pc.del_card(card)
    return card
def main():
    deck,discard = Deck(),Deck()
    deck.start_deck()
    deck.shuffle()
    user = Player("user",deck.create_hand())
    pc = Player("pc",deck.create_hand())
    turn = random_start(pc,user)
    card = deck.deal_card()
    discard.receive_card(card)
    while card.color=="Special":
        card = deck.deal_card()
        discard.receive_card(card)
    flag = True
    while flag:
        no_turn = non_turn(turn,user,pc)
        c=-1
        while c==-1:
            clear()
            print(f"PC {pc}")
            c = play_card(turn,card,deck,discard)
        discard.receive_card(c)
        turn = card_effect(deck,discard,c,turn,no_turn)
        card = c
        flag,winner = check_win(user,pc)
    if winner==pc:
        print("U suck!")
    if winner==user:
        print("Congratulations, u won!!!")
    return

if __name__ == '__main__':
    main()