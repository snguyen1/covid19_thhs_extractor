import requests
from bs4 import BeautifulSoup
import csv
import datetime
from datetime import date
from datetime import timedelta
import os
import urllib3
import json
urllib3.disable_warnings()


def getContent(url):
    appendLog()
    response = requests.get(url, verify=False)
    return json.loads(response.content)['features']


def saveRawData(data):
    with open("./raw/" + getTodayDate() + ".json", "w") as write_file:
        json.dump(data, write_file)
    return


def loadTodayData():
    with open("./raw/" + getTodayDate() + ".json") as out:
        return json.load(out)


def extractStateWideData(data):
    result = []
    return result


def extractCountiesData(data):
    result = []
    for row in data:
        result.append((row['attributes']['County'],
                       row['attributes']['Count_']))
    return result


def countiesDataToCsv(data):
    today = date.today()
    fileNameWithPath = './csv/' + today.strftime("%B%d") + '.csv'
    if os.path.exists(fileNameWithPath):
        os.remove(fileNameWithPath)
    with open(fileNameWithPath, 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['County', today.strftime("%B%d")])
        for row in data:
            csv_out.writerow(row)
    out.close()


def getTodayDate():
    today = date.today()
    return today.strftime("%B%d")


def getYesterdayDate():
    yesterday = date.today() - timedelta(days=1)
    return yesterday.strftime("%B%d")


def appendLog():
    currentDateTime = datetime.datetime.now()
    out = open('log.txt', 'a')
    out.write("Run at " + str(currentDateTime) + "\n")
    out.close()


def processData(sourceData, countyData):
    # Reset attributes before new calculation
    sourceData[getTodayDate()] = 0
    sourceData['NewCases'] = 0

    # Append new column and calculate new cases
    for i, cnt_row in countyData.iterrows():
        for j, row in sourceData.iterrows():
            if row['County'] == cnt_row['County']:
                sourceData.at[j, getTodayDate()] = cnt_row[getTodayDate()]
                if getYesterdayDate() in sourceData:
                    sourceData.at[j, 'NewCases'] = (
                        cnt_row[getTodayDate()] - row[getYesterdayDate()])
    return sourceData


def writeResult(data):
    fileNameWithPath = './Texas_COVID.csv'
    data.to_csv(fileNameWithPath, index=False, header=True)
