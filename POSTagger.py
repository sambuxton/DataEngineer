import urllib.request
import urllib.response
import sys
import os, glob
import tika
from tika import parser
import http.client, urllib
import json
import re
tika.initVM()


with open('SampleTextJSON.json') as json_file:  
    data = json.load(json_file)


accessKey = '456c8198f5e848c4ade149b774bab71d'
url = 'https://westus2.api.cognitive.microsoft.com'
path = '/text/analytics/v2.1/entities'


def TextAnalytics(documents):
    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = http.client.HTTPSConnection(url)
    body = json.dumps (documents)
    conn.request ("POST", path, body, headers)
    response = conn.getresponse ()
    return response.read ()

dictionary = ['Adapt',
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
'Loves' ,
'Lower' ,
'Manulife',
'Mastercard', 
'Metadata' ,
'Michigan' ,
'Nebraska' ,
'PATH' ,
'Phoenix' ,
'Principal',
'Roots' ,
'San Antonio',
'San Jose, CA',
'Schools' ,
'Shell' ,
'Standard', 
'TEST' ,
'Travel', 
'Tropical',
'Under Armour', 
'Valley',
'Waters',
'West',
]

text

result = TextAnalytics (data)
print (json.dumps(json.loads(result), indent=4))




