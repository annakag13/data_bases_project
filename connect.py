import sqlite3

def readSQL(dbfilename, sql, data = None): 
   #print("sql", sql, data)
   db = sqlite3.connect(dbfilename)
   cur = db.cursor()
   if data == None:
      cur.execute(sql)
   else:
      cur.execute(sql, data)
   result = cur.fetchall()
   db.close()
   return result   

def writeSQL(dbfilename, sql, data = None): 
   # print('write', sql, data)
   db = sqlite3.connect(dbfilename)
   cur = db.cursor()
   if data == None:
      cur.execute(sql)
   else:
      cur.execute(sql, data)
   # result = cur.fetchall()
   db.commit()
   db.close()
   # return result
   return 1


"""
database = 'benglish.db'
rows = readSQL(database, 'SELECT * FROM ARENA')

for row in rows:
   print(row)

rows = writeSQL(database, 'DROP TABLE TESTME')

writeSQL(database, '''
   CREATE TABLE IF NOT EXISTS "TESTME"(
      "id" INTEGER NOT NULL,
      "round" INTEGER NOT NULL DEFAULT '0' CHECK("round" BETWEEN 1 AND 30),
      "name" varchar(20) NOT NULL DEFAULT '',
      PRIMARY KEY("id")
   );
   ''')
#print(a)

## sql injection
# ex some value..X = '15, "ok"); INSERT INTO USERS (name, password) VALUES ("hacker","my53creTP44sw0rd") -- '

items = [
   ( 1, 12, 'hello' ),
   ( 2, 16, 'hello again' )
]
for x in range(0,2):
   print(items[x])
   b = writeSQL(database, '''
      INSERT INTO TESTME ("id", "round", "name")
         VALUES (?, ?, ?);
      ''', items[x])
   print(b)

xrows = readSQL(database, 'SELECT * FROM TESTME')
print('have some result', xrows)
for row in xrows:
   print(row)


"""