class grammar:
    def __init__(self,filename):
        self.non_terminals=set()
        self.terminals=set()
        self.start=None
        self.productions={}
        self.current_count=0
        self.get_input(filename)
        self.to_chomsky()

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
                    
    def create_variable(self):
        p="Q"+str(self.current_count)+"_"
        self.current_count+=1
        self.non_terminals.add(p)
        return p
    
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
    
    def to_start(self):
        for (_, ys) in self.productions.items():
            for y in ys:
                if self.start in self.tokenize(y):
                    new_start=self.create_variable()
                    self.non_terminals.add(new_start)
                    self.productions[new_start]=[self.start]
                    self.start=new_start
                    return

    def to_term(self):
        terms={}
        new_productions={} 
        for (care, ys) in self.productions.items():
            if care not in new_productions:
                new_productions[care]=[]

            for y in ys:
                y=self.tokenize(y)
                if len(y)<2:
                    new_productions[care].append("".join(y))
                    continue 
                running=[]
                for x in y:
                    if x in self.terminals:
                        if x not in terms:
                            aux=self.create_variable()
                            terms[x]=aux
                            new_productions[aux]=[x]
                        running.append(terms[x]) 
                    else:
                        running.append(x)
                new_productions[care].append("".join(running))  

        self.productions=new_productions

    def to_bin(self):
        new_productions={}
        deja={} # aici ca sa nu am duplicate gen Q0 -> AB si  Q1 -> AB

        for (care,ys) in self.productions.items():
            if care not in new_productions:
                new_productions[care]=[]

            for y in ys:
                y=self.tokenize(y)
                if len(y)<=2:
                    new_productions[care].append("".join(y))
                    continue 
                
                if y[0]+"-"+y[1] not in deja:
                    aux=self.create_variable()
                    deja[y[0]+"-"+y[1]]=aux 
                    new_productions[aux]=[y[0]+y[1]]
                last=deja[y[0]+"-"+y[1]]

                for i in range(2,len(y)-1):
                    if last+"-"+y[i] not in deja:
                        aux=self.create_variable()
                        deja[last+"-"+y[i]]=aux 
                        new_productions[aux]=[last+y[i]]
                    last=deja[last+"-"+y[i]]
                new_productions[care].append(last+y[-1])
        self.productions=new_productions
                    

    def to_del(self):
        new_productions={}
        nullable=set()
        gasite=True
        while gasite:
            gasite=False
            for (care,ys) in self.productions.items():
                for y in ys:
                    y=self.tokenize(y)
                    if len(y)==0:
                        if care not in nullable:
                            nullable.add(care)
                            gasite=True 
                    else:
                        ok=True 
                        for x in y:
                            if x not in nullable:
                                ok=False
                                break 
                        if ok:
                            if care not in nullable:
                                nullable.add(care)
                                gasite=True 

        for (care,ys) in self.productions.items():
            if care not in new_productions:
                new_productions[care]=[]
            for y in ys:
                y=self.tokenize(y)
                if len(y)==0:
                    continue 
                null_pos=[i for (i,t) in enumerate(y) if t in nullable]
                for mask in range(1<<len(null_pos)):
                    yt=list(y) 
                    for bit, pos in enumerate(null_pos):
                        if mask&(1<<bit):
                            yt[pos]=None 
                    res="".join(x for x in yt if x is not None)
                    if res and res not in new_productions[care]:
                        new_productions[care].append(res)
        self.productions=new_productions


    def to_unit(self):
        unit_pairs=set()
        for A in self.non_terminals:
            unit_pairs.add((A, A))

        gasit=True
        while gasit:
            gasit = False
            for (A, B) in list(unit_pairs):
                if B not in self.productions:
                    continue
                for y in self.productions[B]:
                    y=self.tokenize(y)
                    if len(y)==1 and y[0] in self.non_terminals:
                        C=y[0]
                        if (A, C) not in unit_pairs:
                            unit_pairs.add((A, C))
                            gasit=True

        new_productions={A: [] for A in self.productions}
        for (A, B) in unit_pairs:
            if B not in self.productions:
                continue
            for y in self.productions[B]:
                y=self.tokenize(y)
                is_unit=len(y)==1 and y[0] in self.non_terminals
                if not is_unit and "".join(y) not in new_productions[A]:
                    new_productions[A].append("".join(y))

        self.productions = new_productions 

    def to_chomsky(self):
        self.to_start()
        self.to_term()
        self.to_bin()
        self.to_del()
        self.to_unit()
        self.productions={k:val for (k,val) in self.productions.items() if len(val)>0}

    def print_grammar(self):
        print(self.start)
        for x in self.productions:
            print(x, " | ".join(self.productions[x]), sep=" -> ")

if __name__=="__main__":
    gr=grammar("./tema3/chomsky/gr.in")
    gr.print_grammar()
