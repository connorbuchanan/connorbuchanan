# -*- coding: utf-8 -*-


#Connor Buchanan

#version 4.0 - 2/23/2021

#Combination of all scripts needed for complete process


#Changes to version 3.0
#    -Streamlined scraping from Understat, now seperated by league
#    -Change to Global_LDA_v1 model
    
#Changes to version 4.0
#    -Compatability changes for python 3.8
#       -added r to connection strings
#           -conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
#       -removed block comments




#global list variables for league
leagueList = ['EPL','La liga','Serie A','Bundesliga','Ligue 1']

"""
Connor Buchanan
Stats_Pull.py

Interacts with Understat to pull script response of all recently completed EPL games. 
Should only populate with games that aren't already in the database. Base on URL_ID.
"""


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3

#query to find url values that exist in database
conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()
urlList = c.execute("SELECT DISTINCT URL_ID FROM MATCH").fetchall()
conn.close() 

for l in leagueList:
#query to find maximum url value that exists in database
    conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
    c = conn.cursor()
    maxURL = c.execute("SELECT MAX(URL_ID) FROM STAT_ARCHIVE WHERE LEAGUE = '"+str(l)+"'").fetchall()
    
    games = c.execute("SELECT COUNT(*) FROM MATCH WHERE RESULT IS NULL AND EVENT_DATE < CURRENT_DATE AND LEAGUE = '"+str(l)+"'").fetchall()
    updates = int(games[0][0])
    
    conn.close() 
    
    #determine start and end number for loop
    urlNum = int(maxURL[0][0])-100
    #maxNum = urlNum + 250
    
    #urlNum = 15654
    
    #count the number of inserts made
    inserts = 0
    
    #for ad-hoc\
    #urlNum = 14637
    #maxNum = urlNum + 40
    
    #loop until all null match results are entered
    #while urlNum < maxNum:
    while inserts < updates:
        url = 'https://understat.com/match/' + str(urlNum)
        page = requests.get(url)
        
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
        if league == l:
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
                matchRes = 'AWAY'
            elif awayStats[2] < homeStats[2]:
                iRESULT1 = 'L'
                iPOINTS1 = 0
                matchRes = 'HOME'
            else:
                iRESULT1 = 'D'
                iPOINTS1 = 1
                matchRes = 'DRAW'
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
            
            HOME_TEAM = iTEAM2
            AWAY_TEAM = iTEAM1
            
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
            
            
            #connect to database
            conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
            c = conn.cursor()
            
            """Derive previously assigned variable"""
            urlQuery = c.execute("SELECT URL_ID FROM MATCH WHERE HOME_TEAM = '"+str(HOME_TEAM)+"' AND AWAY_TEAM = '"+str(AWAY_TEAM) \
                                 +"' AND RESULT IS NULL").fetchall()
            replaceURL = int(urlQuery[0][0])
            
            #update URL_ID in prediction tables
            c.execute("UPDATE MATCH SET URL_ID = "+str(iURL_ID)+" WHERE URL_ID = "+str(replaceURL))
            c.execute("UPDATE CHANCES SET URL_ID = "+str(iURL_ID)+" WHERE URL_ID = "+str(replaceURL))
            c.execute("UPDATE GOALS SET URL_ID = "+str(iURL_ID)+" WHERE URL_ID = "+str(replaceURL))
            c.execute("UPDATE OPP_GOALS SET URL_ID = "+str(iURL_ID)+" WHERE URL_ID = "+str(replaceURL))
            c.execute("UPDATE OPP_SHOTS SET URL_ID = "+str(iURL_ID)+" WHERE URL_ID = "+str(replaceURL))
            c.execute("UPDATE OTHER_STATS SET URL_ID = "+str(iURL_ID)+" WHERE URL_ID = "+str(replaceURL))
            c.execute("UPDATE POINTS SET URL_ID = "+str(iURL_ID)+" WHERE URL_ID = "+str(replaceURL))
            c.execute("UPDATE SHOTS SET URL_ID = "+str(iURL_ID)+" WHERE URL_ID = "+str(replaceURL))
            
            #insert result to match table
            matchInsert = "UPDATE MATCH SET RESULT = '"+str(matchRes)+"' WHERE URL_ID = "+str(iURL_ID)
            
            conn.commit()
            
            """Make inserts"""
            #connect and make insertations to database
            conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
            c = conn.cursor()
            c.execute(insert1)
            c.execute(insert2)
            c.execute(matchInsert)
            
            #commit changes and close connection
            conn.commit() 
            conn.close()
            
            
            
            
            """Make inserts to prediction table"""
            
            
            conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
            c = conn.cursor()
            
            #derive fanduel names for query
            FANDUEL_HOME = c.execute("SELECT FANDUEL FROM TEAMS WHERE UNDERSTAT = '"+str(HOME_TEAM)+"'").fetchall()
            FANDUEL_AWAY = c.execute("SELECT FANDUEL FROM TEAMS WHERE UNDERSTAT = '"+str(AWAY_TEAM)+"'").fetchall()
            
            HOME_TEAM = FANDUEL_HOME[0][0]
            AWAY_TEAM = FANDUEL_AWAY[0][0]
            
            #find id to use for update statements
            idQuery = c.execute("SELECT ID FROM PREDICTIONS WHERE HOME_TEAM = '"+str(HOME_TEAM)+"' AND AWAY_TEAM ='" \
                                +str(AWAY_TEAM)+"' AND EVENT_DATE = '"+str(iEVENT_DATE)+"'").fetchall()
            predID = int(idQuery[0][0])
            
            #determine winnings based on results
            betInfo = c.execute("SELECT PREDICTION, TO_WIN, BET FROM PREDICTIONS WHERE ID = "+str(predID)).fetchall()
            pred = betInfo[0][0]
            if pred == 'AWAY_WIN':
                pred = 'AWAY'
            elif pred == 'HOME_WIN':
                pred = 'HOME'
            
            if pred == matchRes:
                correct = 'Y'
            else:
                correct = 'N'
            
            if betInfo[0][2] == 'N':
                win = 0
            else:
                if correct == 'Y':
                    win = betInfo[0][1]
                else:
                    win = -1.00
                
            predUpdate1 = "UPDATE PREDICTIONS SET WINNINGS = "+str(win)+" WHERE ID = "+str(predID)
            predUpdate2 = "UPDATE PREDICTIONS SET CORRECT = '"+str(correct)+"' WHERE ID = "+str(predID)
    
            c.execute(predUpdate1)
            c.execute(predUpdate2)
            
            conn.commit() 
            conn.close()
            
        
            inserts += 1
            
            
            print('Inserted ' +str(iTEAM2)+' v ' +str(iTEAM1) + ' from ' + str(iEVENT_DATE) + ' ('+str(urlNum)+')')    
        else:
            print('URL '+str(urlNum)+ ' does not need to be updated')
        #iterate through urlNum in loop    
        urlNum += 1




"""
Connor Buchanan
Odds_Pull.py
version 1.0 - 1/1/2021

Interacts with Fanduel to pull json response of all EPL games. 
Aggregates each outcome to a single line. Reduces fields to only relevant few.
"""



#import needed libraries
import requests
import pandas as pd
from pandas.io.json import json_normalize
from functools import reduce
import numpy as np

#get odds frm fanduel soccer site
#translate json data to dataframe
#used for main event page
def parse_data(jsonData):
    results_df = pd.DataFrame()
    for alpha in jsonData['events']:
        print ('Gathering %s data: %s @ %s' %(alpha['sportname'],alpha['participantname_away'],alpha['participantname_home']))
        alpha_df = json_normalize(alpha).drop('markets',axis=1)
        for beta in alpha['markets']:
            beta_df = json_normalize(beta).drop('selections',axis=1)
            beta_df.columns = [str(col) + '.markets' for col in beta_df.columns]
            for theta in beta['selections']:
                theta_df = json_normalize(theta)
                theta_df.columns = [str(col) + '.selections' for col in theta_df.columns]
                temp_df = reduce(lambda left,right: pd.merge(left,right, left_index=True, right_index=True), [alpha_df, beta_df, theta_df])
                results_df = results_df.append(temp_df, sort=True).reset_index(drop=True)
    return results_df

#define function to calculate odds based on fanduel return
#current pricedown is amount bet
#current priceup is amount to be returned
# if price down is greater then (pricedown / priceup) * 100 = odds
# if price up is greater then (priceup / pricedown) * 100 = odds
def odds_calc(dataframe):
    newDF = dataframe
    newDF['Odds'] = 0
    for rec in range(len(newDF)):
        priceDown = newDF['currentpricedown.selections'][rec]
        priceUp = newDF['currentpriceup.selections'][rec]
        if priceDown > priceUp:
            newDF['Odds'][rec] = (priceDown / priceUp) * -100
        elif priceUp > priceDown:
            newDF['Odds'][rec] = (priceUp / priceDown) * 100
        else:
            newDF['Odds'][rec] = 100
        print ('Odds for ' + str(newDF['eventname'][rec]) + ': ' + str(newDF['name.selections'][rec]) + ' are ' + str(newDF['Odds'][rec]))
    return newDF


"""EPL Scrape"""
jsonData_fanduel = requests.get('https://sportsbook.fanduel.com/cache/psmg/UK/49625.3.json').json()
fanduel = parse_data(jsonData_fanduel)

oddsDF = odds_calc(fanduel)

#create a new dataframe with only relevant fields
reducedDF = pd.DataFrame()
reducedDF['Event_ID'] = oddsDF['eventlistcode'] 
reducedDF['Date'] = oddsDF['tsstart'].str[:10]
reducedDF['Game'] = oddsDF['eventname']
new = reducedDF['Game'].str.split(' v ',n=1,expand=True)
reducedDF['Home'] = new[0]
reducedDF['Away'] = new[1]
reducedDF['Pick'] = oddsDF['name.selections']
reducedDF['Odds'] = oddsDF['Odds']
reducedDF['Dollar_Returns'] = np.round(oddsDF['currentpriceup.selections'] / oddsDF['currentpricedown.selections'],decimals=2)

#code for result viewing, delete later
#reducedDF.head()

#export to excel
#reducedDF.to_excel('fanduel_df.xlsx')

"""Update SQLite database code section"""
#establish database connection
import sqlite3
conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
c = conn.cursor()

"""Move old entries to history table before deleting all odds records"""
c.execute("DELETE FROM ODDS")

#start of loop to update all rows in the dataframe
dfLen = len(reducedDF)
i = 0

