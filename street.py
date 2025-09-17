import re
from parser import Parser
from poteq import Poteq


def finalcalc(blob):

    PREFLOP={}
    FLOP={}
    TURN={}
    RIVER={}

    parser=Parser(blob)
    preflop=parser.PREFLOP()
    flop=parser.FLOP()
    turn=parser.TURN()
    river=parser.RIVER()
    if not preflop and not flop:
        print('Didnt play hand')
    else:
        if preflop:
            for bets in preflop:
                q=r'raise.+'
                numvill=preflop[bets][2]
                pot_odds=float(preflop[bets][0])*100/float(preflop[bets][1])
                if(re.match(q,bets)):
                    numvill=preflop[bets][3]
                    pot_odds=float(preflop[bets][0])*100/(float(preflop[bets][2])-float(preflop[bets][1])+float(preflop[bets][0]))

                
                poteq=Poteq(numvill,[],blob)
                PREFLOP[bets]=(round(poteq.poteq(),2),round(pot_odds,2))

        if flop:
            for bets in flop:
                q=r'raise.+'
                numvill=flop[bets][2]
                pot_odds=float(flop[bets][0])*100/float(flop[bets][1])
                if(re.match(q,bets)):
                    numvill=flop[bets][3]
                    pot_odds=float(flop[bets][0])*100/(float(flop[bets][2])-float(flop[bets][1])+float(flop[bets][0]))
                poteq=Poteq(numvill,parser.Comm_cards['FLOP'],blob)
                FLOP[bets]=(round(poteq.poteq(),2),round(pot_odds,2))

        if turn:
            for bets in turn:
                q=r'raise.+'
                numvill=turn[bets][2]
                pot_odds=float(turn[bets][0])*100/float(turn[bets][1])
                if(re.match(q,bets)):
                    numvill=turn[bets][3]
                    pot_odds=float(turn[bets][0])*100/(float(turn[bets][2])-float(turn[bets][1])+float(turn[bets][0]))
                poteq=Poteq(numvill,parser.Comm_cards['TURN'],blob)
                TURN[bets]=(round(poteq.poteq(),2),round(pot_odds,2))

        if river:
            for bets in river:
                q=r'raise.+'
                numvill=river[bets][2]
                pot_odds=float(river[bets][0])*100/float(river[bets][1])
                if(re.match(q,bets)):
                    numvill=river[bets][3]
                    pot_odds=float(river[bets][0])*100/(float(river[bets][2])-float(river[bets][1])+float(river[bets][0]))
                poteq=Poteq(numvill,parser.Comm_cards['RIVER'],blob)
                RIVER[bets]=(round(poteq.poteq(),2),round(pot_odds,2))

        print(PREFLOP,FLOP,TURN,RIVER)#[pot_eq,pot_odds]
        print(preflop,flop,turn,river)


fn=input('Enter filename')
fh=open(fn,'r').readlines()

q='\^*+\W+\#\W+(\d+)'

for idx,line in enumerate(fh):
    if re.match(q,line):
        Hand_num=re.findall(q,line)[0]
        print('Hand:',Hand_num)
        for ind,subline in enumerate(fh[idx+1:],start=idx+1):
            if re.match(q,subline) and re.findall(q,subline)[0]!=Hand_num:
                break

        finalcalc(fh[idx+1:ind])




