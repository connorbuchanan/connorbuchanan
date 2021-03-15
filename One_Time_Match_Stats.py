# -*- coding: utf-8 -*-
"""
Connor Buchanan
version 1.0 - 1/7/2021

One time process to populate Match_Stats table with historical stats and results

Intensive SQL queries to aggregate various stats over last 5, 10, away, home, big six, etc.

Will start in the 2016 season, 2015-2016 in database for reference and stat aggregation only
"""

#import statements
import sqlite3

#retrieve list of urls in database
conn = sqlite3.connect('C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()
urlList = c.execute("SELECT DISTINCT URL_ID FROM STAT_ARCHIVE WHERE EVENT_DATE > '2016-08-01' AND LEAGUE != 'EPL'").fetchall()
conn.close()

#for test only, remove code later
#urlList = [14149,15860]
 


#iterate through URLs to get each stat
for u in urlList:
    #create connection that will be used for all queries
    conn = sqlite3.connect('C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
    c = conn.cursor()

    """GLOBAL VARIABLES FOR QUERIES"""
    URL_ID = u
    
    #derive home and away team values for use in future queries
    teamString = "SELECT TEAM, OPPONENT, LEAGUE FROM STAT_ARCHIVE WHERE HOME_AWAY = 'HOME' AND URL_ID="+str(URL_ID)
    teams = c.execute(teamString).fetchall()
    HOME_TEAM = teams[0][0]
    AWAY_TEAM = teams[0][1]
    LEAGUE = teams[0][2]
    
    """MATCH TABLE VARIABLES"""
    matchString = "SELECT S.EVENT_DATE, T1.BIG_SIX AS HOME_BIG_SIX, T2.BIG_SIX AS AWAY_BIG_SIX, RESULT FROM STAT_ARCHIVE S " \
                          +"JOIN TEAMS T1 ON S.TEAM = T1.UNDERSTAT JOIN TEAMS T2 ON S.OPPONENT = T2.UNDERSTAT " \
                          +"WHERE S.HOME_AWAY = 'HOME' AND S.URL_ID = "+str(URL_ID)
    matchList = c.execute(matchString).fetchall()
    
    EVENT_DATE = matchList[0][0]
    
    #derive result from home returned value
    homeRes = matchList[0][3]
    if homeRes == 'W':
        RESULT = 'HOME'
    elif homeRes == 'L':
        RESULT = 'AWAY'
    elif homeRes == 'D':
        RESULT = 'DRAW'
        
    HOME_BIG_SIX = matchList[0][1]
    AWAY_BIG_SIX = matchList[0][2]
    
    
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
    matchInsert = "INSERT INTO MATCH VALUES ("+str(URL_ID)+",'"+str(EVENT_DATE)+"','"+str(HOME_TEAM)+"','"+str(AWAY_TEAM)+"','" \
                    +str(RESULT)+"',"+str(HOME_BIG_SIX)+","+str(AWAY_BIG_SIX)+",'"+str(LEAGUE)+"')"
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
    




"""TEST CODE FOR QUERIES"""
"""

conn = sqlite3.connect('C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
c = conn.cursor()

queryString = "SELECT SUM(POINTS)/5.00,SUM(XPTS)/5.00,SUM(GOALS)/5.00,SUM(XG)/5.00,SUM(OPP_GOALS)/5.00,SUM(OPP_XG)/5.00," \
                    +"SUM(CHANCES)/5.00,SUM(SHOTS)/5.00,SUM(ShOTS_TARGET)/5.00,SUM(OPP_SHOTS)/5.00,SUM(OPP_SHOTS_TARGET)/5.00"  \
                    +" FROM (SELECT * FROM STAT_ARCHIVE WHERE EVENT_DATE < '"+str(EVENT_DATE)+"' AND TEAM = '"+str(HOME_TEAM) \
                    +"' AND HOME_AWAY = 'HOME' ORDER BY EVENT_DATE DESC LIMIT 5)"
queryRes = c.execute(queryString).fetchall()


print(queryRes)

#to return a tupl. spec to get specific value in [row][item] format
#x = c.execute("SELECT * FROM STAT_ARCHIVE WHERE URL_ID=81 AND HOME_AWAY = 'HOME'").fetchall()
#spec = x[0][1] 

#to query to a dataframe
#df = pd.read_sql_query("SELECT * FROM STAT_ARCHIVE WHERE URL_ID=81 AND HOME_AWAY = 'HOME'",conn)

conn.close()
"""
