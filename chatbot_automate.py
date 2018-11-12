#!/usr/local/bin/python3.5
import csv
import http.client
import requests
import json
conn = http.client.HTTPSConnection("api.dialogflow.com")
headers = {
    'authorization': "Bearer deca6715957e4d969f98d033cf844505",
    'content-type': "application/json"
}
Entities_record = []
Intent_record = []
Records = []
count = 0
with open('BOTO.csv', encoding = "ISO-8859-1") as file:
    reader = csv.reader(file)
    for column in reader:
        count = count + 1
        if count == 1:
            continue
        if column[0] == '':
            continue
        syns=[]
        for syn in column[2].split(','):
            syns.append(syn.strip())
            Entities_record.append({
                "entries": [
                {
                    "synonyms": syns,
                    "value": column[1].strip()
                }
                ],
                "name": column[0].strip()
            })
        usersays = []
        userans =  column[4].split('\n')
        for userans in userans:
            usersays.append({
                "count": 0,
                "data": [
                    {
                        "alias": column[1].strip(),
                        "meta": "@" + column[1].strip(),
                        "text": userans.strip(),
                        "userDefined": True
                    }
                ]
            })
        data = {
            "contexts": [],
            "events": [],
            "fallbackIntent": False,
            "name": column[3].strip(),
            "priority": 500000,
            "responses": [
                {    "defaultResponsePlatforms": {
                        "google": True
                    },
                    "messages": [
                        {
                            "speech": column[7].strip() ,
                            "type": 0
                        }
                    ],
                    "parameters": [],
                    "resetContexts": False
                }
            ],
            "userSays": usersays,
            "webhookForSlotFilling": False,
            "webhookUsed": False
        }
        json_foo = json.dumps(data)
        url = "https://api.dialogflow.com/v1/intents?v=20150910"
        response = requests.request("POST", url, data=json_foo, headers=headers)
        print(response.text)

json_foo = json.dumps(Entities_record)
url = "https://api.dialogflow.com/v1/entities?v=20150910"
response = requests.request("PUT", url, data=json_foo, headers=headers)
print(response.text)
