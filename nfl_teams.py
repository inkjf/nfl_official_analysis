# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 02:09:12 2022

@author: kujoh
"""

# Teams = {"League": {"primary": "mediumblue", "secondary" : "whitesmoke", "edge": "red"},
#                    # AFC West
#          "Kansas City Chiefs" : {"primary" : "#E31837", "secondary" : "#FFB81C"},
#          "Los Angeles Chargers"  : {"primary" : "#0080C6", "secondary" : "#FFC20E"},
#          "Denver Broncos" : {"primary" : "#FB4F14", "secondary" : "#002244"},
#          "Las Vegas Raiders" : {"primary" : "#A5ACAF", "secondary" : "black"},
#          "Oakland Raiders" : {"primary" : "darkgrey", "secondary" : "black"},
#          # AFC East
#          "Buffalo Bills" : {"primary" : "#00338D", "secondary" : "#C60C30"},
#          "Miami Dolphins" : {"primary" : "#008E97", "secondary" : "#FC4C02"},
#          "New York Jets" : {"primary" : "#125740", "secondary" : "black"},
#          "New England Patriots" : {"primary" : "#C60C30", "secondary" : "#002244"},
#          # AFC North
#          "Cincinnati Bengals" : {"primary" : "#FB4F14", "secondary" : "black"},
#          "Baltimore Ravens" : {"primary" : "#241773", "secondary" : "#9E7C0C"},
#          "Cleveland Browns" : {"primary" : "#FF3C00", "secondary" : "#311D00"},
#          "Pittsburgh Steelers" : {"primary" : "#FFB612", "secondary" : "#101820"},
#          # AFC South
#          "Tennessee Titans" : {"primary" : "#0C2340", "secondary" : "#4B92DB"},
#          "Jacksonville Jaguars" : {"primary" : "#006778", "secondary" : "#9F792C"},
#          "Indianapolis Colts" : {"primary" : "#002C5F", "secondary" : "whitesmoke"},
#          "Houston Texans" : {"primary" : "#03202F", "secondary" : "#A71930"},
#          # NFC West
#          "San Francisco 49ers" : {"primary" : "#AA0000", "secondary" : "#B3995D"},
#          "Seattle Seahawks" : {"primary" : "#002244", "secondary" : "#69BE28"},
#          "Arizona Cardinals" : {"primary" : "#97233F", "secondary" : "#FFB612"},
#          "Los Angeles Rams" : {"primary" : "#003594", "secondary" : "#FFA300"},
#          # NFC East
#          "Philadelphia Eagles" : {"primary" : "#004C54", "secondary" : "#A5ACAF"},
#          "Dallas Cowboys" : {"primary" : "#869397", "secondary" : "#041E42"},
#          "New York Giants" : {"primary" : "#A71930", "secondary" : "#0B2265"},
#          "Washington Redskins" : {"primary" : "#5A1414", "secondary" : "#FFB612"},
#          # NFC West
#          "Minnesota Vikings"  : {"primary" : "#4F2683", "secondary" : "#FFC62F"},
#          "Detroit Lions"  : {"primary" : "#0076B6", "secondary" : "#B0B7BC"},
#          "Green Bay Packers"  : {"primary" : "#203731", "secondary" : "#FFB612"},
#          "Chicago Bears"  : {"primary" : "#0B162A", "secondary" : "#C83803"},
#          # NFC South
#          "Tampa Bay Buccaneers"  : {"primary" : "#D50A0A", "secondary" : "#FF7900"},
#          "Carolina Panthers"  : {"primary" : "#0085CA", "secondary" : "#101820"},
#          "New Orleans Saints"  : {"primary" : "#D3BC8D", "secondary" : "#101820"},
#          "Atlanta Falcons"  : {"primary" : "#A71930", "secondary" : "black"},
#          }

Teams = {"League": {0: "mediumblue", 1 : "mediumblue", "edge": "red"},
         # AFC West
         "Kansas City Chiefs" : {0 : "#E31837", 1 : "#FFB81C"},
         "Los Angeles Chargers"  : {0 : "#0080C6", 1 : "#FFC20E"},
         "Denver Broncos" : {0 : "#FB4F14", 1 : "#002244"},
         "Las Vegas Raiders" : {0 : "#A5ACAF", 1 : "black"},
         "Oakland Raiders" : {0 : "darkgrey", 1 : "black"},
         # AFC East
         "Buffalo Bills" : {0 : "#00338D", 1 : "#C60C30"},
         "Miami Dolphins" : {0 : "#008E97", 1 : "#FC4C02"},
         "New York Jets" : {0 : "#125740", 1 : "black"},
         "New England Patriots" : {0 : "#C60C30", 1 : "#002244"},
         # AFC North
         "Cincinnati Bengals" : {0 : "#FB4F14", 1 : "black"},
         "Baltimore Ravens" : {0 : "#241773", 1 : "#9E7C0C"},
         "Cleveland Browns" : {0 : "#FF3C00", 1 : "#311D00"},
         "Pittsburgh Steelers" : {0 : "#FFB612", 1 : "#101820"},
         # AFC South
         "Tennessee Titans" : {0 : "#0C2340", 1 : "#4B92DB"},
         "Jacksonville Jaguars" : {0 : "#006778", 1 : "#9F792C"},
         "Indianapolis Colts" : {0 : "#002C5F", 1 : "#A2AAAD"},
         "Houston Texans" : {0 : "#03202F", 1 : "#A71930"},
         # NFC West
         "San Francisco 49ers" : {0 : "#AA0000", 1 : "#B3995D"},
         "Seattle Seahawks" : {0 : "#002244", 1 : "#69BE28"},
         "Arizona Cardinals" : {0 : "#97233F", 1 : "#FFB612"},
         "Los Angeles Rams" : {0 : "#003594", 1 : "#FFA300"},
         # NFC East
         "Philadelphia Eagles" : {0 : "#004C54", 1 : "#A5ACAF"},
         "Dallas Cowboys" : {0 : "#869397", 1 : "#041E42"},
         "New York Giants" : {0 : "#A71930", 1 : "#0B2265"},
         "Washington Commanders" : {0 : "#5A1414", 1 : "#FFB612"},
         # NFC West
         "Minnesota Vikings"  : {0 : "#4F2683", 1 : "#FFC62F"},
         "Detroit Lions"  : {0 : "#0076B6", 1 : "#B0B7BC"},
         "Green Bay Packers"  : {0 : "#203731", 1 : "#FFB612"},
         "Chicago Bears"  : {0 : "#0B162A", 1 : "#C83803"},
         # NFC South
         "Tampa Bay Buccaneers"  : {0 : "#D50A0A", 1 : "#FF7900"},
         "Carolina Panthers"  : {0 : "#0085CA", 1 : "#101820"},
         "New Orleans Saints"  : {0 : "#D3BC8D", 1 : "#101820"},
         "Atlanta Falcons"  : {0 : "#A71930", 1 : "black"},
         }

