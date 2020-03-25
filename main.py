import os
import ssl
import json
from data import getContent, extractCountiesData, extractStateWideData, countiesDataToCsv, getTodayDate, getYesterdayDate, saveRawData, loadTodayData, processData, writeResult
import pandas as pd
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/COVID19County_ViewLayer/FeatureServer/0/query?f=json&where=Count_%3C%3E0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Count_%20desc&outSR=102100&resultOffset=0&resultRecordCount=254&cacheHint=true"


# # Main code starts here

# create dirs to store raw files
if not os.path.exists('raw'):
    os.makedirs('raw')
if not os.path.exists('csv'):
    os.makedirs('csv')


# Get data from URL
data = getContent(url)

# Only use this for testing or when today's data is already in the raw file
# data = loadTodayData()

# Save raw data to raw directory
saveRawData(data)

# extract and save today county data to csv directory
counties = extractCountiesData(data)
countiesDataToCsv(counties)

# read and convert counties to dataframe
counties = pd.read_csv('./csv/' + getTodayDate() + '.csv', delimiter=',')

# Texas_COVID.csv is the file with same schema as local arcMap database
# Load this to dataframe
df = pd.read_csv('Texas_COVID.csv', delimiter=',')

# process Data
final = processData(df, counties)

# Write to Texas_Covid.csv
writeResult(final)
# print(final)
