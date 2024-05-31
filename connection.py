from sqlalchemy import create_engine, text
import psycopg2
# from env import username, password, db_name, host, port

conn = psycopg2.connect(host="37.18.110.244", port=5432, database="helpDesk", user="st3", password="/XjHt(~_+iiRLKPgZvFA;q%5$WhCfW" )
cursor = conn.cursor()
cursor.execute("SELECT * FROM application")
users = cursor.fetchall()
for a in users:
    print(a)


#class BD:
    #def ss(self):
        #cursor.execute("""SELECT * FROM application""")
        #rows = cursor.fetchall()
        #texta = "\n\n".join([', '.join(map(str, row)) for row in rows])
        #return(texta)

conn.close
#engine = create_engine('postgresql://st3:/XjHt(~_+iiRLKPgZvFA;q%5$WhCfW@37.18.110.244:5432/helpDesk')

#connections = engine.connect()
#connections.close()
