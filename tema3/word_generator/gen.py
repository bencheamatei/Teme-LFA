class generator:
    def __init__(self,filename):
        self.non_terminals=[]
        self.terminals=[]
        self.start=None
        self.productions={}
        self.ans=set()
        self.get_input(filename)

    def get_input(self,filename):
        with open(filename) as fin:
            lines=[line.strip() for line in fin.readlines() if line.strip()] 

        self.non_terminals=list(lines[0].split())
        self.terminals=list(lines[1].split())
        self.start=lines[2]
        for i in range(3,len(lines)):
            x,y=lines[i].split("->")
            x=x.strip()
            y=y.strip()
            if x not in self.productions:
                self.productions[x]=[]
            for z in y.split("|"):
                z=z.strip()
                if z!="$":
                    self.productions[x].append(z)
                else:
                    self.productions[x].append("")

    def generate_word(self,n,curr):
        count_t=sum(1 for x in curr if x in self.terminals)
        if count_t>n:
            return 
        
        variabile=False 
        for i in range(len(curr)):
            if curr[i] in self.terminals:
                continue 
            variabile=True 
            if curr[i] not in self.productions:
                continue

            for x in self.productions[curr[i]]:
                self.generate_word(n,curr[:i]+x+curr[i+1:])
            break 
        
        if not variabile and len(curr)==n:
            self.ans.add(curr)

    def get_ans(self,n):
        self.generate_word(n,self.start)
        return self.ans


if __name__=="__main__":
    gr=generator("./gr.in")
    n=int(input())
    print(gr.get_ans(n))