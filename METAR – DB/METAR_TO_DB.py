def MySQLConnection_RawData(METAR):
    from mysql.connector import connection

    #Connects to the database
    cnx=connection.MySQLConnection(user='root', password='****',
                                host='127.0.0.1',database='metar')
    cursor=cnx.cursor()

    #Inserts the data to the database
    add_metar = ("INSERT INTO Raw_data "
                "(raw_data)"
                "VALUES(%s)")

    #Closes the connection to the database
    cursor.execute(add_metar,METAR)
    cnx.commit()
    cursor.close()
    cnx.close()
