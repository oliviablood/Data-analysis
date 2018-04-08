import csv
import MySQLdb


mydb = MySQLdb.connect("127.0.0.1","root","yyicon21647","da_assignment1")
rowcount=0
print ('connected to data base')
cursor = mydb.cursor()

csv_data = csv.reader(file('Batting.csv'),quoting=csv.QUOTE_NONE)

print ('file opened')
for row in csv_data:
    #print rowcount
    print (row)
    if rowcount > 0:
        cursor.execute('INSERT INTO batting(battingid,playerID,yearID,temaID,games,atbats,runsScored,hits,homeruns,runsBattedln,walks,strikeOuts)' \
                                      'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            row)
    rowcount += 1
#commit all insert transactions here
mydb.commit()
#close the connection to the database.
cursor.close()
print ("Done")
