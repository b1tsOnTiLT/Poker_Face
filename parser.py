#The betdic{} for cases where hero bets/calls/raises-has the pot after the hero has bet
#handle ',' in bet amounts
#def __init__(self,linest:int,plyr_list:list,last_line:int):
#return self.pl,self.endline
import re
from dataclasses import dataclass
from numheroes import Villain

class Parser:
        
        def __init__(self,Hand_Blob):
            self.Small_Blind = None
            self.Big_Blind = None
            self.Player_name = None
            self.Hands = None
            self.Round_folded = None
            self.pot = 0.0
            self.preflop_bet = None
            self.flop_bet = None
            self.turn_bet = None
            self.river_bet = None
            self.blind = None
            self.lines=Hand_Blob
            self.Comm_cards={}
            self.start_line=None
            self.player_list=[]
                
            for line in self.lines:
                p='^PokerStars Hand'
                if not re.match(p,line):
                    continue
                blind=r'₹(\d+)'
                blinds=re.findall(blind,line)
                self.Small_Blind,self.Big_Blind=blinds
                
         
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

            for line in self.lines:
                    p=r'^\*+\W+FLOP'
                    q=r'([2-9AKQJdhsc]{2,3})'
                    if re.match(p,line):
                        self.Comm_cards['FLOP']=tuple(re.findall(q,line))
                    p=r'^\*+\W*TURN'
                    if re.match(p,line):
                        self.Comm_cards['TURN']=tuple(re.findall(q,line))
                    p=r'^\*+\W*RIVER'
                    if re.match(p,line):
                        self.Comm_cards['RIVER']=tuple(re.findall(q,line))
            for line in self.lines:
                    if line.startswith('*'):
                        break
                    elif line.startswith('Seat'):
                        p=r'\:\W+(.+)\W+\('
                        name=re.findall(p,line)[0].strip()
                        self.player_list.append(name)
            
        
        def num_villians(self,curr_ind):
           
            if self.start_line is None:
               self.player_list, self.start_line = Villain(0, self.player_list, curr_ind,self.lines).num_villains()
            else:
                self.player_list, self.start_line = Villain(self.start_line, self.player_list, curr_ind,self.lines).num_villains()
                

        def betlog(self, street):
             betdic = {}
             i=0
             p=rf'^\*+\W+{street}'
             q=r'₹(\d+\.?\d*)'
             for idx,line in enumerate(self.lines):
                   if not re.match(p,line):
                         continue
                   elif re.match(p,line):
                         for ind,subline in enumerate(self.lines[idx+1:],start=idx+1):
                            if re.match('^\*+',subline):
                                
                                break
                            
                            elif 'calls' in subline:
                                self.pot += float(re.findall(q,subline)[0])
                                        
                                if self.Player_name in subline:
                                    i += 1
                                    self.num_villians(ind)
                                    betdic[f"call{i}"] = [float(re.findall(q,subline)[0]), int(self.pot), len(self.player_list)]
                            elif 'bets' in subline:
                                self.pot += float(re.findall(q,subline)[0])
                                if self.Player_name in subline:
                                    i += 1
                                    self.num_villians(ind)
                                    betdic[f"bet{i}"] = [float(re.findall(q,subline)[0]), int(self.pot),len(self.player_list)]
                            elif 'raises' in subline:   
                                    
                                self.pot += float(re.findall(r'to\W+₹\W*(\d+\.?\d*)',subline)[0])
                                if self.Player_name in subline:
                                    i += 1
                                    self.num_villians(ind)
                                    betdic[f"raise{i}"] = [float(re.findall(r'raises\W+₹\W*(\d+\.?\d*)',subline)[0]),float(re.findall(r'to\W+₹\W*(\d+\.?\d*)',subline)[0]), int(self.pot),len(self.player_list)]
                                        
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
           
           

if __name__ == "__main__":
    new=Parser()
    print(new.PREFLOP())
    print(new.FLOP())
    print(new.TURN())
    print(new.RIVER())
    print("This is considering the worst case scenario(most callers),Bet List is:[Bet,Pot if Bet, Villains]-for each street,each bet ")

