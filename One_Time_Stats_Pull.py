# -*- coding: utf-8 -*-
"""
Connor Buchanan
version 1.0 - 1/1/2021

Interacts with Understat to pull script response of all EPL games. 
One time script to populate database with historical information
"""


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3

#get list of existing URL IDs
conn = sqlite3.connect('C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()

urlList = c.execute("SELECT DISTINCT URL_ID FROM MATCH").fetchall()
conn.close()

#start at first game available on understat (2017-2018 season)
#change back before running full
urlNum = 15860
#14149
#15860 

#loop until most recent EPL game is captured
while urlNum < 15862:
    url = 'https://understat.com/match/' + str(urlNum)
    page = requests.get(url)
    
    #if value already exists in database
    if urlNum in urlList:
        #assign arbitrary value to skip if block
        childList = ['X','X','X','X','X']
        
    #ensure page is found
    elif str(page) != '<Response [404]>':
        
        #return all html code within the given url
        soup = BeautifulSoup(page.content, 'html.parser')

        #determine if game is EPL
        result = soup.find('div',{'class': 'page-wrapper'}).find('ul')
        children = result.findChildren()
        childList = []
        for child in children:
            x = child.get_text()
            childList.append(x)
    else:
        #assign arbitrary value to skip if block
        childList = ['X','X','X','X','X']
        
    #only continue if league is EPL, else loop
    #insert statement to SQL will use variable names with i at the beginning
    #each game will result in two rows being added to STAT_ARCHIVE
    league = childList[3]
    if league != 'EPL' and league != 'X':
        iURL_ID = urlNum
        childDate = childList[4]
        unformDate = datetime.strptime(childDate, '%b %d %Y')
        iEVENT_DATE = unformDate.strftime('%Y-%m-%d') 
        
        #scrape html for home and away stats
        
        #this code returns the tags for each stat
        statList = [s  for div in soup.select('.progress-bar .progress-title') for s in div.stripped_strings]

        #find the progress draw element for chances
        progressDraw = [s  for div in soup.select('.progress-bar .progress-draw .progress-value') for s in div.stripped_strings]
        if progressDraw != []:
            progDraw = int(progressDraw[0])
        else:
            progDraw = 0

        #this returns the raw values, but some elements will need to be deleted or concatonated
        rawAwayStats = [s  for div in soup.select('.progress-bar .progress-away .progress-value') for s in div.stripped_strings]
        rawHomeStats = [s  for div in soup.select('.progress-bar .progress-home .progress-value') for s in div.stripped_strings]

        #put stats in order within new list
        #account for scenario where chance % is too small to be listed
        awayStats = []
        if rawAwayStats[2] == '%':
            awayStats.append(rawAwayStats[0])
            awayStats.append(int(rawAwayStats[1]))
            awayStats.append(int(rawAwayStats[3]))
            awayStats.append(float(str(rawAwayStats[4])+str(rawAwayStats[5])))
            awayStats.append(int(rawAwayStats[6]))
            awayStats.append(int(rawAwayStats[7]))
            awayStats.append(int(rawAwayStats[8]))
            awayStats.append(float(str(rawAwayStats[9])+str(rawAwayStats[10])))
            awayStats.append(float(str(rawAwayStats[11])+str(rawAwayStats[12])))
        else:
            awayStats.append(rawAwayStats[0])
            awayStats.append(100 - int(int(rawHomeStats[1])+progDraw))
            awayStats.append(int(rawAwayStats[1]))
            awayStats.append(float(str(rawAwayStats[2])+str(rawAwayStats[3])))
            awayStats.append(int(rawAwayStats[4]))
            awayStats.append(int(rawAwayStats[5]))
            awayStats.append(int(rawAwayStats[6]))
            awayStats.append(float(str(rawAwayStats[7])+str(rawAwayStats[8])))
            awayStats.append(float(str(rawAwayStats[9])+str(rawAwayStats[10])))
        #print(awayStats)

        #same process for home stats
        homeStats = []
        if rawHomeStats[2] == '%':
            homeStats.append(rawHomeStats[0])
            homeStats.append(int(rawHomeStats[1]))
            homeStats.append(int(rawHomeStats[3]))
            homeStats.append(float(str(rawHomeStats[4])+str(rawHomeStats[5])))
            homeStats.append(int(rawHomeStats[6]))
            homeStats.append(int(rawHomeStats[7]))
            homeStats.append(int(rawHomeStats[8]))
            homeStats.append(float(str(rawHomeStats[9])+str(rawHomeStats[10])))
            homeStats.append(float(str(rawHomeStats[11])+str(rawHomeStats[12])))
        else:
            homeStats.append(rawHomeStats[0])
            homeStats.append(100 - int(int(rawAwayStats[1])+progDraw))
            homeStats.append(int(rawHomeStats[1]))
            homeStats.append(float(str(rawHomeStats[2])+str(rawHomeStats[3])))
            homeStats.append(int(rawHomeStats[4]))
            homeStats.append(int(rawHomeStats[5]))
            homeStats.append(int(rawHomeStats[6]))
            homeStats.append(float(str(rawHomeStats[7])+str(rawHomeStats[8])))
            homeStats.append(float(str(rawHomeStats[9])+str(rawHomeStats[10])))
        #print(homeStats)
        
        #assign variables for two inserts to database
        #URL_ID and EVENT_DATE are same for both entries
        #All others will have 1 or 2 after variable name
        
        #away values first
        iTEAM1 = awayStats[0]
        iOPPONENT1 = homeStats[0]
        iHOME_AWAY1 = 'AWAY'
        if awayStats[2] > homeStats[2]:
            iRESULT1 = 'W'
            iPOINTS1 = 3
        elif awayStats[2] < homeStats[2]:
            iRESULT1 = 'L'
            iPOINTS1 = 0
        else:
            iRESULT1 = 'D'
            iPOINTS1 = 1
        iCHANCES1 = awayStats[1]
        iGOALS1 = awayStats[2]
        iXG1 = awayStats[3]
        iSHOTS1 = awayStats[4]
        iSHOTS_TARGET1 = awayStats[5]
        iDEEP1 = awayStats[6]
        iPPDA1 = awayStats[7]
        iXPTS1 = awayStats[8]
        
        
        #home values second
        iTEAM2 = homeStats[0]
        iOPPONENT2 = awayStats[0]
        iHOME_AWAY2 = 'HOME'
        if homeStats[2] > awayStats[2]:
            iRESULT2 = 'W'
            iPOINTS2 = 3
        elif homeStats[2] < awayStats[2]:
            iRESULT2 = 'L'
            iPOINTS2 = 0
        else:
            iRESULT2 = 'D'
            iPOINTS2 = 1
        iCHANCES2 = homeStats[1]
        iGOALS2 = homeStats[2]
        iXG2 = homeStats[3]
        iSHOTS2 = homeStats[4]
        iSHOTS_TARGET2 = homeStats[5]
        iDEEP2 = homeStats[6]
        iPPDA2 = homeStats[7]
        iXPTS2 = homeStats[8]
        
        #create insert statements
        insert1 = "INSERT INTO STAT_ARCHIVE VALUES ("+str(iURL_ID)+",'"+str(iEVENT_DATE)+"','"+str(iTEAM1)+"','"+str(iOPPONENT1)+"','" \
                    +str(iHOME_AWAY1)+"','"+str(iRESULT1)+"',"+str(iPOINTS1)+","+str(iCHANCES1)+","+str(iGOALS1)+","+str(iXG1)+"," \
                    +str(iSHOTS1)+","+str(iSHOTS_TARGET1)+","+str(iDEEP1)+","+str(iPPDA1)+","+str(iXPTS1)+"," \
                    +str(iCHANCES2)+","+str(iGOALS2)+","+str(iXG2)+","+str(iSHOTS2)+","+str(iSHOTS_TARGET2)+"," \
                    +str(iDEEP2)+","+str(iPPDA2)+","+str(iXPTS2)+",'"+str(league)+"')"
        insert2 = "INSERT INTO STAT_ARCHIVE VALUES ("+str(iURL_ID)+",'"+str(iEVENT_DATE)+"','"+str(iTEAM2)+"','"+str(iOPPONENT2)+"','" \
                    +str(iHOME_AWAY2)+"','"+str(iRESULT2)+"',"+str(iPOINTS2)+","+str(iCHANCES2)+","+str(iGOALS2)+","+str(iXG2)+"," \
                    +str(iSHOTS2)+","+str(iSHOTS_TARGET2)+","+str(iDEEP2)+","+str(iPPDA2)+","+str(iXPTS2)+"," \
                    +str(iCHANCES1)+","+str(iGOALS1)+","+str(iXG1)+","+str(iSHOTS1)+","+str(iSHOTS_TARGET1)+"," \
                    +str(iDEEP1)+","+str(iPPDA1)+","+str(iXPTS1)+",'"+str(league)+"')"
        
        #connect and make insertations to database
        conn = sqlite3.connect('C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
        c = conn.cursor()
        c.execute(insert1)
        c.execute(insert2)
        
        #commit changes and close connection
        conn.commit() 
        conn.close()
        
        print('Inserted ' +str(iTEAM2)+' v ' +str(iTEAM1) + ' from ' + str(iEVENT_DATE) + ' ('+str(urlNum)+')')    
    else:
        print('URL '+str(urlNum)+ ' is EPL or does not exist')
    #iterate through urlNum in loop    
    urlNum += 1

