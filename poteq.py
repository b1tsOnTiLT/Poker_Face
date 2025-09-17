#Note: poteq is caluclated at each bet indiviudally-this class needs to take the betdic as input.
import eval7,pprint
import random 
from parser import Parser
from dataclasses import dataclass
#remove generator



#eval7.evaluate(hand)  Deck-deal(),shuffle()  eval7.Card('As') eval7.handtype(score), Deck-remove()



class Poteq():
    
    def __init__(self,villains,board_rn,Hand_blob):
        self.Hb=Hand_blob
        self.active_villains=villains-1
        self.curr_board=list(board_rn) if board_rn else []
        self.Hero_Hand=list(Parser(self.Hb).Hands)
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
                if card is not None:
                    deck.cards.remove(eval7.Card(card))
            board=self.board.copy()
            

            
            villian_scores=[]
            villian_hand=[]
            deck.shuffle()
            for i in range(self.active_villains):
                    villian_hand.append(deck.deal(2))
            board+=deck.deal(5-curr_cards)
            for i in range(self.active_villains):
                    
                villian_board=list(board)+list(villian_hand[i])
                villian_scores.append(eval7.evaluate(villian_board))
            Hero_score=eval7.evaluate(list(self.Hero_Handr)+list(board))
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
        return(final_score*100/self.itr)
           
        




            
    