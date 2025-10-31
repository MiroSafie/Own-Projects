def MetarCategoryFunction(RawData):
    import re
    metar=RawData[0].split()

    #The category fucntion only reads through METAR -> QNH
    while True:
        if metar[len(metar)-1][0] != "Q":
            metar.pop()
        if metar[len(metar)-1][0] == "Q":
            break

    BASE={
        "METAR":"METAR",
        "LOCATION":"",
        "TIMESTAMP":"",
        "AUTO":False,
        "WIND":"",
        "WIND_VARIABILITY":None,
        "CAVOK":False,
        "VISIBILITY":None,
        "WEATHER":None,
        "CLOUD":None,
        "TempDew":None,
        "QNH":"",
        "RAIN":False,
        "MajorWx":True,
    }


    #METAR is automatic

    #LOCATION
    BASE["LOCATION"]=metar[1]
    #TIMESTAMP
    BASE["TIMESTAMP"]=metar[2]


    for i in metar:
        #AUTO
        if i.find("AUTO")==0:
            BASE["AUTO"]=True
        #WIND
        if i.find("KT")==5:
            BASE["WIND"]=i
        #WINDVAR
        if i.find("V")==3:
            BASE["WIND_VARIABILITY"]=i
        #CAVOK
        if i.find("CAVOK")==0:
            BASE["CAVOK"]=True
        #VISIBILITY
        if len(i)==4:
            if i[3]=="0":
                BASE["VISIBILITY"]=i
            if i[3]=="9":
                BASE["VISIBILITY"]=i
        #WEATHER
        if len(i)<=3:
            BASE["WEATHER"]=i
        if len(i)==5:
            if i.find("-")==0:
                BASE["WEATHER"]=i
            if i.find("+")==0:
                BASE["WEATHER"]=i
        if len(i)==4:
            if i[0]!="E":
                if i[3]!="0":
                    if i[3]!="9":
                        BASE["WEATHER"]=i
        
        #CLOUD only the lowest cloud level
        if re.search(("(FEW)|(SCT)|(BKN)|(OVC)|(NSC)|(NCD)"),i) != None and BASE["CLOUD"]==None:
            BASE["CLOUD"]=i
        #TEMP / DEW
        if len(i)>3:
            if i[2]=="/":
                BASE["TempDew"]=i
        #QNH
        if i.find("Q")==0:
            BASE["QNH"]=i

    #RAIN
    if BASE["WEATHER"]!=None:
        if re.search(("(DZ)|(GR)|(GS)|(PL)|(RA)|(SG)|(SN)"), BASE["WEATHER"]) !=None:
            BASE["RAIN"]=True

    #MAJOR WEATHER
    if BASE["WEATHER"]==None:
        BASE["MajorWx"]=False
    if BASE["WEATHER"]!=None:
        if BASE["WEATHER"].find("DZ")==len(BASE["WEATHER"])-2:
            BASE["MajorWx"]=False
    #No other major weather phenomena except high cloudcoverage
    if re.search(("(BKN)|(OVC)"), RawData[0]) !=None:
        if BASE["CLOUD"][3]=="0":
            if BASE["CLOUD"][4]<="2":
                BASE["MajorWx"]=True
    #Cumulonimbus /  Towering cumulus
    if re.search(("(CB)| (TCU)"), RawData[0]) !=None:
        BASE["MajorWx"]=True
    
    #Categorized data into a list
    INPUT=[]
    for i in BASE:
        INPUT.append(BASE[i])
    MySQLConnection_CategorizedData(INPUT)
    


def MySQLConnection_CategorizedData(INPUT):
    from mysql.connector import (connection)

    #Connects to the database
    cnx=connection.MySQLConnection(user='root', password='****',
                                host='127.0.0.1',database='metar')
    cursor=cnx.cursor()

    #Inserts the data into the database
    add_metar = ("INSERT INTO CATEGORICALDATA "
                "(METAR,LOCATION,TIMESTAMP,AUTO,WIND,WIND_VARIABILITY,CAVOK,VISIBILITY,WEATHER,CLOUD,TempDew,QNH,RAIN,MajorWx)"
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

    #Closes the connection to the database
    cursor.execute(add_metar,INPUT)
    cnx.commit()
    cursor.close()
    cnx.close()
