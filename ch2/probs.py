import numpy as np
import csv
import itertools
import math

class Probs(object):
    '''
    Represents a probability distribution over n binary variables
    '''

    def __init__(self, n,name=None):
        '''Uniform distribution over n binary variables.'''
        s = [2 for _ in range(n)]
        self.prob_table = np.zeros(tuple(s))
        self.prob_table[:] = 1./np.power(2, n)
        self.name=[]
        nameList=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        if name is not None:
            self.name=name #variables name
        else:
            self.name=nameList[:n]
    
    def read_prob_table_from_csv_file(self, file_name):
        with open(file_name, 'rb') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader) # skip header
            for row in csv_reader:                
                self.prob_table[tuple(row[:-1])] = row[-1]
    
    def marginal(self, variables):
        '''Prob(variables)'''        
        n_old = len(self.prob_table.shape)
        n_new = len(variables)
        combs = itertools.product(range(2), repeat=n_new)

        p_new = Probs(n_new,self.name[variables[0]:(variables[-1]+1)])
        
        for comb in combs:
            index = []
            for i in range(n_old):
                if i in variables:
                    index.append(comb[variables.index(i)])
                else:
                    index.append(slice(None))
            p_new.prob_table[comb] = np.sum(self.prob_table[tuple(index)])
        return p_new
    
    def conditional(self, vars1, vars2):
        '''Prob(vars1|vars2)'''
        if len(vars2)==0:
            return self.marginal(vars1)
        else:
            joint_vars = list(vars1)
            joint_vars.extend(vars2)
            numerator = self.marginal(joint_vars)
            denominator = self.marginal(vars2) # this could be done more efficiently by marginalizing over numerator
            #denominator = numerator.marginal(range(len(joint_vars))[len(vars1):]) # this could be done more efficiently by marginalizing over numerator
            combs = itertools.product(range(2), repeat=len(vars2))
            for comb in combs:
                index = []
                for _ in range(len(vars1)):
                    index.append(slice(None))
                    for c in comb:
                        index.append(c)
                numerator.prob_table[tuple(index)] /= denominator.prob_table[comb]
            return numerator
            

def marginally_independent(jp, var1, var2):
    '''Given a joint distribution jp, test if var1 is marginally independent of var2
       Return True if independent; False otherwise.
    '''
    union_table = jp.marginal((var1+var2)).prob_table
    var1_table = jp.marginal(var1).prob_table
    var2_table = jp.marginal(var2).prob_table
    for i in range(len(var1_table)):
        for j in range(len(var2_table)):
            u=union_table[tuple([i,j])]
            v1= var1_table[i]
            v2= var2_table[j]
            if math.fabs(u-v1*v2)>1e-10:
                return False
    return True

def conditionally_independent(jp, var1, var2, var3):
    '''Given a joint distribution jp, test if var1 is marginally independent of var2 given var3
       Return True if independent; False otherwise.
       P(V1|V2,V3)=P(V1|V3) <-->V1 is independent of V2 given V3
    '''
    assert len(var2)==1
    totLen=len(var1)+len(var2)+len(var3)
    var23=var2+var3
    total_var_table = jp.conditional(var1,var23).prob_table #P(V1|V2,V3)
    var_table=jp.conditional(var1,var3).prob_table #P(V1|V3)
    combs=itertools.product(range(2),repeat=totLen)
    for comb in combs:
        c=list(comb)
        c.pop(1)#var2 is not included; 0000->0?00 0001->0?01; ? could be 0 or 1
        if math.fabs(total_var_table[tuple(comb)]-var_table[tuple(c)])>1e-10:
            return False
    return True

def print_conditionally_independent(jp, var1, var2, var3):
    var3_name=""
    for v in var3:
        var3_name+= str(jp.name[v])
        var3_name+=" "
    if not conditionally_independent(jp,var1,var2,var3):
        print(str(jp.name[var1[0]])+" is not independent with "+ str(jp.name[var2[0]])+" given "+var3_name)
        return False
    print(str(jp.name[var1[0]])+" is independent with "+ str(jp.name[var2[0]])+" given "+var3_name)
    return True


if __name__ == '__main__':
    
    file_name = 'hw1.csv'
    jp = Probs(n=4)
    jp.read_prob_table_from_csv_file(file_name)

    print "MARGINALS\n"

    for i in range(4):
        print "P(%d)\n%s\n" %(i, jp.marginal([i]).prob_table)

    print "\nCONDITIONALS\n"
    for i in range(4):
        for j in range(i+1, 4):
            print "P(%d|%d)\n%s\n" %(i, j, jp.conditional([i], [j]).prob_table)
