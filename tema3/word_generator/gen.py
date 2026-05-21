class generator:
    def __init__(self,filename):
        self.non_terminals=set()
        self.terminals=set()
        self.start=None
        self.productions={}
        self.current_count=0
        self.ans=set()
        self.get_input(filename)

    def get_input(self,filename):
        with open(filename) as fin:
            lines=[line.strip() for line in fin.readlines() if line.strip()] 

        self.non_terminals=set(lines[0].split())
        self.terminals=set(lines[1].split())
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

    def tokenize(self,target):
        pp=[]
        i=0
        aux=sorted(list(self.terminals|self.non_terminals),reverse=True, key=len)
        while i<len(target):
            gasit=False
            for x in aux:
                if target.startswith(x,i):
                    pp.append(x)
                    i+=len(x)
                    gasit=True 
                    break 
            if not gasit:
                pp.append(target[i])
                i+=1
        return pp

    def generate_word(self,n,curr):
        # count_t=sum(1 for x in curr if x in self.terminals)
        new_curr=self.tokenize(curr)
        count_t=sum(1 for x in new_curr if x in self.terminals)
        if count_t>n:
            return 
        
        variabile=False 
        for i in range(len(new_curr)):
            if new_curr[i] in self.terminals:
                continue 
            variabile=True 
            if new_curr[i] not in self.productions:
                continue

            for x in self.productions[new_curr[i]]:
                self.generate_word(n,"".join(new_curr[:i])+x+"".join(new_curr[i+1:]))
            break 
        
        if not variabile and len(curr)==n:
            self.ans.add(curr)

    def get_ans(self,n):
        self.generate_word(n,self.start)
        return self.ans


if __name__=="__main__":
    gr=generator("./tema3/word_generator/gr.in")
    n=int(input())
    print(gr.get_ans(n))