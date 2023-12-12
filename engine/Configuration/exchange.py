import json
import sys
import datetime
import urllib.request

# File with exchange rates (WINDOWS PATH)
path = ".\\Configuration\\results.json"


# Get rates from API (relative to EUR)
def getRatesFromAPI():
    url = 'http://api.exchangeratesapi.io/v1/latest?access_key=57d102e76d357aaaab5dba8955ffa5a8'
    data = urllib.request.urlopen(url).read()
    return json.loads(data)["rates"]


def getDataToSave():
    with open(path, "w+") as file:
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        rates = getRatesFromAPI()
        file.write(json.dumps({"date": date, "rates": rates}))
    return rates


def getRates():
    text = ""
    with open(path, "w+") as file:
        text = file.read()

    try:
        if (text == ""):
            return getDataToSave()

        data = json.loads(text)
        if (["date", "rates"] not in data.keys()):
            return getDataToSave()

        if (data["date"] != datetime.datetime.now().strftime("%d/%m/%Y")):
            return getDataToSave()

        return data["rates"]
    except Exception as e:
        print(str(e), sys.stderr)
        return getDataToSave()


def exchangeMoney(value, currency1, currency2):
    rates = getRates()
    if (currency1 not in rates.keys()):
        raise Exception(currency1 + " doesn't exist in our system.")

    if (currency2 not in rates.keys()):
        raise Exception(currency2 + " doesn't exist in our system.")

    if (currency1 == "EUR"):
        return value * float(rates[currency2])

    if (currency2 == "EUR"):
        return value / float(rates[currency1])

    return value / float(rates[currency1]) * float(rates[currency2])
