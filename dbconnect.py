import MySQLdb as db


HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = ""
DB = "biz"

class database():
    def __init__(self):
        try:
            self.connection = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
            self.dbhandler = self.connection.cursor()
        except:
            print("Unable to connect to database, check internet connection or contact admin")
            exit()



    def query_db(self, query):
        try:
            self.dbhandler.execute(query)
            result = self.dbhandler.fetchall()
            return result
        except:
            print("SQL query is fucked mate, contact admin")
            return None


    def commit_db(self, query):
        try:
            self.dbhandler.execute(query)
            self.connection.commit()
        except:
            print("SQL commit is fucked mate, contact admin")

def main():
    db = database()
    result = db.query_db("SELECT * FROM found_cars")
    for item in result:
        print(item)

if __name__ == "__main__":
	main()