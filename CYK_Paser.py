class Dictlist(dict):
    
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)


class production_rule(object):
    
    result = None
    p1 = None
    p2 = None
    
    #Parameters:
    #   Result: String
    #   p1: Production rule (left child of the production rule)
    #   p2: Production rule (right child of the production rule)
    def __init__(self,result,p1,p2):
        self.result = result
        self.p1 = p1
        self.p2 = p2
    
    #Returns the result of the production rule, VP, S, NP... 
    @property
    def get_type(self):
        return self.result
    
    #Returns the left child of the production rule
    @property
    def get_left(self):
        return self.p1
    
    #Returns the right child of the production rule
    @property
    def get_right(self):
        return self.p2

class Cell(object):
    productions = []
    
    
    #Parameters:
    #   Productions: List of production rules
    
    def __init__(self, productions=None):
        if productions is None:
            self.productions = []
        else:
            self.productions = productions
            
    def add_production(self, result,p1,p2):
        self.productions.append(production_rule(result,p1,p2))
    
    def set_productions(self, p):
        self.productions = p
    
    @property
    def get_types(self):
        types = []
        for p in self.productions:
            types.append(p.result)
        return types
    @property
    def get_rules(self):       
        return self.productions


class Grammar(object):
    
    grammar_rules = Dictlist()
    parse_table = None
    length = 0
    tokens = []
    number_of_trees = 0
    
    #Parameters:
    #   Filename: file containing a grammar
    
    def __init__(self):
        self.grammar_rules = Dictlist()
        self.parse_table = None
        self.length = 0
        for line in open("rules.txt"):
            a, b = line.split("->")
            rules = b.split("|")
            for c in rules:
                self.grammar_rules[c.rstrip().strip()]=a.rstrip().strip()
        
        if len(self.grammar_rules) == 0:
            raise ValueError("No rules found in the grammar file")
        
    def apply_rules(self,t):
        try:
            return self.grammar_rules[t]
        except KeyError as r:
            return None
            
    #Parse a sentence (string) with the CYK algorithm   
    def parse(self,sentence):
        self.number_of_trees = 0
        self.tokens = sentence.lower().split()
        self.length = len(self.tokens)
        if self.length < 1:
            raise ValueError("The sentence could no be read")
        self.parse_table = [ [Cell() for x in range(self.length - y)] for y in range(self.length) ]
        
         #Process the first line
        
        for x, t in enumerate(self.tokens):
            
            r = self.apply_rules(t)
            if r == None:
                raise ValueError("The word " + str(t) + " is not in the grammar")
            else:
                for w in r: 
                    self.parse_table[0][x].add_production(w,production_rule(t,None,None),None)
        
        
        #Run CYK-Parser
        
        
        for l in range(2,self.length+1):
            for s in range(1,self.length-l+2):
                for p in range(1,l-1+1):
                    
                    t1 = self.parse_table[p-1][s-1].get_rules
                    t2 = self.parse_table[l-p-1][s+p-1].get_rules
                            
                    for a in t1:
                        for b in t2:
                            r = self.apply_rules(str(a.get_type) + " " + str(b.get_type))
                                    
                            if r is not None:
                                for w in r:
                                    # print('Applied Rule: ' + str(w) + '[' + str(l) + ',' + str(s) + ']' + ' --> ' + str(a.get_type) + '[' + str(p) + ',' + str(s) + ']' + ' ' + str(b.get_type)+ '[' + str(l-p) + ',' + str(s+p) + ']')
                                    self.parse_table[l-1][s-1].add_production(w,a,b)
                               
        self.number_of_trees = len(self.parse_table[self.length-1][0].get_types)
        if  self.number_of_trees > 0:
            for cell in self.parse_table[self.length-1]:
                for a in cell.get_types:
                    if a == 'K':
                        return True
            return False
        else:
            return False
        
        
    #Returns a list containing the parent of the possible trees that we can generate for the last sentence that have been parsed
    def get_trees(self):
        return self.parse_table[self.length-1][0].productions  
                
    #@TODO
    def print_trees(self):
        trees = self.get_trees()
        if not trees:
            print("No parse trees available.")
            return

        print("tree :")
        print("Parse Trees:")
        for i, tree in enumerate(trees, start=1):
            if str(tree.get_type) == 'K':
                print(f"Tree:")
                self._print_tree(tree, indent=2)
                print("\n" + "-" * 40)
            else:
                continue

    def _print_tree(self, node, indent=0):
        if node is not None:
            if isinstance(node, production_rule):
                print(" " * indent + str(node.get_type))
                self._print_tree(node.get_left, indent + 2)
                self._print_tree(node.get_right, indent + 2)
            elif isinstance(node, Cell):
                for production in node.get_rules:
                    print(" " * indent + f"({production.get_type})")
                    self._print_tree(production.get_left, indent + 2)
                    self._print_tree(production.get_right, indent + 2)
                      
    #Print the CYK parse trable for the last sentence that have been parsed.             
    def print_parse_table(self):
        lines = {}
        length = 0
        
        for i, row in enumerate(reversed(self.parse_table)):
            length+=1
            l = []
            for cell in row:
                l.append(cell.get_types)
            lines[i] = l

        for key, arr in lines.items():
            while len(arr) < length:
                lines[key].append([])
        
        lines[length+1] = []
        for s in self.tokens:
            lines[length+1].append([s])

        self.print_table()
        self.print_trees()
        return lines

        
    def print_table(self):
        from tabulate import tabulate
        lines = [] 
        
        for row in reversed(self.parse_table):
            l = []
            for cell in row:
                l.append(cell.get_types)
            lines.append(l)
        
        lines.append(self.tokens)
        print('')
        print(tabulate(lines))

if __name__ == "__main__":
    g = Grammar()
    if g.parse(input("Input sentence: ")):
        print("----------------------------------------")
        print('The sentence IS accepted in the language')
        print("----------------------------------------")
    else:
        print("--------------------------------------------")
        print('The sentence IS NOT accepted in the language')
        print("--------------------------------------------") 
    g.print_table()
    g.print_trees()