while i < dfLen:
    #assign variable values for insertion statement
    eventID = reducedDF['Event_ID'][i]
    eventDate = reducedDF['Date'][i]
    game = reducedDF['Game'][i]
    homeName = reducedDF['Home'][i]
    awayName = reducedDF['Away'][i]
    
    #logic to correctly derive odds fields
    pick1 = reducedDF['Pick'][i]
    pick2 = reducedDF['Pick'][i+1]
    pick3 = reducedDF['Pick'][i+2]
    if homeName == pick1:
        homeWin = reducedDF['Dollar_Returns'][i]
        if awayName == pick2:
            awayWin = reducedDF['Dollar_Returns'][i+1]
            draw = reducedDF['Dollar_Returns'][i+2]
        else:
            awayWin = reducedDF['Dollar_Returns'][i+2]
            draw = reducedDF['Dollar_Returns'][i+1]
    elif awayName == pick1:
        awayWin = reducedDF['Dollar_Returns'][i]
        if homeName == pick2:
            homeWin = reducedDF['Dollar_Returns'][i+1]
            draw = reducedDF['Dollar_Returns'][i+2]
        else:
            homeWin = reducedDF['Dollar_Returns'][i+2]
            draw = reducedDF['Dollar_Returns'][i+1]
    else:
        draw = reducedDF['Dollar_Returns'][i]
        if homeName == pick2:
            homeWin = reducedDF['Dollar_Returns'][i+1]
            awayWin = reducedDF['Dollar_Returns'][i+2]
        else:
            homeWin = reducedDF['Dollar_Returns'][i+2]
            awayWin = reducedDF['Dollar_Returns'][i+1] 
    
    #create string to insert each row into the database
    execString = "INSERT INTO ODDS (EVENT_ID, EVENT_DATE, GAME, HOME_NAME, AWAY_NAME, HOME_WIN, AWAY_WIN, DRAW, HOME_ID, AWAY_ID) VALUES (" \
              "'"+str(eventID)+"','"+str(eventDate)+"','"+str(game)+"','"+str(homeName)+"','"+str(awayName)+"',"+str(homeWin)+ \
              ','+str(awayWin)+','+str(draw)+','+ \
              '(SELECT TEAM_ID FROM TEAMS WHERE FANDUEL = '+"'"+str(homeName)+"')," \
              '(SELECT TEAM_ID FROM TEAMS WHERE FANDUEL = '+"'"+str(awayName)+"'))"
    #insert calculated string
    c.execute(execString)
    
    #iterate by 3 due to one line per pick nature of dataframe 
    i += 3

#close the database connection
conn.commit() 
conn.close()


"""La Liga"""
jsonData_fanduel = requests.get('https://sportsbook.fanduel.com/cache/psmg/UK/49654.3.json').json()
fanduel = parse_data(jsonData_fanduel)

oddsDF = odds_calc(fanduel)

#create a new dataframe with only relevant fields
reducedDF = pd.DataFrame()
reducedDF['Event_ID'] = oddsDF['eventlistcode'] 
reducedDF['Date'] = oddsDF['tsstart'].str[:10]
reducedDF['Game'] = oddsDF['eventname']
new = reducedDF['Game'].str.split(' v ',n=1,expand=True)
reducedDF['Home'] = new[0]
reducedDF['Away'] = new[1]
reducedDF['Pick'] = oddsDF['name.selections']
reducedDF['Odds'] = oddsDF['Odds']
reducedDF['Dollar_Returns'] = np.round(oddsDF['currentpriceup.selections'] / oddsDF['currentpricedown.selections'],decimals=2)

#code for result viewing, delete later
#reducedDF.head()

#export to excel
#reducedDF.to_excel('fanduel_df.xlsx')

"""Update SQLite database code section"""
#establish database connection
import sqlite3
conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
c = conn.cursor()


#start of loop to update all rows in the dataframe
dfLen = len(reducedDF)
i = 0

while i < dfLen:
    #assign variable values for insertion statement
    eventID = reducedDF['Event_ID'][i]
    eventDate = reducedDF['Date'][i]
    game = reducedDF['Game'][i]
    homeName = reducedDF['Home'][i]
    awayName = reducedDF['Away'][i]
    
    #logic to correctly derive odds fields
    pick1 = reducedDF['Pick'][i]
    pick2 = reducedDF['Pick'][i+1]
    pick3 = reducedDF['Pick'][i+2]
    if homeName == pick1:
        homeWin = reducedDF['Dollar_Returns'][i]
        if awayName == pick2:
            awayWin = reducedDF['Dollar_Returns'][i+1]
            draw = reducedDF['Dollar_Returns'][i+2]
        else:
            awayWin = reducedDF['Dollar_Returns'][i+2]
            draw = reducedDF['Dollar_Returns'][i+1]
    elif awayName == pick1:
        awayWin = reducedDF['Dollar_Returns'][i]
        if homeName == pick2:
            homeWin = reducedDF['Dollar_Returns'][i+1]
            draw = reducedDF['Dollar_Returns'][i+2]
        else:
            homeWin = reducedDF['Dollar_Returns'][i+2]
            draw = reducedDF['Dollar_Returns'][i+1]
    else:
        draw = reducedDF['Dollar_Returns'][i]
        if homeName == pick2:
            homeWin = reducedDF['Dollar_Returns'][i+1]
            awayWin = reducedDF['Dollar_Returns'][i+2]
        else:
            homeWin = reducedDF['Dollar_Returns'][i+2]
            awayWin = reducedDF['Dollar_Returns'][i+1] 
    
    #create string to insert each row into the database
    execString = "INSERT INTO ODDS (EVENT_ID, EVENT_DATE, GAME, HOME_NAME, AWAY_NAME, HOME_WIN, AWAY_WIN, DRAW, HOME_ID, AWAY_ID) VALUES (" \
              "'"+str(eventID)+"','"+str(eventDate)+"','"+str(game)+"','"+str(homeName)+"','"+str(awayName)+"',"+str(homeWin)+ \
              ','+str(awayWin)+','+str(draw)+','+ \
              '(SELECT TEAM_ID FROM TEAMS WHERE FANDUEL = '+"'"+str(homeName)+"')," \
              '(SELECT TEAM_ID FROM TEAMS WHERE FANDUEL = '+"'"+str(awayName)+"'))"
    #insert calculated string
    c.execute(execString)
    
    #iterate by 3 due to one line per pick nature of dataframe 
    i += 3

#close the database connection
conn.commit() 
conn.close()


"""Bundesliga"""
jsonData_fanduel = requests.get('https://sportsbook.fanduel.com/cache/psmg/UK/49768.3.json').json()
fanduel = parse_data(jsonData_fanduel)

oddsDF = odds_calc(fanduel)

#create a new dataframe with only relevant fields
reducedDF = pd.DataFrame()
reducedDF['Event_ID'] = oddsDF['eventlistcode'] 
reducedDF['Date'] = oddsDF['tsstart'].str[:10]
reducedDF['Game'] = oddsDF['eventname']
new = reducedDF['Game'].str.split(' v ',n=1,expand=True)
reducedDF['Home'] = new[0]
reducedDF['Away'] = new[1]
reducedDF['Pick'] = oddsDF['name.selections']
reducedDF['Odds'] = oddsDF['Odds']
reducedDF['Dollar_Returns'] = np.round(oddsDF['currentpriceup.selections'] / oddsDF['currentpricedown.selections'],decimals=2)

#code for result viewing, delete later
#reducedDF.head()

#export to excel
#reducedDF.to_excel('fanduel_df.xlsx')

"""Update SQLite database code section"""
#establish database connection
import sqlite3
conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
c = conn.cursor()


#start of loop to update all rows in the dataframe
dfLen = len(reducedDF)
i = 0

while i < dfLen:
    #assign variable values for insertion statement
    eventID = reducedDF['Event_ID'][i]
    eventDate = reducedDF['Date'][i]
    game = reducedDF['Game'][i]
    homeName = reducedDF['Home'][i]
    awayName = reducedDF['Away'][i]
    
    #logic to correctly derive odds fields
    pick1 = reducedDF['Pick'][i]
    pick2 = reducedDF['Pick'][i+1]
    pick3 = reducedDF['Pick'][i+2]
    if homeName == pick1:
        homeWin = reducedDF['Dollar_Returns'][i]
        if awayName == pick2:
            awayWin = reducedDF['Dollar_Returns'][i+1]
            draw = reducedDF['Dollar_Returns'][i+2]
        else:
            awayWin = reducedDF['Dollar_Returns'][i+2]
            draw = reducedDF['Dollar_Returns'][i+1]
    elif awayName == pick1:
        awayWin = reducedDF['Dollar_Returns'][i]
        if homeName == pick2:
            homeWin = reducedDF['Dollar_Returns'][i+1]
            draw = reducedDF['Dollar_Returns'][i+2]
        else:
            homeWin = reducedDF['Dollar_Returns'][i+2]
            draw = reducedDF['Dollar_Returns'][i+1]
    else:
        draw = reducedDF['Dollar_Returns'][i]
        if homeName == pick2:
            homeWin = reducedDF['Dollar_Returns'][i+1]
            awayWin = reducedDF['Dollar_Returns'][i+2]
        else:
            homeWin = reducedDF['Dollar_Returns'][i+2]
            awayWin = reducedDF['Dollar_Returns'][i+1] 
    
    #create string to insert each row into the database
    execString = "INSERT INTO ODDS (EVENT_ID, EVENT_DATE, GAME, HOME_NAME, AWAY_NAME, HOME_WIN, AWAY_WIN, DRAW, HOME_ID, AWAY_ID) VALUES (" \
              "'"+str(eventID)+"','"+str(eventDate)+"','"+str(game)+"','"+str(homeName)+"','"+str(awayName)+"',"+str(homeWin)+ \
              ','+str(awayWin)+','+str(draw)+','+ \
              '(SELECT TEAM_ID FROM TEAMS WHERE FANDUEL = '+"'"+str(homeName)+"')," \
              '(SELECT TEAM_ID FROM TEAMS WHERE FANDUEL = '+"'"+str(awayName)+"'))"
    #insert calculated string
    c.execute(execString)
    
    #iterate by 3 due to one line per pick nature of dataframe 
    i += 3

#close the database connection
conn.commit() 
conn.close()



"""Serie A"""
jsonData_fanduel = requests.get('https://sportsbook.fanduel.com/cache/psmg/UK/49751.3.json').json()
fanduel = parse_data(jsonData_fanduel)

oddsDF = odds_calc(fanduel)

#create a new dataframe with only relevant fields
reducedDF = pd.DataFrame()
reducedDF['Event_ID'] = oddsDF['eventlistcode'] 
reducedDF['Date'] = oddsDF['tsstart'].str[:10]
reducedDF['Game'] = oddsDF['eventname']
new = reducedDF['Game'].str.split(' v ',n=1,expand=True)
reducedDF['Home'] = new[0]
reducedDF['Away'] = new[1]
reducedDF['Pick'] = oddsDF['name.selections']
reducedDF['Odds'] = oddsDF['Odds']
reducedDF['Dollar_Returns'] = np.round(oddsDF['currentpriceup.selections'] / oddsDF['currentpricedown.selections'],decimals=2)

#code for result viewing, delete later
#reducedDF.head()

#export to excel
#reducedDF.to_excel('fanduel_df.xlsx')

"""Update SQLite database code section"""
#establish database connection
import sqlite3
conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
c = conn.cursor()


#start of loop to update all rows in the dataframe
dfLen = len(reducedDF)
i = 0

while i < dfLen:
    #assign variable values for insertion statement
    eventID = reducedDF['Event_ID'][i]
    eventDate = reducedDF['Date'][i]
    game = reducedDF['Game'][i]
    homeName = reducedDF['Home'][i]
    awayName = reducedDF['Away'][i]
    
    #logic to correctly derive odds fields
    pick1 = reducedDF['Pick'][i]
    pick2 = reducedDF['Pick'][i+1]
    pick3 = reducedDF['Pick'][i+2]
    if homeName == pick1:
        homeWin = reducedDF['Dollar_Returns'][i]
        if awayName == pick2:
            awayWin = reducedDF['Dollar_Returns'][i+1]
            draw = reducedDF['Dollar_Returns'][i+2]
        else:
            awayWin = reducedDF['Dollar_Returns'][i+2]
            draw = reducedDF['Dollar_Returns'][i+1]
    elif awayName == pick1:
        awayWin = reducedDF['Dollar_Returns'][i]
        if homeName == pick2:
            homeWin = reducedDF['Dollar_Returns'][i+1]
            draw = reducedDF['Dollar_Returns'][i+2]
        else:
            homeWin = reducedDF['Dollar_Returns'][i+2]
            draw = reducedDF['Dollar_Returns'][i+1]
    else:
        draw = reducedDF['Dollar_Returns'][i]
        if homeName == pick2:
            homeWin = reducedDF['Dollar_Returns'][i+1]
            awayWin = reducedDF['Dollar_Returns'][i+2]
        else:
            homeWin = reducedDF['Dollar_Returns'][i+2]
            awayWin = reducedDF['Dollar_Returns'][i+1] 
    
    #create string to insert each row into the database
    execString = "INSERT INTO ODDS (EVENT_ID, EVENT_DATE, GAME, HOME_NAME, AWAY_NAME, HOME_WIN, AWAY_WIN, DRAW, HOME_ID, AWAY_ID) VALUES (" \
              "'"+str(eventID)+"','"+str(eventDate)+"','"+str(game)+"','"+str(homeName)+"','"+str(awayName)+"',"+str(homeWin)+ \
              ','+str(awayWin)+','+str(draw)+','+ \
              '(SELECT TEAM_ID FROM TEAMS WHERE FANDUEL = '+"'"+str(homeName)+"')," \
              '(SELECT TEAM_ID FROM TEAMS WHERE FANDUEL = '+"'"+str(awayName)+"'))"
    #insert calculated string
    c.execute(execString)
    
    #iterate by 3 due to one line per pick nature of dataframe 
    i += 3

