import re#line:the current hero bet/call line, last_line-where num heroes was checked till last time
class Villain():
    
    def __init__(self,linest:int,plyr_list:list,last_line:int,curr_inlines):
        self.pl = plyr_list
        self.lines=curr_inlines
        self.stline=linest
        self.endline=last_line
        

    def num_villains(self):

        
        for line in self.lines[self.stline:self.endline]:
            if 'folds' in line:
                
                pn=re.findall(r'(.+)\:\W+folds',line)[0].strip()
                
                if pn in self.pl:
                    self.pl.remove(pn)
                    
                    

        return self.pl,self.endline
    


            
            
        
        
        



       