import psycopg2

conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="101077",
                        port="5432")

cur = conn.cursor()
datauser = "testing1", "passtesting1"
cur.execute("INSERT INTO datauser (username,password) VAlUES (%s,%s)",datauser)
conn.commit()

conn.close()