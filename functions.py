from random import shuffle
from random import random
from random import sample
from random import randint
from collections import defaultdict
import numpy as np


class perm:
    frequency = {}
    frequency[' '] = 19
    frequency['a'] = 7
    frequency['b'] = 1
    frequency['c'] = 2
    frequency['d'] = 4
    frequency['e'] = 10
    frequency['f'] = 2
    frequency['g'] = 2
    frequency['h'] = 5
    frequency['i'] = 6
    frequency['j'] = 1
    frequency['k'] = 1
    frequency['l'] = 3
    frequency['m'] = 2
    frequency['n'] = 6
    frequency['o'] = 6
    frequency['p'] = 2
    frequency['q'] = 1
    frequency['r'] = 5
    frequency['s'] = 5
    frequency['t'] = 7
    frequency['u'] = 2
    frequency['v'] = 1
    frequency['w'] = 2
    frequency['x'] = 1
    frequency['y'] = 2
    frequency['z'] = 1

    def __init__(self):
        pass

    def encrypt(self, plain, encrypt_table):
        crypt = []
        for i,p in enumerate(plain):
            crypt.append(encrypt_table[p][i % len(encrypt_table[p])])
        return crypt

    def rand_key(self):
        keyspace = list(range(106))
        shuffle(keyspace)
        return keyspace


    def get_decrypt_table(self, key):
        t = []
        i = 0
        for c,f in sorted(self.frequency.items()):
            for _ in range(f):
                t.append(c)
                i += 1
        d = {}
        for i,k in enumerate(key):
            d[k] = t[i]
        return d

    def decrypt(self, crypt, decrypt_table):
        plain = "".join([decrypt_table[c] for c in crypt])
        return plain


class single:

    permutation_cipher = perm()
    def __init__(self, crypt, key_length, key = None, plaintext = None):
        self.fitness = 0
        self.crypt = crypt
        self.key_length = key_length
        if key:
            self.key = key
        else:
            self.key = list(range(self.key_length))
            shuffle(self.key)
        self.plaintext = plaintext                  
        self.getScore()

    def decrypt(self):
        plain = self.permutation_cipher.decrypt(self.crypt,self.permutation_cipher.get_decrypt_table(self.key))
        return plain

    def getScore(self):
        plain = self.decrypt()
        self.fitness = self.fitScore(plain)
        return self.fitness

    
    def fitScore(self, plaintxt):
        score = 0
        for i in range(len(plaintxt)):
            if plaintxt[i] == self.plaintext[i]:
                pf = self.permutation_cipher.frequency[plaintxt[i]]
                if pf  == 1:
                    score += 1500
                elif pf == 2:
                    score += 500
                elif pf == 3:
                    score += 150 
                elif pf == 4:
                    score += 15
                elif pf == 5:
                    score += 7 
                elif pf == 6:
                    score += 2 
                else:
                    score += 1
        return score


class Population:
    
    def __init__(self, size, crypt, key_length, plaintext):
        self.crypt = crypt
        self.key_length = key_length
        self.plaintext = plaintext
        self.pop_size = size
        self.init()

    def init(self):
        self.individuals = np.array([single(self.crypt, self.key_length ,plaintext = self.plaintext) for i in range(self.pop_size)])
        self.individuals_dict = defaultdict(int)
        for individual in self.individuals:
            self.individuals_dict[tuple(individual.key)] += 1
        self.cal_fittest()

    def cal_fittest(self):
        self.fittest = self.individuals[self.get_fittest_index()]
        return self.fittest
    
    def get_fittest_index(self):
        max_index = float('-inf')
        _max = float('-inf')
        for i,idx in enumerate(self.individuals):
            if idx.fitness > _max:
                _max = idx.fitness
                max_index = i
        return max_index
    
    def get_least_fittest_index(self):
        min_index = float('-inf')
        _min = float('inf')
        for i,idx in enumerate(self.individuals):
            if idx.fitness < _min:
                _min = idx.fitness
                min_index = i
        return min_index

    def replace(self, replace_index, replace, revive_threshold):
        rk = tuple(replace.key)
        if rk in self.individuals_dict:
            self.individuals_dict[rk] += 1
            self.revive(rk, revive_threshold)
            return
        del self.individuals_dict[tuple(self.individuals[replace_index].key)]
        self.individuals[replace_index] = replace
        self.individuals_dict[rk] += 1

    def revive(self, key, revive_threshold):
        if self.individuals_dict[key] > revive_threshold and False:
            fprint("revive...")
            self.init()


