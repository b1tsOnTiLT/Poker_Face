#The betdic{} for cases where hero bets/calls/raises-has the pot after the hero has bet
#handle ',' in bet amounts
import re
from dataclasses import dataclass
@dataclass
class Parser:
        fn='new1.txt'
        Small_Blind = None
        Big_Blind = None
        Player_name = None
        Hands = None
        Round_folded = None
        pot = 0.0
        preflop_bet = None
        flop_bet = None
        turn_bet = None
        river_bet = None
        blind = None
        lines=open(fn, 'r', errors='replace').readlines()

        def __post_init__(self):
             
            for line in self.lines:
                p='^PokerStars Hand'
                if not re.match(p,line):
                    continue
                blind=r'₹(\d+)'
                blinds=re.findall(blind,line)
                self.Small_Blind,self.Big_Blind=blinds
                print(self.Small_Blind,self.Big_Blind)
         
            for line in self.lines:
                    p='Dealt'
                    if re.search(p,line)==None:
                        continue
                    self.Player_name=re.findall(r'to(.+)\[',line)[0].strip()
                    p=r'\[([a-zA-Z0-9]+).([a-zA-Z0-9]+)\]'
                    self.Hands=re.search(p,line)
                    self.Hands=self.Hands.groups()
                    self.Round_folded = 'PREFLOP'
                    self.pot = int(self.Big_Blind) + int(self.Small_Blind)
                   

        def betlog(self, street):
             betdic = {}
             i=0
             p=rf'^\*+\W+{street}'
             q=r'₹(\d+)'
             for idx,line in enumerate(self.lines):
                   if not re.match(p,line):
                         continue
                   elif re.match(p,line):
                         for subline in self.lines[idx+1:]:
                            if re.match('^\*+',subline):
                                break
                            
                            elif 'calls' in subline:
                                self.pot += float(re.findall(q,subline)[0])
                                        
                                if self.Player_name in subline:
                                    i += 1
                                    betdic[f"call{i}"] = [float(re.findall(q,subline)[0]), int(self.pot)]
                            elif 'bets' in subline:
                                self.pot += float(re.findall(q,subline)[0])
                                if self.Player_name in subline:
                                    i += 1
                                    betdic[f"bet{i}"] = [float(re.findall(q,subline)[0]), int(self.pot)]
                            elif 'raises' in subline:   
                                    
                                self.pot += float(re.findall(r'to\W+₹\W*(\d+)',subline)[0])
                                if self.Player_name in subline:
                                    i += 1
                                    betdic[f"raise{i}"] = [float(re.findall(r'to\W+₹\W*(\d+)',subline)[0]), int(self.pot)]
                                        
                            elif 'folds' in subline and self.Player_name in subline:
                                self.Round_folded = street
                                break

             return(betdic)  

        def PREFLOP(self):
            self.preflop_bet = self.betlog('HOLE')
            return self.preflop_bet
            

        def FLOP(self):
            self.flop_bet = self.betlog('FLOP')
            return self.flop_bet
            

        def TURN(self):
            self.turn_bet = self.betlog('TURN')
            return self.turn_bet
            

        def RIVER(self):
            self.river_bet = self.betlog('RIVER')
            return self.river_bet
           
            



