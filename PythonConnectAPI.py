
    
{"documents": [{"id": "1", "language": "en", "text": "Jeff bought three dozen eggs because there was a 50% discount." }, 
               {"id": "2", "language": "en", "text": "The Great Depression began in 1929. By 1933, the GDP in America fell by 25%." } ] 
}

    
import http.client, urllib.request, urllib.parse, urllib.error, base64, urllib.response, json





#with open('SampleRequest.json') as json_file:
#   data = json.load(json_file)


#json_file = open('SampleRequest.josn')



f= open("SampleRequest.json","r")
file = json.load(f)


print(file)



headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '-------',
}


#body = json.dumps()


params = urllib.parse.urlencode({
})


try:
    conn = http.client.HTTPSConnection('westus2.api.cognitive.microsoft.com')
    conn.request("POST", "/text/analytics/v2.1/entities?%s" % params, file, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    #print("[Errno {0}] {1}".format(e.errno, e.strerror))
    print("ohno")










