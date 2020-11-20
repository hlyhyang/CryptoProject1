#!/usr/bin/env python3
#!python3

from functions import trans


# identify the ciphertext
c_file = input("Please enter ciphertext file name ")
# identify the dictionary
d_file = "dictionary_1.txt"
# output to file
out_file = "test1_output.txt"

# frequencies of each letter
freq = [19,7,1,2,4,10,2,2,5,6,1,1,3,2,6,6,2,1,5,5,7,2,1,2,1,2,1]
# initialize the frequency matrix
freq_matrix = {}

# find the int unicode value of a
ord_init = ord('a')
# create the array of all the letters
letters = [' '] + [chr(i + ord_init) for i in range(26)]
# build the matrix of letters to frequencies
for i in range(len(letters)):
	freq_matrix[letters[i]] = freq[i]

with open(c_file) as f:
	ciphertext = f.readline()
ciphertext = list(map(int,ciphertext.split(",")))

with open(d_file) as f:
	dictionary = list(map(str.strip, f.readlines()))

key_range = 106
results = [0]*(len(dictionary))

gram_score = None


for i in range(len(dictionary)):
	if len(dictionary[i]) < len(ciphertext):
            continue
	d = trans(ciphertext, key_range, dictionary[i], population_size = 20)
	_,fitness,_= d.run(generation_limit = 300, fitness_threshold = float('inf'),crossover_rate = 1, mutation_rate = 1 )
	results[i] = fitness

s = sum(results)

for i,f in enumerate(results):
	print("Dictionary{}\tConfidence:\t{}".format(i,f/s))

output = dictionary[max(enumerate(results),key = lambda x:x[1])[0]]

with open(out_file,'w+') as f:
	f.write(output)

print(output)

