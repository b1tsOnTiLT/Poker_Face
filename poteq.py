#Note: poteq is caluclated at each bet indiviudally-this class needs to take the betdic as input.
import eval7,pprint
import random 
from parser import Parser
from dataclasses import dataclass
#remove generator



#eval7.evaluate(hand)  Deck-deal(),shuffle()  eval7.Card('As') eval7.handtype(score), Deck-remove()



class Poteq():
    
    def __init__(self,villains,board_rn):
        self.active_villains=villains
        self.curr_board=board_rn
        self.Hero_Hand=list(Parser().Hands)
        self.Hero_Handr=[]
        for s in self.Hero_Hand:
            self.Hero_Handr.append(eval7.Card(s))    
        self.board=[]
        self.current_hands=self.Hero_Hand+self.curr_board
        for s in self.curr_board:
            if s is None:
                break
            self.board.append(eval7.Card(s))
        self.itr=10000



    def poteq(self):
        
        curr_cards=len(self.board)
        win=0
        tie=[]
        board=self.board.copy()
        
        
        
        for i in range(self.itr):
            deck=eval7.Deck()
            for card in self.current_hands:
                deck.cards.remove(eval7.Card(card))
            board=self.board.copy()
            

            
            villian_scores=[]
            villian_hand=[]
            deck.shuffle()
            for i in range(self.active_villains):
                    villian_hand.append(deck.deal(2))
            board+=deck.deal(5-curr_cards)
            for i in range(self.villains):
                    
                villian_board=board+villian_hand[i]
                villian_scores.append(eval7.evaluate(villian_board))
            Hero_score=eval7.evaluate(self.Hero_Handr+board)
            if Hero_score>max(villian_scores):
                        win+=1
            elif Hero_score==max(villian_scores):
                        t=0
                        for i in villian_scores:
                            if i==Hero_score:
                                t+=1
                        tie.append(t)
        final_score=win
        for t in tie:
                final_score+=1/t
        print(final_score*100/self.itr)
           
        




            
    