#close the database connection
conn.commit() 
conn.close()



"""Ligue 1"""
jsonData_fanduel = requests.get('https://sportsbook.fanduel.com/cache/psmg/UK/49761.3.json').json()
fanduel = parse_data(jsonData_fanduel)

oddsDF = odds_calc(fanduel)

#create a new dataframe with only relevant fields
reducedDF = pd.DataFrame()
reducedDF['Event_ID'] = oddsDF['eventlistcode'] 
reducedDF['Date'] = oddsDF['tsstart'].str[:10]
reducedDF['Game'] = oddsDF['eventname']
new = reducedDF['Game'].str.split(' v ',n=1,expand=True)
reducedDF['Home'] = new[0]
reducedDF['Away'] = new[1]
reducedDF['Pick'] = oddsDF['name.selections']
reducedDF['Odds'] = oddsDF['Odds']
reducedDF['Dollar_Returns'] = np.round(oddsDF['currentpriceup.selections'] / oddsDF['currentpricedown.selections'],decimals=2)

#code for result viewing, delete later
#reducedDF.head()

#export to excel
#reducedDF.to_excel('fanduel_df.xlsx')

"""Update SQLite database code section"""
#establish database connection
import sqlite3
conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
c = conn.cursor()


#start of loop to update all rows in the dataframe
dfLen = len(reducedDF)
i = 0

while i < dfLen:
    #assign variable values for insertion statement
    eventID = reducedDF['Event_ID'][i]
    eventDate = reducedDF['Date'][i]
    game = reducedDF['Game'][i]
    homeName = reducedDF['Home'][i]
    awayName = reducedDF['Away'][i]
    
    #logic to correctly derive odds fields
    pick1 = reducedDF['Pick'][i]
    pick2 = reducedDF['Pick'][i+1]
    pick3 = reducedDF['Pick'][i+2]
    if homeName == pick1:
        homeWin = reducedDF['Dollar_Returns'][i]
        if awayName == pick2:
            awayWin = reducedDF['Dollar_Returns'][i+1]
            draw = reducedDF['Dollar_Returns'][i+2]
        else:
            awayWin = reducedDF['Dollar_Returns'][i+2]
            draw = reducedDF['Dollar_Returns'][i+1]
    elif awayName == pick1:
        awayWin = reducedDF['Dollar_Returns'][i]
        if homeName == pick2:
            homeWin = reducedDF['Dollar_Returns'][i+1]
            draw = reducedDF['Dollar_Returns'][i+2]
        else:
            homeWin = reducedDF['Dollar_Returns'][i+2]
            draw = reducedDF['Dollar_Returns'][i+1]
    else:
        draw = reducedDF['Dollar_Returns'][i]
        if homeName == pick2:
            homeWin = reducedDF['Dollar_Returns'][i+1]
            awayWin = reducedDF['Dollar_Returns'][i+2]
        else:
            homeWin = reducedDF['Dollar_Returns'][i+2]
            awayWin = reducedDF['Dollar_Returns'][i+1] 
    
    #create string to insert each row into the database
    execString = "INSERT INTO ODDS (EVENT_ID, EVENT_DATE, GAME, HOME_NAME, AWAY_NAME, HOME_WIN, AWAY_WIN, DRAW, HOME_ID, AWAY_ID) VALUES (" \
              "'"+str(eventID)+"','"+str(eventDate)+"','"+str(game)+"','"+str(homeName)+"','"+str(awayName)+"',"+str(homeWin)+ \
              ','+str(awayWin)+','+str(draw)+','+ \
              '(SELECT TEAM_ID FROM TEAMS WHERE FANDUEL = '+"'"+str(homeName)+"')," \
              '(SELECT TEAM_ID FROM TEAMS WHERE FANDUEL = '+"'"+str(awayName)+"'))"
    #insert calculated string
    c.execute(execString)
    
    #iterate by 3 due to one line per pick nature of dataframe 
    i += 3

#close the database connection
conn.commit() 
conn.close()



# -*- coding: utf-8 -*-

"""
Connor Buchanan
Match_Stats.py
version 1.0 - 1/9/2021

Recurring process to identify upcoming matches and populate all prediction tables with relevant information
"""


#imports
import sqlite3
import pandas as pd

#connect to soccer database
conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
c = conn.cursor()

#max url to use for temporary URL assignement
#uses max value where result is null
#if that doesn't exist uses max value + 900,000
url = c.execute("SELECT MAX(URL_ID) FROM MATCH WHERE RESULT IS NULL").fetchall()
isValue = not all(url[0])
if isValue == True:
    url = c.execute("SELECT MAX(URL_ID) FROM MATCH").fetchall()
    maxURL = int(url[0][0]) + 900000
else:
    maxURL = int(url[0][0])


#first query to pull existing future matches from MATCH table
matchDF = pd.read_sql_query("SELECT EVENT_DATE, HOME_TEAM, AWAY_TEAM FROM MATCH WHERE RESULT IS NULL",conn)

#second query to pull odds data
oddsDF = pd.read_sql_query("SELECT O.EVENT_DATE, HT.UNDERSTAT AS HOME, AT.UNDERSTAT AS AWAY, HT.LEAGUE FROM ODDS O " \
                           +"JOIN TEAMS HT ON HT.FANDUEL = O.HOME_NAME JOIN TEAMS AT ON AT.FANDUEL = O.AWAY_NAME " \
                           +"ORDER BY EVENT_DATE",conn)

#close connection
conn.close()


#add new column to dataframe indicating if it should be removed
oddsDF['Remove'] = 'FALSE'

#remove any 2nd games from odds dataframe. Only first upcomming game for each team should be added
dfLen = range(len(oddsDF))
for i in dfLen:
    for j in dfLen:
        if j > i:
            iHome = oddsDF['HOME'][i]
            iAway = oddsDF['AWAY'][i]
            jHome = oddsDF['HOME'][j]
            jAway = oddsDF['AWAY'][j]
            if iHome == jHome:
                oddsDF['Remove'][j] = 'TRUE'
            elif iHome == jAway:
                oddsDF['Remove'][j] = 'TRUE'
            elif iAway == jHome:
                oddsDF['Remove'][j] = 'TRUE'
            elif iAway == jAway:
                oddsDF['Remove'][j] = 'TRUE'

#remove all duplicates
oddsDF = oddsDF.drop(oddsDF[oddsDF.Remove=='TRUE'].index, inplace=False)
oddsDF = oddsDF.reset_index(drop=True)

#reset oddsDF value for later removal
oddsDF['Remove'] = 'FALSE'

#check to see if odds records already exist in match database. if not, add them
if isValue == False:
    for i in range(len(oddsDF)):
        for j in range(len(matchDF)):
            if oddsDF['HOME'][i] == matchDF['HOME_TEAM'][j]:
                if oddsDF['AWAY'][i] == matchDF['AWAY_TEAM'][j]:
                    if oddsDF['EVENT_DATE'][i] == matchDF['EVENT_DATE'][j]:
                        oddsDF['Remove'][i] = 'TRUE'
                        
#remove all unneeded entries
oddsDF = oddsDF.drop(oddsDF[oddsDF.Remove=='TRUE'].index, inplace=False)
oddsDF = oddsDF.reset_index(drop=True)

#oddsDF is now update with entries to be added


