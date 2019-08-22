import nltk

#----------------------------------------------------------------------------------------------------------
# Author: Behnam Khabazan, Samuel Buxton
# Project: Part of Sentence Tagger (Noun Extractor)
# Required Imports and Python Packages: Natural Language Tool Kit 
###########################################################################################################

__names = [] #private list of names of companies
counter = 0  #Global counter to see how many errors, it is not required


# Extracts the company names of business partners
def extractNames():
    global __names
    companyNames = "companies.txt" 
    f = open(companyNames, "r")
    for line in f:
        lines = line.rstrip('\n')
        __names.append(lines.lower())
    __names = sorted(__names)
    return __names

#takes in a sentance and returns back a list of nouns
def extractNouns(input):
    retVal = []
    text = input.split(" ")
    everything = nltk.pos_tag(text)
    for i in range(len(everything)):
        if everything[i][1] == "NNS" or everything[i][1] == "NN" or everything[i][1] == "NNP" or everything[i][1] == "JJ":
            retVal.append(everything[i][0])
    return retVal

#Removes commas within a text
def getRidOfCommas(text):
    return text.split(", ")

#   This is the main method that will be used for the project
def validatenoothercompany(businesspartners, texttovalidate, currentpartner):
    #Run POS tagger on text
    #Check nouns against the list of business partners
    #If match, check if it is current partner
    #If not, print error message
    global counter
    global __names
    __names = [x.lower() for x in businesspartners]
    currentpartner = getRidOfCommas(currentpartner)
    nouns = extractNouns(texttovalidate)
    for noun in nouns:
        if (noun.lower() in businesspartners): #checks to see if a business partner
            if(noun.lower() not in currentpartner): #checks to see if it not is a current partner
                counter += 1
                print(counter, "Error:", noun, "should not be in this text")  

    for word in subDict(businesspartners): #checks if any buniess partners have a space in between
        if word.lower() in texttovalidate.lower(): #checks to see if the partner exist in the sentence
            if word.lower() not in currentpartner: #checks to see if partner is not in the current partners
                counter += 1
                print(counter, "Error:", word, "should not be in this text") 
                
#Checks to see of a word has a space in between it
def subDict(dict):
    newDict = []
    for word in dict:
        if " " in word and word not in newDict:
            newDict.append(word)
    return newDict
       


#main method
if __name__ == "__main__":
    f = open("OrgSent.txt", "r")
    texts = []
    for line in f:
        lines = line.rstrip('\n')
        texts.append(lines)
    
    for text in texts:
        name = extractNames()
        currentpartner = "adobe, west, gates, hawaii, logitech"
        validatenoothercompany(name, text, currentpartner)