import eval7,pprint
import random 
from parser import Parser
from dataclasses import dataclass



#eval7.evaluate(hand)  Deck-deal(),shuffle()  eval7.Card('As') eval7.handtype(score), Deck-remove()
#assuming number of active players right now is fixed at 3.


@dataclass
class Poteq():
    villains=3
    """flop=list(Parser().Comm_cards.get('FLOP',None))
    turn=list(Parser().Comm_cards.get('TURN',None))
    river=list(Parser().Comm_cards.get('RIVER',None))

    Hero_Hand=list(Parser().Hands)
    """
    flop=[]
    turn=[]
    river=[]
    Hero_Hand=['As','Ad']
    current_hands=Hero_Hand+flop+turn+river
    board=[eval7.Cards(s) for s in flop+turn+river]
    itr=1000



    def poteq(self):
        
        curr_cards=len(self.current_hands)-2
        deck=eval7.Deck()
        deck.cards.remove(eval7.Card(s) for s in self.current_hands)
        win=0
        tie=[]
        
        
        for i in range(self.itr):
           villian_scores=[]
           villian_hand=[]
           deck.shuffle()
           for i in range(self.villains):
                villian_hand.append(deck.deal(2))
           self.board+=deck.deal(5-curr_cards)
           for i in range(self.villains):
                
                villian_scores.append(eval7.evaluate([j for j in villian_hand]+self.board))
           Hero_score=eval7.evaluate(eval7.Card(self.Hero_Hand)+self.board)
           if Hero_score>max(villian_scores):
                win+=1
           elif Hero_score==max(villian_scores):
                t=0
                for i in villian_scores:
                    if i==Hero_score:
                        t+=1
                tie.append(t)
        final_score=win+ [1/t for t in tie]
        print(final_score/self.itr*100)
        
        

            
            



                
















    







