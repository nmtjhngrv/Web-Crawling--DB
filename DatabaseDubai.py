import sqlite3

class Database:

    __conn = None
    __dbname = "dubai.db"

    def __init__(self):
        self.connect()

    def connect(self):
        if not self.__conn:
            self.__conn = sqlite3.connect(self.__dbname)

    def close(self):

        if self.__conn:
            self.__conn.commit()
            self.__conn.close();
       

    def create_tables(self):
           
        cursor = self.__conn.cursor() 

        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS LISTINGS
                        (ID INTEGER PRIMARY KEY,
                        NAME TEXT NOT NULL,
                        URL TEXT NOT NULL,
                        LOCATION TEXT NOT NULL);
                    """)

        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS PRICES 
                        (ID INTEGER PRIMARY KEY,
                        LISTING_ID ID NOT NULL,
                        PRICE INT NOT NULL,
                        LAST_UPDATE_DATE TEXT
                        );
                    """)

        cursor.close()

    def get_listing_by_url(self, url):

        cursor = self.__conn.cursor()
        print(url)        
        cursor.execute("SELECT ID, NAME, URL, LOCATION FROM LISTINGS WHERE URL = '" + url + "'")
    
        data = cursor.fetchone()

        cursor.close()

        return data


    def get_listings(self):
        cursor = self.__conn.cursor()

        cursor.execute("SELECT ID, NAME, URL, LOCATION FROM LISTINGS") 
        
        data = cursor.fetchall()

        cursor.close()
        
        return data
    
    def add_listing(self, name, url, location):
        
        cursor = self.__conn.cursor()
        cursor.execute("INSERT INTO LISTINGS(NAME, URL, LOCATION) VALUES(?, ?, ?)", (name, str(url), location))


        listing_id = cursor.lastrowid

        cursor.close()

        return listing_id

    def get_price(self, listing_id):
        cursor = self.__conn.cursor()

        cursor.execute("SELECT * FROM PRICES WHERE LISTING_ID = {}".format(listing_id))

        data = cursor.fetchall()

        cursor.close()

        return data

    def add_price(self, listing_id, price):
        
        cursor = self.__conn.cursor()

        cursor.execute("""
                INSERT INTO PRICES(LISTING_ID, PRICE, LAST_UPDATE_DATE)
                VALUES({}, {}, datetime('now'))
                            """.format(listing_id, price))

        cursor.close()
