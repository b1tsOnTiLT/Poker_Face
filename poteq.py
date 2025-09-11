import eval7,pprint
import random 
from parser import Parser
from dataclasses import dataclass
#remove generator



#eval7.evaluate(hand)  Deck-deal(),shuffle()  eval7.Card('As') eval7.handtype(score), Deck-remove()
#assuming number of active players right now is fixed at 3.


@dataclass
class Poteq():
    villains=None
    flop=list(Parser().Comm_cards.get('FLOP',[]))
    turn=list(Parser().Comm_cards.get('TURN',[]))
    river=list(Parser().Comm_cards.get('RIVER',[]))
    if(turn==[]):
          curr_board=flop
    elif(river==[]):
          curr_boar=turn
    elif(river!=[]):
          curr_board=river
    
    
          

    Hero_Hand=list(Parser().Hands)
    
    
    Hero_Hand=['As','Ad']
    Hero_Handr=[]
    for s in Hero_Hand:
          Hero_Handr.append(eval7.Card(s))
          
    board=[]
    current_hands=Hero_Hand+curr_board
    for s in curr_board:
        if s is None:
               break
        board.append(eval7.Card(s))
    itr=10000



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
            for i in range(self.villains):
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
           
        

new=Poteq()
new.poteq()


            
    