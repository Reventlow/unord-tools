import requests
import json
from decouple import config
from datetime import date, datetime


def dateWeekday(thisDate):
    if thisDate.weekday() == 0:
        thisDate = thisDate.strftime('%d/%m/%Y') + " Mandag"
        return thisDate
    elif thisDate.weekday() == 1:
        thisDate = thisDate.strftime('%d/%m/%Y') + " Tirsdag"
        return thisDate
    elif thisDate.weekday() == 2:
        thisDate = thisDate.strftime('%d/%m/%Y') + " Onsdag"
        return thisDate
    elif thisDate.weekday() == 3:
        thisDate = thisDate.strftime('%d/%m/%Y') + " Torsdag"
        return thisDate
    elif thisDate.weekday() == 4:
        thisDate = thisDate.strftime('%d/%m/%Y') + " Fredag"
        return thisDate
    elif thisDate.weekday() == 5:
        thisDate = thisDate.strftime('%d/%m/%Y') + " Lørdag"
        return thisDate
    elif thisDate.weekday() == 6:
        thisDate = thisDate.strftime('%d/%m/%Y') + " Søndag"
        return thisDate

def smsSend(thisCellphone, thisMsg):
    url = "https://api.sms.dk/v1/sms/send"
    payload = json.dumps({
        "receiver": thisCellphone,
        "senderName": "U/Nord IT",
        "message": thisMsg ,
        "format": "gsm",
        "encoding": "utf8",
      })

    headers = {
     'Authorization': 'Bearer '+ config('SMS_API_KEY'),
     'Content-Type': 'application/json'
     }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)