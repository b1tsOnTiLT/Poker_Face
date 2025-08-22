class Parser:
    def __init__(self, fn):
        self.Small_blind = None
        self.Big_blind = None
        self.Player_name = None
        self.H1 = None
        self.H2 = None
        self.Round_folded = None
        self.preflop_bet = None
        self.flop_bet = None
        self.turn_bet = None
        self.river_bet = None
        self.blind = None
        self.pot = None
        
          
        fh = open(fn, 'r', errors='replace')
        self.lines = fh.readlines()
        for line in self.lines:
            if not line.startswith('PokerStars Hand'):
                continue
            self.Small_blind, self.Big_blind = line.split('(')[1].split('I')[0].split('/')
            self.Big_blind = self.Big_blind.split('₹')[1]
            self.Small_blind = self.Small_blind.split('₹')[1]

        for line in self.lines:
            if not 'Dealt' in line:
                continue
            self.Player_name = line.split('to')[1].split('[')[0].strip()
            Hand = line.split('to')[1].split('[')[1].split(']')[0]
            self.H1 = Hand.split(' ')[0]
            self.H2 = Hand.split(' ')[1]
            self.Round_folded = 'PREFLOP'
        self.pot = int(self.Big_blind) + int(self.Small_blind)
    
        self.isblind()
    
    def isblind(self):
            for line in self.lines:
                if 'posts small blind' in line  and self.Player_name in line:
                    self.blind = 'small blind'
                elif 'posts big blind' in line  and self.Player_name in line:
                    self.blind = 'big blind'
                

    def betlog(self, street):
        
        betdic = {}
        count=0
        i=0
        
        for line in self.lines:
            if street not in line:
              count+=1
            elif line.startswith('*') and  street in line:
              break
        
        count1=0

        for line in self.lines:
                if count1 < count:
                    count1+=1
                    continue
                elif line.startswith('*') and street in line:
                    continue
                elif line.startswith('*') and street not in line:
                    break
                elif 'calls' in line:
                   self.pot += float(line.split('calls')[1].split('₹')[1].split()[0])
                  
                   if self.Player_name in line:
                        i += 1
                        betdic[f"bet{i}"] = [float(line.split('calls')[1].split('₹')[1].split()[0]), int(self.pot)]
                elif 'bets' in line:
                   self.pot += float(line.split('bets')[1].split('₹')[1].split()[0])
                  
                   if self.Player_name in line:
                        i += 1
                        betdic[f"bet{i}"] = [float(line.split('bets')[1].split('₹')[1].split()[0]), int(self.pot)]
                elif 'raises' in line:   
                   
                   self.pot += float(line.split('to')[1].split('₹')[1].split()[0])
                   if self.Player_name in line:
                        i += 1
                        betdic[f"bet{i}"] = [float(line.split('to')[1].split('₹')[1].split()[0]), int(self.pot)]
                elif 'checks' in line and self.Player_name in line and self.Big_blind and street == 'HOLE':
                        
                        
                        betdic[f"bet{i}"] = [self.Big_blind, int(self.pot)]
                elif 'folds' in line and self.Player_name in line:
                    self.Round_folded = street
                    break
                  
                
       
        return betdic  

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





        
    


