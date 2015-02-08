import numpy as np
import csv
import itertools

class Probs(object):
    '''
    Represents a probability distribution over n binary variables
    '''

    def __init__(self, n):
        '''Uniform distribution over n binary variables.'''
        s = [2 for _ in range(n)]
        self.prob_table = np.zeros(tuple(s))
        self.prob_table[:] = 1./np.power(2, n)
    
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
                
        p_new = Probs(n_new)
        
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
    raise NotImplementedError('Not implemented yet.')

def conditionally_independent(jp, var1, var2, var3):
    '''Given a joint distribution jp, test if var1 is marginally independent of var2 given var3
       Return True if independent; False otherwise.
    '''
    raise NotImplementedError('Not implemented yet.')


        
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