#update match database with new games if exists
for i in range(len(oddsDF)):
    conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
    c = conn.cursor()
    
    maxURL += 1
    
    """GLOBAL VARIABLES FOR QUERIES"""
    URL_ID = maxURL
    LEAGUE = oddsDF['LEAGUE'][i]
    HOME_TEAM = oddsDF['HOME'][i]
    AWAY_TEAM = oddsDF['AWAY'][i]
    EVENT_DATE = oddsDF['EVENT_DATE'][i]
    
    
    """BIG SIX VARIABLES"""
    home6String = "SELECT BIG_SIX FROM TEAMS WHERE UNDERSTAT = '"+str(HOME_TEAM)+"'"
    home6 = c.execute(home6String).fetchall()
    
    away6String = "SELECT BIG_SIX FROM TEAMS WHERE UNDERSTAT = '"+str(AWAY_TEAM)+"'"
    away6 = c.execute(away6String).fetchall()
    
        
    HOME_BIG_SIX = home6[0][0]
    AWAY_BIG_SIX = away6[0][0]
    
    
    """HOME LAST 5 VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/5.00,SUM(XPTS)/5.00,SUM(GOALS)/5.00,SUM(XG)/5.00,SUM(OPP_GOALS)/5.00,SUM(OPP_XG)/5.00," \
                    +"SUM(CHANCES)/5.00,SUM(SHOTS)/5.00,SUM(ShOTS_TARGET)/5.00,SUM(OPP_SHOTS)/5.00,SUM(OPP_SHOTS_TARGET)/5.00," \
                    +"SUM(DEEP)/5.00,SUM(PPDA)/5.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(HOME_TEAM) \
                    +"' ORDER BY EVENT_DATE DESC LIMIT 5)"
    queryRes = c.execute(queryString).fetchall()
    
    H_PTS_5 = round(queryRes[0][0] or 0,2)
    H_XPTS_5 = round(queryRes[0][1] or 0,2)
    H_G_5 = round(queryRes[0][2] or 0,2)
    H_XG_5 = round(queryRes[0][3] or 0,2)
    H_OPP_G_5 = round(queryRes[0][4] or 0,2)
    H_OPP_XG_5 = round(queryRes[0][5] or 0,2)
    H_CH_5 = round(queryRes[0][6] or 0,2)
    H_SH_5 = round(queryRes[0][7] or 0,2)
    H_SHT_5 = round(queryRes[0][8] or 0,2)
    H_OPP_SH_5 = round(queryRes[0][9] or 0,2)
    H_OPP_SHT_5 = round(queryRes[0][10] or 0,2)
    H_DEEP_5 = round(queryRes[0][11] or 0,2)
    H_PPDA_5 = round(queryRes[0][12] or 0,2)
    
    
    """HOME LAST 10 VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/10.00,SUM(XPTS)/10.00,SUM(GOALS)/10.00,SUM(XG)/10.00,SUM(OPP_GOALS)/10.00,SUM(OPP_XG)/10.00," \
                    +"SUM(CHANCES)/10.00,SUM(SHOTS)/10.00,SUM(ShOTS_TARGET)/10.00,SUM(OPP_SHOTS)/10.00,SUM(OPP_SHOTS_TARGET)/10.00," \
                    +"SUM(DEEP)/10.00,SUM(PPDA)/10.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(HOME_TEAM) \
                    +"' ORDER BY EVENT_DATE DESC LIMIT 10)"
    queryRes = c.execute(queryString).fetchall()
    
    H_PTS_10 = round(queryRes[0][0] or 0,2)
    H_XPTS_10 = round(queryRes[0][1] or 0,2)
    H_G_10 = round(queryRes[0][2] or 0,2)
    H_XG_10 = round(queryRes[0][3] or 0,2)
    H_OPP_G_10 = round(queryRes[0][4] or 0,2)
    H_OPP_XG_10 = round(queryRes[0][5] or 0,2)
    H_CH_10 = round(queryRes[0][6] or 0,2)
    H_SH_10 = round(queryRes[0][7] or 0,2)
    H_SHT_10 = round(queryRes[0][8] or 0,2)
    H_OPP_SH_10 = round(queryRes[0][9] or 0,2)
    H_OPP_SHT_10 = round(queryRes[0][10] or 0,2)
    H_DEEP_10 = round(queryRes[0][11] or 0,2)
    H_PPDA_10 = round(queryRes[0][12] or 0,2)

    
    """HOME LAST 20 VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/20.00,SUM(XPTS)/20.00,SUM(GOALS)/20.00,SUM(XG)/20.00,SUM(OPP_GOALS)/20.00,SUM(OPP_XG)/20.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(HOME_TEAM) \
                    +"' ORDER BY EVENT_DATE DESC LIMIT 20)"
    queryRes = c.execute(queryString).fetchall()
    
    H_PTS_20 = round(queryRes[0][0] or 0,2)
    H_XPTS_20 = round(queryRes[0][1] or 0,2)
    H_G_20 = round(queryRes[0][2] or 0,2)
    H_XG_20 = round(queryRes[0][3] or 0,2)
    H_OPP_G_20 = round(queryRes[0][4] or 0,2)
    H_OPP_XG_20 = round(queryRes[0][5] or 0,2)


    """HOME LAST 5 VS OPPTYPE VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/5.00,SUM(XPTS)/5.00,SUM(GOALS)/5.00,SUM(XG)/5.00,SUM(OPP_GOALS)/5.00,SUM(OPP_XG)/5.00," \
                    +"SUM(CHANCES)/5.00,SUM(SHOTS)/5.00,SUM(ShOTS_TARGET)/5.00,SUM(OPP_SHOTS)/5.00,SUM(OPP_SHOTS_TARGET)/5.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE JOIN TEAMS ON OPPONENT = UNDERSTAT " \
                    +"WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(HOME_TEAM)+"' AND BIG_SIX = "+str(AWAY_BIG_SIX) \
                    +" ORDER BY EVENT_DATE DESC LIMIT 5)"
    queryRes = c.execute(queryString).fetchall()
    
    H_PTS_V_OPPTYPE_5 = round(queryRes[0][0] or 0,2)
    H_XPTS_V_OPPTYPE_5 = round(queryRes[0][1] or 0,2)
    H_G_V_OPPTYPE_5 = round(queryRes[0][2] or 0,2)
    H_XG_V_OPPTYPE_5 = round(queryRes[0][3] or 0,2)
    H_OPP_G_V_OPPTYPE_5 = round(queryRes[0][4] or 0,2)
    H_OPP_XG_V_OPPTYPE_5 = round(queryRes[0][5] or 0,2)
    H_CH_V_OPPTYPE_5 = round(queryRes[0][6] or 0,2)
    H_SH_V_OPPTYPE_5 = round(queryRes[0][7] or 0,2)
    H_SHT_V_OPPTYPE_5 = round(queryRes[0][8] or 0,2)
    H_OPP_SH_V_OPPTYPE_5 = round(queryRes[0][9] or 0,2)
    H_OPP_SHT_V_OPPTYPE_5 = round(queryRes[0][10] or 0,2)
    
    
    """HOME LAST 10 VS OPPTYPE VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/10.00,SUM(XPTS)/10.00,SUM(GOALS)/10.00,SUM(XG)/10.00,SUM(OPP_GOALS)/10.00,SUM(OPP_XG)/10.00," \
                    +"SUM(CHANCES)/10.00,SUM(SHOTS)/10.00,SUM(ShOTS_TARGET)/10.00,SUM(OPP_SHOTS)/10.00,SUM(OPP_SHOTS_TARGET)/10.00," \
                    +"SUM(DEEP)/10.00,SUM(PPDA)/10.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE JOIN TEAMS ON OPPONENT = UNDERSTAT " \
                    +"WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(HOME_TEAM)+"' AND BIG_SIX = "+str(AWAY_BIG_SIX) \
                    +" ORDER BY EVENT_DATE DESC LIMIT 10)"
    queryRes = c.execute(queryString).fetchall()
    
    H_PTS_V_OPPTYPE_10 = round(queryRes[0][0] or 0,2)
    H_XPTS_V_OPPTYPE_10 = round(queryRes[0][1] or 0,2)
    H_G_V_OPPTYPE_10 = round(queryRes[0][2] or 0,2)
    H_XG_V_OPPTYPE_10 = round(queryRes[0][3] or 0,2)
    H_OPP_G_V_OPPTYPE_10 = round(queryRes[0][4] or 0,2)
    H_OPP_XG_V_OPPTYPE_10 = round(queryRes[0][5] or 0,2)
    H_CH_V_OPPTYPE_10 = round(queryRes[0][6] or 0,2)
    H_SH_V_OPPTYPE_10 = round(queryRes[0][7] or 0,2)
    H_SHT_V_OPPTYPE_10 = round(queryRes[0][8] or 0,2)
    H_OPP_SH_V_OPPTYPE_10 = round(queryRes[0][9] or 0,2)
    H_OPP_SHT_V_OPPTYPE_10 = round(queryRes[0][10] or 0,2)
    H_DEEP_V_OPPTYPE_10 = round(queryRes[0][11] or 0,2)
    H_PPDA_V_OPPTYPE_10 = round(queryRes[0][12] or 0,2)
    
    
    """HOME LAST 5 HOME VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/5.00,SUM(XPTS)/5.00,SUM(GOALS)/5.00,SUM(XG)/5.00,SUM(OPP_GOALS)/5.00,SUM(OPP_XG)/5.00," \
                    +"SUM(CHANCES)/5.00,SUM(SHOTS)/5.00,SUM(ShOTS_TARGET)/5.00,SUM(OPP_SHOTS)/5.00,SUM(OPP_SHOTS_TARGET)/5.00"  \
                    +" FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(HOME_TEAM) \
                    +"' AND HOME_AWAY = 'HOME' ORDER BY EVENT_DATE DESC LIMIT 5)"
    queryRes = c.execute(queryString).fetchall()
    
    H_PTS_HOME_5 = round(queryRes[0][0] or 0,2)
    H_XPTS_HOME_5 = round(queryRes[0][1] or 0,2)
    H_G_HOME_5 = round(queryRes[0][2] or 0,2)
    H_XG_HOME_5 = round(queryRes[0][3] or 0,2)
    H_OPP_G_HOME_5 = round(queryRes[0][4] or 0,2)
    H_OPP_XG_HOME_5 = round(queryRes[0][5] or 0,2)
    H_CH_HOME_5 = round(queryRes[0][6] or 0,2)
    H_SH_HOME_5 = round(queryRes[0][7] or 0,2)
    H_SHT_HOME_5 = round(queryRes[0][8] or 0,2)
    H_OPP_SH_HOME_5 = round(queryRes[0][9] or 0,2)
    H_OPP_SHT_HOME_5 = round(queryRes[0][10] or 0,2)
    
    
    """HOME LAST 10 VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/10.00,SUM(XPTS)/10.00,SUM(GOALS)/10.00,SUM(XG)/10.00,SUM(OPP_GOALS)/10.00,SUM(OPP_XG)/10.00," \
                    +"SUM(CHANCES)/10.00,SUM(SHOTS)/10.00,SUM(ShOTS_TARGET)/10.00,SUM(OPP_SHOTS)/10.00,SUM(OPP_SHOTS_TARGET)/10.00," \
                    +"SUM(DEEP)/10.00,SUM(PPDA)/10.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(HOME_TEAM) \
                    +"' AND HOME_AWAY = 'HOME' ORDER BY EVENT_DATE DESC LIMIT 10)"
    queryRes = c.execute(queryString).fetchall()
    
    H_PTS_HOME_10 = round(queryRes[0][0] or 0,2)
    H_XPTS_HOME_10 = round(queryRes[0][1] or 0,2)
    H_G_HOME_10 = round(queryRes[0][2] or 0,2)
    H_XG_HOME_10 = round(queryRes[0][3] or 0,2)
    H_OPP_G_HOME_10 = round(queryRes[0][4] or 0,2)
    H_OPP_XG_HOME_10 = round(queryRes[0][5] or 0,2)
    H_CH_HOME_10 = round(queryRes[0][6] or 0,2)
    H_SH_HOME_10 = round(queryRes[0][7] or 0,2)
    H_SHT_HOME_10 = round(queryRes[0][8] or 0,2)
    H_OPP_SH_HOME_10 = round(queryRes[0][9] or 0,2)
    H_OPP_SHT_HOME_10 = round(queryRes[0][10] or 0,2)
    H_DEEP_HOME_10 = round(queryRes[0][11] or 0,2)
    H_PPDA_HOME_10 = round(queryRes[0][12] or 0,2)

    
    """HOME LAST 20 VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/20.00,SUM(XPTS)/20.00,SUM(GOALS)/20.00,SUM(XG)/20.00,SUM(OPP_GOALS)/20.00,SUM(OPP_XG)/20.00," \
                    +"SUM(CHANCES)/20.00,SUM(SHOTS)/20.00,SUM(ShOTS_TARGET)/20.00,SUM(OPP_SHOTS)/20.00,SUM(OPP_SHOTS_TARGET)/20.00" \
                    +" FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(HOME_TEAM) \
                    +"' AND HOME_AWAY = 'HOME' ORDER BY EVENT_DATE DESC LIMIT 10)"
    queryRes = c.execute(queryString).fetchall()
    
    H_PTS_HOME_20 = round(queryRes[0][0] or 0,2)
    H_XPTS_HOME_20 = round(queryRes[0][1] or 0,2)
    H_G_HOME_20 = round(queryRes[0][2] or 0,2)
    H_XG_HOME_20 = round(queryRes[0][3] or 0,2)
    H_OPP_G_HOME_20 = round(queryRes[0][4] or 0,2)
    H_OPP_XG_HOME_20 = round(queryRes[0][5] or 0,2)
    H_CH_HOME_20 = round(queryRes[0][6] or 0,2)
    H_SH_HOME_20 = round(queryRes[0][7] or 0,2)
    H_SHT_HOME_20 = round(queryRes[0][8] or 0,2)
    H_OPP_SH_HOME_20 = round(queryRes[0][9] or 0,2)
    H_OPP_SHT_HOME_20 = round(queryRes[0][10] or 0,2)


    """HOME LAST 5 VS OPPTYPE VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/5.00,SUM(XPTS)/5.00,SUM(GOALS)/5.00,SUM(XG)/5.00,SUM(OPP_GOALS)/5.00,SUM(OPP_XG)/5.00," \
                    +"SUM(CHANCES)/5.00,SUM(SHOTS)/5.00,SUM(ShOTS_TARGET)/5.00,SUM(OPP_SHOTS)/5.00,SUM(OPP_SHOTS_TARGET)/5.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE JOIN TEAMS ON OPPONENT = UNDERSTAT " \
                    +"WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(HOME_TEAM)+"' AND BIG_SIX = "+str(AWAY_BIG_SIX) \
                    +" AND HOME_AWAY = 'HOME' ORDER BY EVENT_DATE DESC LIMIT 5)"
    queryRes = c.execute(queryString).fetchall()
    
    H_PTS_HOME_V_OPPTYPE_5 = round(queryRes[0][0] or 0,2)
    H_XPTS_HOME_V_OPPTYPE_5 = round(queryRes[0][1] or 0,2)
    H_G_HOME_V_OPPTYPE_5 = round(queryRes[0][2] or 0,2)
    H_XG_HOME_V_OPPTYPE_5 = round(queryRes[0][3] or 0,2)
    H_OPP_G_HOME_V_OPPTYPE_5 = round(queryRes[0][4] or 0,2)
    H_OPP_XG_HOME_V_OPPTYPE_5 = round(queryRes[0][5] or 0,2)
    H_CH_HOME_V_OPPTYPE_5 = round(queryRes[0][6] or 0,2)
    H_SH_HOME_V_OPPTYPE_5 = round(queryRes[0][7] or 0,2)
    H_SHT_HOME_V_OPPTYPE_5 = round(queryRes[0][8] or 0,2)
    H_OPP_SH_HOME_V_OPPTYPE_5 = round(queryRes[0][9] or 0,2)
    H_OPP_SHT_HOME_V_OPPTYPE_5 = round(queryRes[0][10] or 0,2)
    
    
    """HOME LAST 10 VS OPPTYPE VARIABLES"""
    
    queryString = "SELECT SUM(POINTS)/10.00,SUM(XPTS)/10.00,SUM(GOALS)/10.00,SUM(XG)/10.00,SUM(OPP_GOALS)/10.00,SUM(OPP_XG)/10.00," \
                    +"SUM(CHANCES)/10.00,SUM(SHOTS)/10.00,SUM(ShOTS_TARGET)/10.00,SUM(OPP_SHOTS)/10.00,SUM(OPP_SHOTS_TARGET)/10.00," \
                    +"SUM(DEEP)/10.00,SUM(PPDA)/10.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE JOIN TEAMS ON OPPONENT = UNDERSTAT " \
                    +"WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(HOME_TEAM)+"' AND BIG_SIX = "+str(AWAY_BIG_SIX) \
                    +" AND HOME_AWAY = 'HOME' ORDER BY EVENT_DATE DESC LIMIT 10)"
    queryRes = c.execute(queryString).fetchall()
    
    H_PTS_HOME_V_OPPTYPE_10 = round(queryRes[0][0] or 0,2)
    H_XPTS_HOME_V_OPPTYPE_10 = round(queryRes[0][1] or 0,2)
    H_G_HOME_V_OPPTYPE_10 = round(queryRes[0][2] or 0,2)
    H_XG_HOME_V_OPPTYPE_10 = round(queryRes[0][3] or 0,2)
    H_OPP_G_HOME_V_OPPTYPE_10 = round(queryRes[0][4] or 0,2)
    H_OPP_XG_HOME_V_OPPTYPE_10 = round(queryRes[0][5] or 0,2)
    H_CH_HOME_V_OPPTYPE_10 = round(queryRes[0][6] or 0,2)
    H_SH_HOME_V_OPPTYPE_10 = round(queryRes[0][7] or 0,2)
    H_SHT_HOME_V_OPPTYPE_10 = round(queryRes[0][8] or 0,2)
    H_OPP_SH_HOME_V_OPPTYPE_10 = round(queryRes[0][9] or 0,2)
    H_OPP_SHT_HOME_V_OPPTYPE_10 = round(queryRes[0][10] or 0,2)
    H_DEEP_HOME_V_OPPTYPE_10 = round(queryRes[0][11] or 0,2)
    H_PPDA_HOME_V_OPPTYPE_10 = round(queryRes[0][12] or 0,2)
    
    """HOME VARIABLES ARE COMPLETE"""
    
    
    
    """BEGIN AWAY VARIABLES"""
    
    """AWAY LAST 5 VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/5.00,SUM(XPTS)/5.00,SUM(GOALS)/5.00,SUM(XG)/5.00,SUM(OPP_GOALS)/5.00,SUM(OPP_XG)/5.00," \
                    +"SUM(CHANCES)/5.00,SUM(SHOTS)/5.00,SUM(ShOTS_TARGET)/5.00,SUM(OPP_SHOTS)/5.00,SUM(OPP_SHOTS_TARGET)/5.00," \
                    +"SUM(DEEP)/5.00,SUM(PPDA)/5.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(AWAY_TEAM) \
                    +"' ORDER BY EVENT_DATE DESC LIMIT 5)"
    queryRes = c.execute(queryString).fetchall()
    
    A_PTS_5 = round(queryRes[0][0] or 0,2)
    A_XPTS_5 = round(queryRes[0][1] or 0,2)
    A_G_5 = round(queryRes[0][2] or 0,2)
    A_XG_5 = round(queryRes[0][3] or 0,2)
    A_OPP_G_5 = round(queryRes[0][4] or 0,2)
    A_OPP_XG_5 = round(queryRes[0][5] or 0,2)
    A_CH_5 = round(queryRes[0][6] or 0,2)
    A_SH_5 = round(queryRes[0][7] or 0,2)
    A_SHT_5 = round(queryRes[0][8] or 0,2)
    A_OPP_SH_5 = round(queryRes[0][9] or 0,2)
    A_OPP_SHT_5 = round(queryRes[0][10] or 0,2)
    A_DEEP_5 = round(queryRes[0][11] or 0,2)
    A_PPDA_5 = round(queryRes[0][12] or 0,2)
    
    
    """AWAY LAST 10 VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/10.00,SUM(XPTS)/10.00,SUM(GOALS)/10.00,SUM(XG)/10.00,SUM(OPP_GOALS)/10.00,SUM(OPP_XG)/10.00," \
                    +"SUM(CHANCES)/10.00,SUM(SHOTS)/10.00,SUM(ShOTS_TARGET)/10.00,SUM(OPP_SHOTS)/10.00,SUM(OPP_SHOTS_TARGET)/10.00," \
                    +"SUM(DEEP)/10.00,SUM(PPDA)/10.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(AWAY_TEAM) \
                    +"' ORDER BY EVENT_DATE DESC LIMIT 10)"
    queryRes = c.execute(queryString).fetchall()
    
    A_PTS_10 = round(queryRes[0][0] or 0,2)
    A_XPTS_10 = round(queryRes[0][1] or 0,2)
    A_G_10 = round(queryRes[0][2] or 0,2)
    A_XG_10 = round(queryRes[0][3] or 0,2)
    A_OPP_G_10 = round(queryRes[0][4] or 0,2)
    A_OPP_XG_10 = round(queryRes[0][5] or 0,2)
    A_CH_10 = round(queryRes[0][6] or 0,2)
    A_SH_10 = round(queryRes[0][7] or 0,2)
    A_SHT_10 = round(queryRes[0][8] or 0,2)
    A_OPP_SH_10 = round(queryRes[0][9] or 0,2)
    A_OPP_SHT_10 = round(queryRes[0][10] or 0,2)
    A_DEEP_10 = round(queryRes[0][11] or 0,2)
    A_PPDA_10 = round(queryRes[0][12] or 0,2)

    
    """AWAY LAST 20 VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/20.00,SUM(XPTS)/20.00,SUM(GOALS)/20.00,SUM(XG)/20.00,SUM(OPP_GOALS)/20.00,SUM(OPP_XG)/20.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(AWAY_TEAM) \
                    +"' ORDER BY EVENT_DATE DESC LIMIT 20)"
    queryRes = c.execute(queryString).fetchall()
    
    A_PTS_20 = round(queryRes[0][0] or 0,2)
    A_XPTS_20 = round(queryRes[0][1] or 0,2)
    A_G_20 = round(queryRes[0][2] or 0,2)
    A_XG_20 = round(queryRes[0][3] or 0,2)
    A_OPP_G_20 = round(queryRes[0][4] or 0,2)
    A_OPP_XG_20 = round(queryRes[0][5] or 0,2)


    """AWAY LAST 5 VS OPPTYPE VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/5.00,SUM(XPTS)/5.00,SUM(GOALS)/5.00,SUM(XG)/5.00,SUM(OPP_GOALS)/5.00,SUM(OPP_XG)/5.00," \
                    +"SUM(CHANCES)/5.00,SUM(SHOTS)/5.00,SUM(ShOTS_TARGET)/5.00,SUM(OPP_SHOTS)/5.00,SUM(OPP_SHOTS_TARGET)/5.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE JOIN TEAMS ON OPPONENT = UNDERSTAT " \
                    +"WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(AWAY_TEAM)+"' AND BIG_SIX = "+str(HOME_BIG_SIX) \
                    +" ORDER BY EVENT_DATE DESC LIMIT 5)"
    queryRes = c.execute(queryString).fetchall()
    
    A_PTS_V_OPPTYPE_5 = round(queryRes[0][0] or 0,2)
    A_XPTS_V_OPPTYPE_5 = round(queryRes[0][1] or 0,2)
    A_G_V_OPPTYPE_5 = round(queryRes[0][2] or 0,2)
    A_XG_V_OPPTYPE_5 = round(queryRes[0][3] or 0,2)
    A_OPP_G_V_OPPTYPE_5 = round(queryRes[0][4] or 0,2)
    A_OPP_XG_V_OPPTYPE_5 = round(queryRes[0][5] or 0,2)
    A_CH_V_OPPTYPE_5 = round(queryRes[0][6] or 0,2)
    A_SH_V_OPPTYPE_5 = round(queryRes[0][7] or 0,2)
    A_SHT_V_OPPTYPE_5 = round(queryRes[0][8] or 0,2)
    A_OPP_SH_V_OPPTYPE_5 = round(queryRes[0][9] or 0,2)
    A_OPP_SHT_V_OPPTYPE_5 = round(queryRes[0][10] or 0,2)
    
    
    """AWAY LAST 10 VS OPPTYPE VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/10.00,SUM(XPTS)/10.00,SUM(GOALS)/10.00,SUM(XG)/10.00,SUM(OPP_GOALS)/10.00,SUM(OPP_XG)/10.00," \
                    +"SUM(CHANCES)/10.00,SUM(SHOTS)/10.00,SUM(ShOTS_TARGET)/10.00,SUM(OPP_SHOTS)/10.00,SUM(OPP_SHOTS_TARGET)/10.00," \
                    +"SUM(DEEP)/10.00,SUM(PPDA)/10.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE JOIN TEAMS ON OPPONENT = UNDERSTAT " \
                    +"WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(AWAY_TEAM)+"' AND BIG_SIX = "+str(HOME_BIG_SIX) \
                    +" ORDER BY EVENT_DATE DESC LIMIT 10)"
    queryRes = c.execute(queryString).fetchall()
    
    A_PTS_V_OPPTYPE_10 = round(queryRes[0][0] or 0,2)
    A_XPTS_V_OPPTYPE_10 = round(queryRes[0][1] or 0,2)
    A_G_V_OPPTYPE_10 = round(queryRes[0][2] or 0,2)
    A_XG_V_OPPTYPE_10 = round(queryRes[0][3] or 0,2)
    A_OPP_G_V_OPPTYPE_10 = round(queryRes[0][4] or 0,2)
    A_OPP_XG_V_OPPTYPE_10 = round(queryRes[0][5] or 0,2)
    A_CH_V_OPPTYPE_10 = round(queryRes[0][6] or 0,2)
    A_SH_V_OPPTYPE_10 = round(queryRes[0][7] or 0,2)
    A_SHT_V_OPPTYPE_10 = round(queryRes[0][8] or 0,2)
    A_OPP_SH_V_OPPTYPE_10 = round(queryRes[0][9] or 0,2)
    A_OPP_SHT_V_OPPTYPE_10 = round(queryRes[0][10] or 0,2)
    A_DEEP_V_OPPTYPE_10 = round(queryRes[0][11] or 0,2)
    A_PPDA_V_OPPTYPE_10 = round(queryRes[0][12] or 0,2)
    
    
    """AWAY LAST 5 AWAY VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/5.00,SUM(XPTS)/5.00,SUM(GOALS)/5.00,SUM(XG)/5.00,SUM(OPP_GOALS)/5.00,SUM(OPP_XG)/5.00," \
                    +"SUM(CHANCES)/5.00,SUM(SHOTS)/5.00,SUM(ShOTS_TARGET)/5.00,SUM(OPP_SHOTS)/5.00,SUM(OPP_SHOTS_TARGET)/5.00"  \
                    +" FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(AWAY_TEAM) \
                    +"' AND HOME_AWAY = 'AWAY' ORDER BY EVENT_DATE DESC LIMIT 5)"
    queryRes = c.execute(queryString).fetchall()
    
    A_PTS_AWAY_5 = round(queryRes[0][0] or 0,2)
    A_XPTS_AWAY_5 = round(queryRes[0][1] or 0,2)
    A_G_AWAY_5 = round(queryRes[0][2] or 0,2)
    A_XG_AWAY_5 = round(queryRes[0][3] or 0,2)
    A_OPP_G_AWAY_5 = round(queryRes[0][4] or 0,2)
    A_OPP_XG_AWAY_5 = round(queryRes[0][5] or 0,2)
    A_CH_AWAY_5 = round(queryRes[0][6] or 0,2)
    A_SH_AWAY_5 = round(queryRes[0][7] or 0,2)
    A_SHT_AWAY_5 = round(queryRes[0][8] or 0,2)
    A_OPP_SH_AWAY_5 = round(queryRes[0][9] or 0,2)
    A_OPP_SHT_AWAY_5 = round(queryRes[0][10] or 0,2)
    
    
    """AWAY LAST 10 AWAY VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/10.00,SUM(XPTS)/10.00,SUM(GOALS)/10.00,SUM(XG)/10.00,SUM(OPP_GOALS)/10.00,SUM(OPP_XG)/10.00," \
                    +"SUM(CHANCES)/10.00,SUM(SHOTS)/10.00,SUM(ShOTS_TARGET)/10.00,SUM(OPP_SHOTS)/10.00,SUM(OPP_SHOTS_TARGET)/10.00," \
                    +"SUM(DEEP)/10.00,SUM(PPDA)/10.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(AWAY_TEAM) \
                    +"' AND HOME_AWAY = 'AWAY' ORDER BY EVENT_DATE DESC LIMIT 10)"
    queryRes = c.execute(queryString).fetchall()
    
    A_PTS_AWAY_10 = round(queryRes[0][0] or 0,2)
    A_XPTS_AWAY_10 = round(queryRes[0][1] or 0,2)
    A_G_AWAY_10 = round(queryRes[0][2] or 0,2)
    A_XG_AWAY_10 = round(queryRes[0][3] or 0,2)
    A_OPP_G_AWAY_10 = round(queryRes[0][4] or 0,2)
    A_OPP_XG_AWAY_10 = round(queryRes[0][5] or 0,2)
    A_CH_AWAY_10 = round(queryRes[0][6] or 0,2)
    A_SH_AWAY_10 = round(queryRes[0][7] or 0,2)
    A_SHT_AWAY_10 = round(queryRes[0][8] or 0,2)
    A_OPP_SH_AWAY_10 = round(queryRes[0][9] or 0,2)
    A_OPP_SHT_AWAY_10 = round(queryRes[0][10] or 0,2)
    A_DEEP_AWAY_10 = round(queryRes[0][11] or 0,2)
    A_PPDA_AWAY_10 = round(queryRes[0][12] or 0,2)

    
    """AWAY LAST 20 AWAY VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/20.00,SUM(XPTS)/20.00,SUM(GOALS)/20.00,SUM(XG)/20.00,SUM(OPP_GOALS)/20.00,SUM(OPP_XG)/20.00," \
                    +"SUM(CHANCES)/20.00,SUM(SHOTS)/20.00,SUM(ShOTS_TARGET)/20.00,SUM(OPP_SHOTS)/20.00,SUM(OPP_SHOTS_TARGET)/20.00" \
                    +" FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(AWAY_TEAM) \
                    +"' AND HOME_AWAY = 'AWAY' ORDER BY EVENT_DATE DESC LIMIT 10)"
    queryRes = c.execute(queryString).fetchall()
    
    A_PTS_AWAY_20 = round(queryRes[0][0] or 0,2)
    A_XPTS_AWAY_20 = round(queryRes[0][1] or 0,2)
    A_G_AWAY_20 = round(queryRes[0][2] or 0,2)
    A_XG_AWAY_20 = round(queryRes[0][3] or 0,2)
    A_OPP_G_AWAY_20 = round(queryRes[0][4] or 0,2)
    A_OPP_XG_AWAY_20 = round(queryRes[0][5] or 0,2)
    A_CH_AWAY_20 = round(queryRes[0][6] or 0,2)
    A_SH_AWAY_20 = round(queryRes[0][7] or 0,2)
    A_SHT_AWAY_20 = round(queryRes[0][8] or 0,2)
    A_OPP_SH_AWAY_20 = round(queryRes[0][9] or 0,2)
    A_OPP_SHT_AWAY_20 = round(queryRes[0][10] or 0,2)


    """AWAY LAST 5 VS OPPTYPE VARIABLES""" #DONE
    
    queryString = "SELECT SUM(POINTS)/5.00,SUM(XPTS)/5.00,SUM(GOALS)/5.00,SUM(XG)/5.00,SUM(OPP_GOALS)/5.00,SUM(OPP_XG)/5.00," \
                    +"SUM(CHANCES)/5.00,SUM(SHOTS)/5.00,SUM(ShOTS_TARGET)/5.00,SUM(OPP_SHOTS)/5.00,SUM(OPP_SHOTS_TARGET)/5.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE JOIN TEAMS ON OPPONENT = UNDERSTAT " \
                    +"WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(AWAY_TEAM)+"' AND BIG_SIX = "+str(HOME_BIG_SIX) \
                    +" AND HOME_AWAY = 'AWAY' ORDER BY EVENT_DATE DESC LIMIT 5)"
    queryRes = c.execute(queryString).fetchall()
    
    A_PTS_AWAY_V_OPPTYPE_5 = round(queryRes[0][0] or 0,2)
    A_XPTS_AWAY_V_OPPTYPE_5 = round(queryRes[0][1] or 0,2)
    A_G_AWAY_V_OPPTYPE_5 = round(queryRes[0][2] or 0,2)
    A_XG_AWAY_V_OPPTYPE_5 = round(queryRes[0][3] or 0,2)
    A_OPP_G_AWAY_V_OPPTYPE_5 = round(queryRes[0][4] or 0,2)
    A_OPP_XG_AWAY_V_OPPTYPE_5 = round(queryRes[0][5] or 0,2)
    A_CH_AWAY_V_OPPTYPE_5 = round(queryRes[0][6] or 0,2)
    A_SH_AWAY_V_OPPTYPE_5 = round(queryRes[0][7] or 0,2)
    A_SHT_AWAY_V_OPPTYPE_5 = round(queryRes[0][8] or 0,2)
    A_OPP_SH_AWAY_V_OPPTYPE_5 = round(queryRes[0][9] or 0,2)
    A_OPP_SHT_AWAY_V_OPPTYPE_5 = round(queryRes[0][10] or 0,2)
    
    
    """AWAY LAST 10 VS OPPTYPE VARIABLES"""
    
    queryString = "SELECT SUM(POINTS)/10.00,SUM(XPTS)/10.00,SUM(GOALS)/10.00,SUM(XG)/10.00,SUM(OPP_GOALS)/10.00,SUM(OPP_XG)/10.00," \
                    +"SUM(CHANCES)/10.00,SUM(SHOTS)/10.00,SUM(ShOTS_TARGET)/10.00,SUM(OPP_SHOTS)/10.00,SUM(OPP_SHOTS_TARGET)/10.00," \
                    +"SUM(DEEP)/10.00,SUM(PPDA)/10.00 " \
                    +"FROM (SELECT * FROM STAT_ARCHIVE JOIN TEAMS ON OPPONENT = UNDERSTAT " \
                    +"WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(AWAY_TEAM)+"' AND BIG_SIX = "+str(HOME_BIG_SIX) \
                    +" AND HOME_AWAY = 'AWAY' ORDER BY EVENT_DATE DESC LIMIT 10)"
    queryRes = c.execute(queryString).fetchall()
    
    A_PTS_AWAY_V_OPPTYPE_10 = round(queryRes[0][0] or 0,2)
    A_XPTS_AWAY_V_OPPTYPE_10 = round(queryRes[0][1] or 0,2)
    A_G_AWAY_V_OPPTYPE_10 = round(queryRes[0][2] or 0,2)
    A_XG_AWAY_V_OPPTYPE_10 = round(queryRes[0][3] or 0,2)
    A_OPP_G_AWAY_V_OPPTYPE_10 = round(queryRes[0][4] or 0,2)
    A_OPP_XG_AWAY_V_OPPTYPE_10 = round(queryRes[0][5] or 0,2)
    A_CH_AWAY_V_OPPTYPE_10 = round(queryRes[0][6] or 0,2)
    A_SH_AWAY_V_OPPTYPE_10 = round(queryRes[0][7] or 0,2)
    A_SHT_AWAY_V_OPPTYPE_10 = round(queryRes[0][8] or 0,2)
    A_OPP_SH_AWAY_V_OPPTYPE_10 = round(queryRes[0][9] or 0,2)
    A_OPP_SHT_AWAY_V_OPPTYPE_10 = round(queryRes[0][10] or 0,2)
    A_DEEP_AWAY_V_OPPTYPE_10 = round(queryRes[0][11] or 0,2)
    A_PPDA_AWAY_V_OPPTYPE_10 = round(queryRes[0][12] or 0,2)
    
    
    
    
    """INSERT STATEMENTS"""
    
    #MATCH TABLE
    matchInsert = "INSERT INTO MATCH (URL_ID,EVENT_DATE,HOME_TEAM,AWAY_TEAM,HOME_BIG_SIX,AWAY_BIG_SIX,LEAGUE)" + \
                       "VALUES ("+str(URL_ID)+",'"+str(EVENT_DATE)+"','"+str(HOME_TEAM)+"','"+str(AWAY_TEAM)+"'" \
                       +","+str(HOME_BIG_SIX)+","+str(AWAY_BIG_SIX)+",'"+str(LEAGUE)+"')"
    c.execute(matchInsert)
    
    
    #POINTS TABLE
    pointsInsert = "INSERT INTO POINTS VALUES("+str(URL_ID)+","+str(H_PTS_5)+","+str(H_PTS_10)+","+str(H_PTS_20)+"," \
                    +str(H_PTS_V_OPPTYPE_5)+","+str(H_PTS_V_OPPTYPE_10)+","+str(H_PTS_HOME_5)+","+str(H_PTS_HOME_10)+"," \
                    +str(H_PTS_HOME_20)+","+str(H_PTS_HOME_V_OPPTYPE_5)+","+str(H_PTS_HOME_V_OPPTYPE_10)+","+str(H_XPTS_5)+"," \
                    +str(H_XPTS_10)+","+str(H_XPTS_20)+","+str(H_XPTS_V_OPPTYPE_5)+","+str(H_XPTS_V_OPPTYPE_10)+"," \
                    +str(H_XPTS_HOME_5)+","+str(H_XPTS_HOME_10)+","+str(H_XPTS_HOME_20)+","+str(H_XPTS_HOME_V_OPPTYPE_5)+"," \
                    +str(H_XPTS_HOME_V_OPPTYPE_10)+","+str(A_PTS_5)+","+str(A_PTS_10)+","+str(A_PTS_20)+","+str(A_PTS_V_OPPTYPE_5)+"," \
                    +str(A_PTS_V_OPPTYPE_10)+","+str(A_PTS_AWAY_5)+","+str(A_PTS_AWAY_10)+","+str(A_PTS_AWAY_20)+"," \
                    +str(A_PTS_AWAY_V_OPPTYPE_5)+","+str(A_PTS_AWAY_V_OPPTYPE_10)+","+str(A_XPTS_5)+","+str(A_XPTS_10)+"," \
                    +str(A_XPTS_20)+","+str(A_XPTS_V_OPPTYPE_5)+","+str(A_XPTS_V_OPPTYPE_10)+","+str(A_XPTS_AWAY_5)+"," \
                    +str(A_XPTS_AWAY_10)+","+str(A_XPTS_AWAY_20)+","+str(A_XPTS_AWAY_V_OPPTYPE_5)+","+str(A_XPTS_AWAY_V_OPPTYPE_10)+")"
    c.execute(pointsInsert)
    
    
    #GOALS TABLE
    goalsInsert = "INSERT INTO GOALS VALUES("+str(URL_ID)+","+str(H_G_5)+","+str(H_G_10)+","+str(H_G_20)+","+str(H_G_V_OPPTYPE_5)+"," \
                    +str(H_G_V_OPPTYPE_10)+","+str(H_G_HOME_5)+","+str(H_G_HOME_10)+","+str(H_G_HOME_20)+"," \
                    +str(H_G_HOME_V_OPPTYPE_5)+","+str(H_G_HOME_V_OPPTYPE_10)+","+str(H_XG_5)+","+str(H_XG_10)+","+str(H_XG_20)+"," \
                    +str(H_XG_V_OPPTYPE_5)+","+str(H_XG_V_OPPTYPE_10)+","+str(H_XG_HOME_5)+","+str(H_XG_HOME_10)+"," \
                    +str(H_XG_HOME_20)+","+str(H_XG_HOME_V_OPPTYPE_5)+","+str(H_XG_HOME_V_OPPTYPE_10)+","+str(A_G_5)+"," \
                    +str(A_G_10)+","+str(A_G_20)+","+str(A_G_V_OPPTYPE_5)+","+str(A_G_V_OPPTYPE_10)+","+str(A_G_AWAY_5)+"," \
                    +str(A_G_AWAY_10)+","+str(A_G_AWAY_20)+","+str(A_G_AWAY_V_OPPTYPE_5)+","+str(A_G_AWAY_V_OPPTYPE_10)+"," \
                    +str(A_XG_5)+","+str(A_XG_10)+","+str(A_XG_20)+","+str(A_XG_V_OPPTYPE_5)+","+str(A_XG_V_OPPTYPE_10)+"," \
                    +str(A_XG_AWAY_5)+","+str(A_XG_AWAY_10)+","+str(A_XG_AWAY_20)+","+str(A_XG_AWAY_V_OPPTYPE_5)+"," \
                    +str(A_XG_AWAY_V_OPPTYPE_10)+")"
    c.execute(goalsInsert)
    
    
    #OPP_GOALS TABLE
    oppGoalsInsert = "INSERT INTO OPP_GOALS VALUES("+str(URL_ID)+","+str(H_OPP_G_5)+","+str(H_OPP_G_10)+","+str(H_OPP_G_20)+"," \
                    +str(H_OPP_G_V_OPPTYPE_5)+","+str(H_OPP_G_V_OPPTYPE_10)+","+str(H_OPP_G_HOME_5)+","+str(H_OPP_G_HOME_10)+"," \
                    +str(H_OPP_G_HOME_20)+","+str(H_OPP_G_HOME_V_OPPTYPE_5)+","+str(H_OPP_G_HOME_V_OPPTYPE_10)+"," \
                    +str(H_OPP_XG_5)+","+str(H_OPP_XG_10)+","+str(H_OPP_XG_20)+","+str(H_OPP_XG_V_OPPTYPE_5)+"," \
                    +str(H_OPP_XG_V_OPPTYPE_10)+","+str(H_OPP_XG_HOME_5)+","+str(H_OPP_XG_HOME_10)+","+str(H_OPP_XG_HOME_20)+"," \
                    +str(H_OPP_XG_HOME_V_OPPTYPE_5)+","+str(H_OPP_XG_HOME_V_OPPTYPE_10)+","+str(A_OPP_G_5)+","+str(A_OPP_G_10)+"," \
                    +str(A_OPP_G_20)+","+str(A_OPP_G_V_OPPTYPE_5)+","+str(A_OPP_G_V_OPPTYPE_10)+","+str(A_OPP_G_AWAY_5)+"," \
                    +str(A_OPP_G_AWAY_10)+","+str(A_OPP_G_AWAY_20)+","+str(A_OPP_G_AWAY_V_OPPTYPE_5)+"," \
                    +str(A_OPP_G_AWAY_V_OPPTYPE_10)+","+str(A_OPP_XG_5)+","+str(A_OPP_XG_10)+","+str(A_OPP_XG_20)+"," \
                    +str(A_OPP_XG_V_OPPTYPE_5)+","+str(A_OPP_XG_V_OPPTYPE_10)+","+str(A_OPP_XG_AWAY_5)+","+str(A_OPP_XG_AWAY_10)+"," \
                    +str(A_OPP_XG_AWAY_20)+","+str(A_OPP_XG_AWAY_V_OPPTYPE_5)+","+str(A_OPP_XG_AWAY_V_OPPTYPE_10)+")"
    c.execute(oppGoalsInsert)
    
    
    #CHANCES TABLE
    chancesInsert = "INSERT INTO CHANCES VALUES("+str(URL_ID)+","+str(H_CH_5)+","+str(H_CH_10)+","+str(H_CH_V_OPPTYPE_5)+"," \
                    +str(H_CH_V_OPPTYPE_10)+","+str(H_CH_HOME_5)+","+str(H_CH_HOME_10)+","+str(H_CH_HOME_20)+"," \
                    +str(H_CH_HOME_V_OPPTYPE_5)+","+str(H_CH_HOME_V_OPPTYPE_10)+","+str(A_CH_5)+","+str(A_CH_10)+"," \
                    +str(A_CH_V_OPPTYPE_5)+","+str(A_CH_V_OPPTYPE_10)+","+str(A_CH_AWAY_5)+","+str(A_CH_AWAY_10)+"," \
                    +str(A_CH_AWAY_20)+","+str(A_CH_AWAY_V_OPPTYPE_5)+","+str(A_CH_AWAY_V_OPPTYPE_10)+")"
    c.execute(chancesInsert)
    
    
    #SHOTS TABLE
    shotsInsert = "INSERT INTO SHOTS VALUES("+str(URL_ID)+","+str(H_SH_5)+","+str(H_SH_10)+","+str(H_SH_V_OPPTYPE_5)+"," \
                    +str(H_SH_V_OPPTYPE_10)+","+str(H_SH_HOME_5)+","+str(H_SH_HOME_10)+","+str(H_SH_HOME_20)+"," \
                    +str(H_SH_HOME_V_OPPTYPE_5)+","+str(H_SH_HOME_V_OPPTYPE_10)+","+str(H_SHT_5)+","+str(H_SHT_10)+"," \
                    +str(H_SHT_V_OPPTYPE_5)+","+str(H_SHT_V_OPPTYPE_10)+","+str(H_SHT_HOME_5)+","+str(H_SHT_HOME_10)+"," \
                    +str(H_SHT_HOME_20)+","+str(H_SHT_HOME_V_OPPTYPE_5)+","+str(H_SHT_HOME_V_OPPTYPE_10)+","+str(A_SH_5)+"," \
                    +str(A_SH_10)+","+str(A_SH_V_OPPTYPE_5)+","+str(A_SH_V_OPPTYPE_10)+","+str(A_SH_AWAY_5)+"," \
                    +str(A_SH_AWAY_10)+","+str(A_SH_AWAY_20)+","+str(A_SH_AWAY_V_OPPTYPE_5)+","+str(A_SH_AWAY_V_OPPTYPE_10)+"," \
                    +str(A_SHT_5)+","+str(A_SHT_10)+","+str(A_SHT_V_OPPTYPE_5)+","+str(A_SHT_V_OPPTYPE_10)+","+str(A_SHT_AWAY_5)+"," \
                    +str(A_SHT_AWAY_10)+","+str(A_SHT_AWAY_20)+","+str(A_SHT_AWAY_V_OPPTYPE_5)+","+str(A_SHT_AWAY_V_OPPTYPE_10)+")"
    c.execute(shotsInsert)
    
    
    #OPP_SHOTS TABLE
    oppShotsInsert = "INSERT INTO OPP_SHOTS VALUES("+str(URL_ID)+","+str(H_OPP_SH_5)+","+str(H_OPP_SH_10)+"," \
                    +str(H_OPP_SH_V_OPPTYPE_5)+","+str(H_OPP_SH_V_OPPTYPE_10)+","+str(H_OPP_SH_HOME_5)+","+str(H_OPP_SH_HOME_10)+"," \
                    +str(H_OPP_SH_HOME_20)+","+str(H_OPP_SH_HOME_V_OPPTYPE_5)+","+str(H_OPP_SH_HOME_V_OPPTYPE_10)+"," \
                    +str(H_OPP_SHT_5)+","+str(H_OPP_SHT_10)+","+str(H_OPP_SHT_V_OPPTYPE_5)+","+str(H_OPP_SHT_V_OPPTYPE_10)+"," \
                    +str(H_OPP_SHT_HOME_5)+","+str(H_OPP_SHT_HOME_10)+","+str(H_OPP_SHT_HOME_20)+"," \
                    +str(H_OPP_SHT_HOME_V_OPPTYPE_5)+","+str(H_OPP_SHT_HOME_V_OPPTYPE_10)+","+str(A_OPP_SH_5)+"," \
                    +str(A_OPP_SH_10)+","+str(A_OPP_SH_V_OPPTYPE_5)+","+str(A_OPP_SH_V_OPPTYPE_10)+","+str(A_OPP_SH_AWAY_5)+"," \
                    +str(A_OPP_SH_AWAY_10)+","+str(A_OPP_SH_AWAY_20)+","+str(A_OPP_SH_AWAY_V_OPPTYPE_5)+"," \
                    +str(A_OPP_SH_AWAY_V_OPPTYPE_10)+","+str(A_OPP_SHT_5)+","+str(A_OPP_SHT_10)+","+str(A_OPP_SHT_V_OPPTYPE_5)+"," \
                    +str(A_OPP_SHT_V_OPPTYPE_10)+","+str(A_OPP_SHT_AWAY_5)+","+str(A_OPP_SHT_AWAY_10)+","+str(A_OPP_SHT_AWAY_20)+"," \
                    +str(A_OPP_SHT_AWAY_V_OPPTYPE_5)+","+str(A_OPP_SHT_AWAY_V_OPPTYPE_10)+")"
    c.execute(oppShotsInsert)
    
    
    #OTHER_STATS TABLE
    otherStatsInsert = "INSERT INTO OTHER_STATS VALUES("+str(URL_ID)+","+str(H_DEEP_5)+","+str(H_DEEP_10)+"," \
                    +str(H_DEEP_V_OPPTYPE_10)+","+str(H_DEEP_HOME_10)+","+str(H_PPDA_5)+","+str(H_PPDA_10)+"," \
                    +str(H_PPDA_V_OPPTYPE_10)+","+str(H_PPDA_HOME_10)+","+str(A_DEEP_5)+","+str(A_DEEP_10)+"," \
                    +str(A_DEEP_V_OPPTYPE_10)+","+str(A_DEEP_AWAY_10)+","+str(A_PPDA_5)+","+str(A_PPDA_10)+"," \
                    +str(A_PPDA_V_OPPTYPE_10)+","+str(A_PPDA_AWAY_10)+")"
    c.execute(otherStatsInsert)
    
    
    #close connection
    conn.commit()
    conn.close()
    
    print('Inserted values for match ' + str(URL_ID))
    
    
    
"""
Connor Buchanan
Predict.py
version 1.0 - 1/13/2021

