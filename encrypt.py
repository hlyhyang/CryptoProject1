#!/usr/bin/env python3
#!python3

from random import shuffle


m_file = "message.txt"
k_file = "keys.txt"
c_file = "ciphertext.txt"


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

with open(m_file,'r') as f:
	plaintext = (' '.join(f.readlines())).strip()

# create the keyspace
keyspace = list(range(106))
shuffle(keyspace)

#save the keyspace to file
with open(k_file,'w+') as f:
	f.write(str(keyspace))
print("Saved keyspace to:", k_file)

# create the key matrix
key_matrix = {}
counter = 0
for i,j in freq_matrix.items():
	key_matrix[i] = keyspace[counter:(counter+j)]
	counter += j

# create the ciphertext
crypt = []
for i,j in enumerate(plaintext):
	# mod function
	mod = i % len(key_matrix[j])
	crypt.append(key_matrix[j][mod])

# save the ciphertext to file
with open(c_file,'w+') as f:
	f.write(",".join(list(map(str,crypt))))
print("Ciphertext saved to ciphertext.txt")


