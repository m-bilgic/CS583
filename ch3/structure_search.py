from ch2.probs import Probs, marginally_independent, conditionally_independent
import itertools

def print_conditionally_independent_multi_vars(jp,var1,var2,var3):
    var2_name=""
    for v in var2:
        var2_name+= str(jp.name[v])
        var2_name+=" "
    var3_name=""
    for v in var3:
        var3_name+= str(jp.name[v])
        var3_name+=" "
    if not conditionally_independent_multi_vars(jp,var1,var2,var3):
        print(str(jp.name[var1[0]])+" is not independent with "+ var2_name+"given "+var3_name)
        return False
    print(str(jp.name[var1[0]])+" is independent with "+ var2_name+"given "+var3_name)
    return True

def conditionally_independent_multi_vars(jp,var1,var2,var3):
    for v2 in var2:
        if not conditionally_independent(jp,var1,[v2],var3):
            return False
    return True

def marginally_independent_multi_vars(jp,var1,var2):
    for v2 in var2:
        if not marginally_independent(jp,var1,[v2]):
            return False
    return True

def get_subset(given_Set):
    all_subset=[]
    for i in range(len(given_Set)+1):
        combs=itertools.combinations(given_Set,i)
        for c in combs:
            all_subset.append(list(c))
    return all_subset

def subtract_set(full_set,sub_set):
    assert len(full_set)>=len(sub_set)
    for v in sub_set:
        full_set.remove(v)
    return full_set

def minimal_imap(jp, variable_order):
    '''Given a joint distribution and a variable order,
       construct a minimal imap.
       Algorithm 3.2 in the PGM book.
       http://pgm.stanford.edu/Algs/page-79.pdf
    '''
    post_set=[]
    for var_order in variable_order:
        if len(post_set)==0:
            post_set.append(var_order)
        else:
            u_set=get_subset(post_set)

            for u in u_set:
                # var2=[]
                copy_set=list(post_set)
                var2=subtract_set(copy_set,u)
                if conditionally_independent_multi_vars(jp,[var_order],var2,u):
                    for v in u:
                        print str(jp.name[v])+"->"+str(jp.name[var_order])
                    break
            post_set.append(var_order)


def iequivalent_structures(jp):
    '''Given a joint distribution find all i-equilavent structures that
       are a p-map.
       Algorithms 3.3, 3.4, and 3.5 in the PGM book.
       http://pgm.stanford.edu/Algs/page-85.pdf
       http://pgm.stanford.edu/Algs/page-86.pdf
       http://pgm.stanford.edu/Algs/page-89.pdf
    '''
    raise NotImplementedError('Not implemented yet.')

if __name__ == '__main__':
    file_name = 'hw1.csv'
    jp = Probs(n=4)
    jp.read_prob_table_from_csv_file(file_name)
    minimal_imap(jp, [3,2,1,0])