class trans:
    def __init__(self, crypt, key_length, plaintext, population_size):
        self.crypt = crypt
        self.key_length = key_length
        self.plaintext = plaintext
        self.population_size = population_size
        self.permutation_cipher = perm()
        self.f_table = sorted(self.permutation_cipher.frequency.items())
        self.tmp_table = list(range(len(self.f_table)))
        base = 0
        for i in range(len(self.f_table)):
            self.f_table[i] = (self.f_table[i][0],self.f_table[i][1],base)
            base += self.f_table[i][1]

        self.init()
    
    def init(self):
        self.generationCount = 0
        self.population = Population(self.population_size, self.crypt, self.key_length,self.plaintext)
        self.fittest = self.population.cal_fittest()

    def selection(self):
        p = []
        offset = abs(self.population.individuals[self.population.get_least_fittest_index()].fitness)
        _sum = sum((i.fitness+offset)for i in self.population.individuals)

        for i in self.population.individuals:
            p.append((i.fitness+offset)/_sum)
        return np.random.choice(self.population.individuals,2, p = p,replace=False)

    def crossover(self):
        si1,si2 = self.selection()
        return self.co2(si1,si2)

    # two point crossover
    def co2(self, si1, si2):
        P = 106
        c1 = [0]*P 
        c2 = [0]*P
        p1 = si1.key
        p2 = si2.key
        tmp_set = set()
        L = list(range(P+1))
        s = sample(L,2)
        st,ed = min(s),max(s)

        for i in range(st,ed):
            c1[i] = p1[i]
            tmp_set.add(p1[i])

        j = 0
        k = 0
        while j < st and k < P:
            if p2[k] in tmp_set:
                k += 1
            else:
                c1[j] = p2[k]
                tmp_set.add(p2[k])
                j += 1

        j = ed
        while j < P and k < P:
            if p2[k] in tmp_set:
                k += 1
            else:
                c1[j] = p2[k]
                tmp_set.add(p2[k])
                j += 1

        tmp_set.clear()

        for i in range(st,ed):
            c2[i] = p2[i]
            tmp_set.add(p2[i])

        j = 0
        k = 0
        while j < st and k < P:
            if p1[k] in tmp_set:
                k += 1
            else:
                c2[j] = p1[k]
                tmp_set.add(p1[k])
                j += 1

        j = ed
        while j < P and k < P:
            if p1[k] in tmp_set:
                k += 1
            else:
                c2[j] = p1[k]
                tmp_set.add(p1[k])
                j += 1
        
        c_i1 = single(self.crypt, self.key_length , key = c1, plaintext = self.plaintext)
        c_i2 = single(self.crypt, self.key_length , key = c2, plaintext = self.plaintext)
        c_i1.getScore()
        c_i2.getScore()

        c_i_max= max(c_i1, c_i2, key=(lambda x:x.fitness))

        self.population.replace(self.population.get_least_fittest_index(), c_i_max, self.revive_threshold)
    

    # randomly chosse two positions and swap : choose principal: first randomly choose from 1~27, then randomly choose the offset 
    def mutation(self):

        c1,c2 = self.selection()
        cc1 = list(c1.key)
        cc2 = list(c2.key)
        
        if self.fittest.fitness < 0:
            si1 = 0
            si2 = randint(1,len(self.f_table)-1)
        else:
            si1,si2 = sample(self.tmp_table,2)
        s1 = self.f_table[si1]
        s2 = self.f_table[si2]
        ss1 = s1[2] + randint(0,s1[1]-1)
        ss2 = s2[2] + randint(0,s2[1]-1)

        cc1[ss1], cc1[ss2] = cc1[ss2], cc1[ss1]

        if self.fittest.fitness < 0:
            si1 = 0
            si2 = randint(1,len(self.f_table)-1)
        else:
            si1,si2 = sample(self.tmp_table,2)
        s1 = self.f_table[si1]
        s2 = self.f_table[si2]
        ss1 = s1[2] + randint(0,s1[1]-1)
        ss2 = s2[2] + randint(0,s2[1]-1)
        cc2[ss1], cc2[ss2] = cc2[ss2], cc2[ss1]

        cc_i1 = single(self.crypt, self.key_length , key = cc1, plaintext = self.plaintext)
        cc_i2 = single(self.crypt, self.key_length , key = cc2, plaintext = self.plaintext)
        cc_i1.getScore()
        cc_i2.getScore()

        # if cc_i1.fitness > c_i_max.fitness or cc_i2.fitness > c_i_max.fitness:
        c_i_max= max(cc_i1, cc_i2, key=(lambda x:x.fitness))
        self.population.replace(self.population.get_least_fittest_index(), c_i_max, self.revive_threshold)

    def run(self, fitness_threshold, generation_limit, crossover_rate, mutation_rate):
        results = []
        self.revive_threshold = generation_limit//500
        while self.generationCount < generation_limit :        
            self.generationCount += 1
            for _ in range(3):
                if random() < crossover_rate:
                    self.crossover()
                    if random() < mutation_rate:
                        self.mutation()
            
            self.fittest = self.population.cal_fittest()


            if self.fittest.fitness >= fitness_threshold:
                if results and tuple(self.fittest.key) == tuple(results[-1][2]):
                    continue
                r = (self.fittest.decrypt(),self.fittest.fitness,self.fittest.key)
                results.append(r)
                print("Found:\n{}\nScore:{} Key:{}".format(r[0],r[1],r[2]))
                switch = input("\nif not right enter n to keep working")
                if switch == 'n':
                    break
                elif switch == 're': # restart
                    results.clear()
                    self.init()

        best_guess = self.fittest.decrypt()
        return best_guess, self.fittest.fitness, results
