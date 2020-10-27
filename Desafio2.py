import json
import pandas as pd
import pathlib
from datetime import datetime
currentPath = str(pathlib.Path().absolute())
file_path =currentPath+'/data.json'
data = [json.loads(line) for line in open(file_path, 'r', encoding='utf-8-sig')]

def getIntValue(dict, key):
    if key in dict:
        return int(dict[key])
    else:
        return 0 

def getStringValue(dict, key):
    if key in dict:
        return dict[key]
    else:
        return ''
    
def newDict(dataDict):
    idVisit = dataDict['fullVisitorId']+"."+dataDict['visitId']       
    newDict={'id':idVisit, 
             'pageViews':getIntValue(dataDict['totals'],'pageviews'), 
             'timeOnSite':getIntValue(dataDict['totals'],'timeOnSite'), 
             'browser':getStringValue(dataDict['device'],'browser'),
             'date':datetime.strptime(dataDict['date'], '%Y%m%d'),
             'visitNumber':dataDict['visitNumber'],
             'fullVisitorID':dataDict['fullVisitorId'],
             'visitId':dataDict['visitId']
            }
    return newDict

newData=list(map(lambda x: newDict(x), data))

df = pd.DataFrame(newData)
pd.DataFrame.from_dict(newData)

#Number of sessions by user
su=df.groupby("fullVisitorID")["visitId"].count()

su.to_csv(currentPath+'/SessoesPorUsuario.csv', index_label=["Ususario","NumeroDeSessoes"])

#Count de pageViews
print("Total de pageViews")
print (df['pageViews'].sum())

#Sessions by date
sd=df.groupby("date")["id"].count()
sd.to_csv(currentPath+'/SessoesPorData.csv', index_label=["Data","NumeroDeSessoes"])

#Average session duration by date 
dt=df.groupby("date")["timeOnSite"].mean()
dt.to_csv(currentPath+'/DuracaoMediaSessoesPorData.csv', index_label=["Data","MediaTempoDasSessoes(s)"])

#Diare session by the type of browsers
sb=df.groupby(["date","browser"])["id"].count()
sb.to_csv(currentPath+'/SessoesDiariasPorBrowser.csv', index_label=["data","Tipo de Browsers","SomaSessoesDiarias"])
