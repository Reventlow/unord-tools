import requests
import json
from decouple import config
from datetime import date, datetime, timedelta

from asset_app.models import Loan_asset, Sms, SmsLog

def createLoanReportPeriode(thisLocation, thisReturnDate, thisTask):
    pass


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
        "receiver": int("45" + str(thisCellphone)),
        "senderName": "U/Nord IT",
        "message": thisMsg,
        "format": "gsm",
        "encoding": "utf8",
      })

    headers = {
     'Authorization': 'Bearer '+ config('SMS_API_KEY'),
     'Content-Type': 'application/json'
     }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def smsAutoLoanAsset():

    message = Sms.objects.filter(description="Udlåns-SMS").last()
    queryset = Loan_asset.objects.filter(loan_date=datetime.today()).exclude(sms_automatic=False).exclude(returned=True)


    sendSmsStatGorm=True
    thisCount = 0
    for obj in queryset:

        thisCount = thisCount + 1
        thisMsg = message.sms_message

        thisId = obj.id
        thisName = obj.loaner_name
        thisAsset = obj.asset.name
        thisLoanDate = obj.loan_date.strftime('%d-%m-%Y')
        thisReturnDate = obj.return_date.strftime('%d-%m-%Y')
        thisMobile = int(obj.loaner_telephone_number)


        thisMsg = thisMsg.replace("#Personens navn#", thisName)
        thisMsg = thisMsg.replace("#Udstyr#", thisAsset)
        thisMsg = thisMsg.replace("#udlåns dato#", thisLoanDate)
        thisMsg = thisMsg.replace("#afleverings dato#", thisReturnDate)

        if(thisMobile < 100000000 and thisMobile > 9999999):
            smsSend(thisMobile, thisMsg)

            new_SmsLog_entry = SmsLog(sms_name=thisName, sms_number=thisMobile, sms_timestamp=datetime.now(), sms_msg_sent=thisMsg, sms_msg_type="Automatisk",  loan_asset_id=thisId)
            new_SmsLog_entry.save()
        else:
            thisCount = thisCount - 1

    if sendSmsStatGorm == True and thisCount > 0 :
        smsSend(91330148, "SMS om ny udlån i dag er sendt til, følgende antal bruger: " + str(thisCount))

def smsAutoReturnReminder():

    message = Sms.objects.filter(description="Påmindelses-SMS").last()

    thisToday = datetime.today()
    thisDaysDif = timedelta(days=3)
    thisReminderDate = thisToday - thisDaysDif
    #print("thisReminderDate"+str(thisReminderDate))

    queryset = Loan_asset.objects.filter(return_date=thisReminderDate).exclude(sms_automatic=False).exclude(returned=True)
    #print(queryset)

    sendSmsStatGorm=True
    thisCount = 0
    for obj in queryset:

        thisCount = thisCount + 1
        thisMsg = message.sms_message

        thisId = obj.id
        thisName = obj.loaner_name
        thisAsset = obj.asset.name
        thisLoanDate = obj.loan_date.strftime('%d-%m-%Y')
        thisReturnDate = obj.return_date.strftime('%d-%m-%Y')
        thisMobile = int(obj.loaner_telephone_number)
        thisLocation = obj.location

        thisMsg = thisMsg.replace("#Personens navn#", thisName)
        thisMsg = thisMsg.replace("#Udstyr#", thisAsset)
        thisMsg = thisMsg.replace("#udlåns dato#", thisLoanDate)
        thisMsg = thisMsg.replace("#afleverings dato#", thisReturnDate)

        if(thisMobile < 100000000 and thisMobile > 9999999):
            smsSend(thisMobile, thisMsg)

            new_SmsLog_entry = SmsLog(sms_name=thisName, sms_number=thisMobile, sms_timestamp=datetime.now(), sms_msg_sent=thisMsg, sms_msg_type="Automatisk",  loan_asset_id=thisId)
            new_SmsLog_entry.save()
        else:
            thisCount = thisCount - 1

    if sendSmsStatGorm == True and thisCount > 0 :
        smsSend(91330148, "SMS om husk at aflever om 3 dage, er sendt til følgende antal bruger: " + str(thisCount))

def smsAutoLateReturn():

    message = Sms.objects.filter(description="Rykker-SMS").last()

    thisToday = datetime.today()
    thisDaysDif = timedelta(days=3)
    thisReminderDate = thisToday + thisDaysDif

    queryset = Loan_asset.objects.filter(return_date=thisReminderDate).exclude(sms_automatic=False).exclude(returned=True)

    sendSmsStatGorm=True
    thisCount = 0
    for obj in queryset:

        thisCount = thisCount + 1
        thisMsg = message.sms_message

        thisId = obj.id
        thisName = obj.loaner_name
        thisAsset = obj.asset.name
        thisLoanDate = obj.loan_date.strftime('%d-%m-%Y')
        thisReturnDate = obj.return_date.strftime('%d-%m-%Y')
        thisMobile = int(obj.loaner_telephone_number)
        thisLocation = obj.location

        thisMsg = thisMsg.replace("#Personens navn#", thisName)
        thisMsg = thisMsg.replace("#Udstyr#", thisAsset)
        thisMsg = thisMsg.replace("#udlåns dato#", thisLoanDate)
        thisMsg = thisMsg.replace("#afleverings dato#", thisReturnDate)

        if(thisMobile < 100000000 and thisMobile > 9999999):
            smsSend(thisMobile, thisMsg)

            new_SmsLog_entry = SmsLog(sms_name=thisName, sms_number=thisMobile, sms_timestamp=datetime.now(), sms_msg_sent=thisMsg, sms_msg_type="Automatisk",  loan_asset_id=thisId)
            new_SmsLog_entry.save()
        else:
            thisCount = thisCount - 1

    if sendSmsStatGorm == True and thisCount > 0 :
        smsSend(91330148, "SMS om at afleve4r for 3 dage siden, er sendt til følgende antal bruger: " + str(thisCount))

def smsButtonLateReturn(thisId):

    message = Sms.objects.filter(description="Rykker-SMS").last()
    obj = Loan_asset.objects.filter(id=thisId).last()
    thisMsg = message.sms_message




    thisName = obj.loaner_name
    thisAsset = obj.asset.model_hardware.asset_type.name + ": " + obj.asset.name
    thisLoanDate = obj.loan_date.strftime('%d-%m-%Y')
    thisReturnDate = obj.return_date.strftime('%d-%m-%Y')
    thisMobile = int(obj.loaner_telephone_number)


    thisMsg = thisMsg.replace("#Personens navn#", thisName)
    thisMsg = thisMsg.replace("#Udstyr#", thisAsset)
    thisMsg = thisMsg.replace("#udlåns dato#", thisLoanDate)
    thisMsg = thisMsg.replace("#afleverings dato#", thisReturnDate)

    if(thisMobile < 100000000 and thisMobile > 9999999):
        smsSend(thisMobile, thisMsg)

        new_SmsLog_entry = SmsLog(sms_name=thisName, sms_number=thisMobile, sms_timestamp=datetime.now(), sms_msg_sent=thisMsg, sms_msg_type="Manuelt", loan_asset_id=thisId)
        new_SmsLog_entry.save()

