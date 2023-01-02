from datetime import date, datetime

def addCookieFromFile(driver):
    stream = open('cookie.txt', 'r')
    data = stream.read()
    items = data.split(';')
    for item in items:
        name = item.split('=')[0]
        value = item.split('=')[1]
        print(name, value)
        driver.add_cookie({   
            "name": name, 
            "value": value,
            "domain": ".bilibili.com",
            "path": "./"
        })


def getUpListFromFile():
    stream = open('ups_dust.txt', 'r')
    data = stream.readlines()
    return data


def checkDateDelta(dateString):
    if "投稿" in dateString:
        return False
    elif "前" in dateString:
        return True
    elif len(dateString) == 5:
        today = date.today()
        year = str(today.year)
        statusDateString = year + '-' + dateString
        statusDate = datetime.strptime(statusDateString, '%Y-%m-%d').date()
        days_delta = today - statusDate
        if days_delta.days < 21:
            return True
        return False
    elif len(dateString) > 5:
        today = date.today()
        year = str(today.year)
        statusDate = datetime.strptime(dateString, '%Y-%m-%d %H:%M').date()
        days_delta = today - statusDate
        if days_delta.days < 21:
            return True
        return False
    return False


def storeFwdedStatus(status_id):
    stream = open('fwded.txt', 'a')
    stream.write(status_id)
    stream.write('\n')
    stream.close()


def getFwdedStatus():
    stream = open('fwded.txt', 'r')
    ids = stream.readlines()
    ids = [id.strip('\n') for id in ids]
    stream.close()
    return ids


def checkIfFwded(id):
    fwdws_ids = getFwdedStatus()
    return id not in fwdws_ids