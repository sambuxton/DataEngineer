import nltk
nltk.download('averaged_perceptron_tagger')

text = ["Ben", "left", "for", "like", "an", "hour", "so", "I", "moved", "to", "the", "other", "table", "sad", "emoji"]

text2 = dictionary = ['Adapt',
'Adobe'
'Alabama',
'Analog' ,
'Apple' ,
'Arkansas',
'Arrow',
'Cisco' ,
'Columbia',
'Cubic',
'Dairy' ,
'Energizer',
'EY',
'Forever 21',
'Fortress' ,
'Gates' ,
'Hawaii' ,
'Houston' ,
'Illinois' ,
'Landmark' ,
'live' ,
'Logitech' ,
'loves' ,
'lower' ,
'Manulife',
'Mastercard',
'Metadata' ,
'Michigan' ,
'Nebraska' ,
'PATH' ,
'Phoenix' ,
'Principal',
'roots' ,
'San Antonio',
'San Jose, CA',
'schools' ,
'Shell' ,
'Standard',
'TEST' ,
'Travel',
'Tropical',
'under armour',
'Valley',
'Waters',
'west',
]
#for sentence in text:
#    sentence = sentence.split()
#    print(sentence)


print(nltk.pos_tag(text2))
test1 = ['I', 'love', 'working', 'for', 'Under Armor']
test2 = ['I', 'love', 'working', 'for', 'under armor']

print(nltk.pos_tag(test1))
print('------------------------------------------------------')
print(nltk.pos_tag(test2))

text3 = 'I love to eat pancakes for breakfast'
text4 = text3.split(" ")


print(text4)
print(nltk.pos_tag(test1)[0][0])