Prediction process
"""


#import statements
import pandas as pd
import sqlite3
import pickle

#load previously created model
model1 = pickle.load(open('Global_NN_v1', 'rb'),encoding="latin1")
model2 = pickle.load(open('Global_LDA_v1', 'rb'),encoding="latin1")
model3 = pickle.load(open('Global_LR_v1', 'rb'),encoding="latin1")

#sql database connection
conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
c = conn.cursor()

#create query string to pull non completed game for predictions
queryString = "SELECT * FROM MATCH M JOIN POINTS P ON M.URL_ID=P.URL_ID JOIN GOALS G ON M.URL_ID=G.URL_ID JOIN OPP_GOALS OG " \
                +"ON M.URL_ID=OG.URL_ID JOIN CHANCES C ON M.URL_ID=C.URL_ID JOIN SHOTS S ON M.URL_ID=S.URL_ID JOIN OPP_SHOTS OP " \
                +"ON M.URL_ID=OP.URL_ID JOIN OTHER_STATS OS ON M.URL_ID=OS.URL_ID WHERE M.RESULT IS NULL"

#return dataframe and close connection
statDF = pd.read_sql_query(queryString,conn)
conn.close() 

#delete duplicated URL_ID columns
statDF = statDF.loc[:,~statDF.columns.duplicated()]



"""MODEL PREP AND SETUP"""

"""For Global_NN_v1"""
#split out valiation dataset
X = statDF.iloc[:,5:]
y = statDF['RESULT']

del X['LEAGUE']

#predict
predictions = model1.predict(X)
probPredict = model1.predict_proba(X)

#add results of model to dataframe
resultsDF = statDF[['URL_ID','EVENT_DATE','HOME_TEAM','AWAY_TEAM','RESULT']].copy()
resultsDF['Pred1'] = predictions
resultsDF['HOME_PROB1'],resultsDF['AWAY_PROB1'] = probPredict[:,1],probPredict[:,0]



"""for Global_LDA_v1"""
X = statDF.loc[:,['H_PTS_V_OPPTYPE_10', 'H_XPTS_10', 'H_XPTS_V_OPPTYPE_10', 'H_XPTS_HOME_V_OPPTYPE_5', 'H_XPTS_HOME_V_OPPTYPE_10', 'A_XPTS_20', 'A_XPTS_AWAY_V_OPPTYPE_5', 'A_XPTS_AWAY_V_OPPTYPE_10', 'H_XG_5', 'H_XG_V_OPPTYPE_5', 'H_XG_HOME_5', 'H_XG_HOME_V_OPPTYPE_5', 'H_XG_HOME_V_OPPTYPE_10', 'A_XG_V_OPPTYPE_10', 'A_XG_AWAY_10', 'A_XG_AWAY_V_OPPTYPE_10', 'H_OPP_XG_5', 'H_OPP_XG_HOME_5', 'H_OPP_XG_HOME_V_OPPTYPE_10', 'A_OPP_XG_20', 'A_OPP_XG_V_OPPTYPE_5', 'A_OPP_XG_AWAY_5', 'A_OPP_XG_AWAY_V_OPPTYPE_5', 'A_OPP_XG_AWAY_V_OPPTYPE_10', 'H_CH_10', 'H_CH_V_OPPTYPE_5', 'H_CH_V_OPPTYPE_10', 'H_CH_HOME_5', 'H_CH_HOME_10', 'H_CH_HOME_V_OPPTYPE_5', 'A_CH_V_OPPTYPE_5', 'A_CH_V_OPPTYPE_10', 'A_CH_AWAY_5', 'A_CH_AWAY_20', 'A_CH_AWAY_V_OPPTYPE_10', 'H_SH_V_OPPTYPE_10', 'H_SH_HOME_20', 'A_SH_5', 'A_SH_10', 'A_SH_AWAY_V_OPPTYPE_10', 'H_OPP_SH_V_OPPTYPE_5', 'H_OPP_SH_V_OPPTYPE_10', 'A_OPP_SH_V_OPPTYPE_10', 'A_OPP_SH_AWAY_10', 'H_DEEP_5', 'H_DEEP_V_OPPTYPE_10', 'H_PPDA_5', 'H_PPDA_V_OPPTYPE_10', 'H_PPDA_HOME_10', 'A_DEEP_V_OPPTYPE_10', 'A_PPDA_5', 'A_PPDA_V_OPPTYPE_10', 'A_PPDA_AWAY_10']]
y = statDF['RESULT']


#predict
predictions = model2.predict(X)
probPredict = model2.predict_proba(X)

#add results of model to dataframe
resultsDF['Pred2'] = predictions
resultsDF['HOME_PROB2'],resultsDF['AWAY_PROB2'] = probPredict[:,1],probPredict[:,0]


"""for Global_LR_v1"""
X = statDF.loc[:,['HOME_BIG_SIX'	,'AWAY_BIG_SIX'	,'H_PTS_5'	,'H_G_5'	,'H_OPP_G_5'	,'H_XPTS_5'	,'H_XG_5'	,'H_OPP_XG_5'	,'A_PTS_5'	,'A_G_5'	,'A_OPP_G_5'	,'A_XPTS_5'	,'A_XG_5'	,'A_OPP_XG_5'	,'H_DEEP_5'	,'H_PPDA_5'	,'A_DEEP_5'	,'A_PPDA_5'	,'H_SHT_5'	,'A_SHT_5']]
y = statDF['RESULT']


#predict
predictions = model3.predict(X)
probPredict = model3.predict_proba(X)

#add results of model to dataframe
resultsDF['Pred3'] = predictions
resultsDF['HOME_PROB3'],resultsDF['AWAY_PROB3'] = probPredict[:,1],probPredict[:,0]



#resultsDF.to_csv('Predictions.csv')




#insert predictions to database
for i in range(len(resultsDF)):
    conn = sqlite3.connect(r'C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
    c = conn.cursor()
    
    #variables for odds query
    EVENT_DATE = resultsDF['EVENT_DATE'][i]
    HOME_PROB1 = round(resultsDF['HOME_PROB1'][i],2)
    AWAY_PROB1 = round(resultsDF['AWAY_PROB1'][i],2)
    HOME_PROB2 = round(resultsDF['HOME_PROB2'][i],2)
    AWAY_PROB2 = round(resultsDF['AWAY_PROB2'][i],2)
    HOME_PROB3 = round(resultsDF['HOME_PROB3'][i],2)
    AWAY_PROB3 = round(resultsDF['AWAY_PROB3'][i],2)
    
    HOME_PROB = round((HOME_PROB1 + HOME_PROB2 + HOME_PROB3)/3,2)
    AWAY_PROB = round((AWAY_PROB1 + AWAY_PROB2 + AWAY_PROB3)/3,2)
    
    #queries for fandual name
    HOME = resultsDF['HOME_TEAM'][i]
    AWAY = resultsDF['AWAY_TEAM'][i]
    
    h = c.execute("SELECT FANDUEL FROM TEAMS WHERE UNDERSTAT = '"+str(HOME)+"'").fetchall()
    HOME_TEAM = h[0][0]
    a = c.execute("SELECT FANDUEL FROM TEAMS WHERE UNDERSTAT = '"+str(AWAY)+"'").fetchall()
    AWAY_TEAM = a[0][0]
    l = c.execute("SELECT LEAGUE FROM TEAMS WHERE UNDERSTAT = '"+str(HOME)+"'").fetchall()
    LEAGUE = l[0][0]
    
    """
    pred = resultsDF['Pred'][i]
    if pred == 'HOME':
        PREDICTION = 'HOME_WIN'
    elif pred == 'AWAY':
        PREDICTION = 'AWAY_WIN'
    """
    if HOME_PROB > AWAY_PROB:
        PREDICTION = 'HOME_WIN'
    elif AWAY_PROB > HOME_PROB:
        PREDICTION = 'AWAY_WIN'
        
    #query for odds of predictions value    
    queryString = "SELECT "+str(PREDICTION)+" FROM ODDS WHERE EVENT_DATE = '"+str(EVENT_DATE)+"' AND HOME_NAME = '"+str(HOME_TEAM) \
                    +"' AND AWAY_NAME = '"+str(AWAY_TEAM)+"'"
                    
    odds = c.execute(queryString).fetchall()
    TO_WIN = float(odds[0][0])
    
    maxID = c.execute("SELECT MAX(ID) FROM PREDICTIONS").fetchall()
    newID = int(maxID[0][0])+1
    
    """Bet recommendation"""
    if PREDICTION == 'HOME_WIN':
        prob = HOME_PROB
        ratio = HOME_PROB * TO_WIN
    elif PREDICTION == 'AWAY_WIN':
        prob = AWAY_PROB
        ratio = AWAY_PROB * TO_WIN
    
    if ratio > 0.85 and PREDICTION == 'HOME_WIN':
        BET = 'Y'
    elif ratio > 1 and PREDICTION == 'AWAY_WIN':
        BET = 'Y'
    elif HOME_PROB > 0.9 and TO_WIN > 0.5:
        BET = 'Y'
    elif prob > 0.7 and TO_WIN > 1.2:
        BET = 'Y'
    else:
        BET = 'N'
    
    #check if game has alredy been bet
    prevBet = c.execute("SELECT ID FROM PREDICTIONS WHERE EVENT_DATE = '"+str(EVENT_DATE)+"' AND HOME_TEAM = '"+str(HOME_TEAM) \
                   +"' AND AWAY_TEAM = '"+str(AWAY_TEAM)+"' AND BET_PLACED = 'Y'").fetchall()
    
    #if not already previously bet
    if not prevBet:
        #delete any previous predictions for match
        deleteString = ("DELETE FROM PREDICTIONS WHERE EVENT_DATE = '"+str(EVENT_DATE)+"' AND HOME_TEAM = '"+str(HOME_TEAM) \
                   +"' AND AWAY_TEAM = '"+str(AWAY_TEAM)+"'")
        c.execute(deleteString)
                    
        insertString = "INSERT INTO PREDICTIONS (ID,EVENT_DATE,HOME_TEAM,AWAY_TEAM,PREDICTION,HOME_PROB,AWAY_PROB,TO_WIN,BET,LEAGUE)" \
                        + " VALUES ("+str(newID)+",'"+str(EVENT_DATE)+"','"+str(HOME_TEAM)+"','"+str(AWAY_TEAM)+"','"+str(PREDICTION) \
                        +"',"+str(HOME_PROB)+","+str(AWAY_PROB)+","+str(TO_WIN)+",'"+str(BET)+"','"+str(LEAGUE)+"')"
    
        c.execute(insertString)
    
        print('Inserted ' + str(HOME_TEAM) + ' v ' + str(AWAY_TEAM))
    
        conn.commit()    
        conn.close()
