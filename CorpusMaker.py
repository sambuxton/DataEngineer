import nltk
import random
import json

# Take random sentences from a company 
from nltk.corpus import wordnet as wn

with open('C:\\Users\\samuel.buxton\\source\\repos\\companyNames.txt', 'r') as f:
    x = f.read().splitlines()




print('this should be the company names')
print(x)



nouns = random.sample(list(wn.all_synsets('n')), 1000)
print('nouns done')
adj = random.sample(list(wn.all_synsets('a')), 1000)
print('adjectives done')
verbs = random.sample(list(wn.all_synsets('v')), 1000)
print('verbs done')
adv = random.sample(list(wn.all_synsets('r')), 1000)
print('adjectives done')

nouns2 = []
for word in nouns:
    nouns2.append(word.name().split('.')[0].replace("_", " "))


adj2 = []
for word in adj:
    adj2.append(word.name().split('.')[0].replace("_", " "))

def conjugate(newWord):
    if newWord[-1] == 'y':
        newWord = newWord[0:len(newWord)-1] + 'ies'
    elif newWord[-1] == 'h' or newWord[-1] == 's' or newWord[-1] == 'x' :
        newWord = newWord[0:len(newWord)] + 'es'
    else:
        newWord = newWord + 's'
    return newWord

verbs2 = []
for word in verbs:
    newWord = word.name().split('.')[0].replace("_", " ")
    finalWord = newWord.split(" ")
    firstWord = conjugate(finalWord[0])

    if len(finalWord) > 1:
        firstWord = firstWord + ' ' + finalWord[1]
    
    verbs2.append(firstWord)
    


adv2 = []
for word in adv:
    adv2.append(word.name().split('.')[0].replace("_", " "))






def jsonFormat(fileName):
    file = open(fileName, 'r')

    documents = {}
    documents["documents"] = []
    charCount = 0
    id = 1

    for line in file:
        documents["documents"].append({
                'id': str(id),
                'language': 'en',
                'text': str(line)
        })
        id += 1

    return documents

def jsonMaker(fileName):
    retVal = jsonFormat(fileName)
    file = open('SampleRequestFinal.json', 'w+')
    file.write(json.dumps(retVal))





#for word in nouns:
#    print(word.next)
#print(nouns[0].name())

# This example uses choice to choose from possible expansions
#from random import choice
# This function is based on _generate_all() in nltk.parse.generate
# It therefore assumes the same import environment otherwise.

file1 = open('notOrgSent.txt','w+')
for i in range(0,20):
    file1.write(nouns2[i] + ' ' + adv2[i] + ' ' + verbs2[i] + ' the ' + adj2[i] + ' ' + nouns2[i+1] + '\n')

file1.close()

companies = x

file2 = open('OrgSent.txt', 'w+')
file3 = open('companies.txt', 'w+')
for i in range(0,20):
    if random.uniform(1, 20) % 2 == 0:
        file2.write(companies[i].capitalize() + ' ' + adv2[i] + ' ' + verbs2[i] + ' the ' + adj2[i] + ' ' + nouns2[i] + '\n')
        file3.write(companies[i].capitalize()  + '\n')
    else:
        file2.write(nouns2[i].capitalize() + ' ' + adv2[i] + ' ' + verbs2[i] + ' the ' + adj2[i] + ' ' + companies[i] + '\n')
        file3.write(companies[i].capitalize()  + '\n')



file3.close()
file2.close()

jsonMaker("orgsent.txt")


# Not string?









