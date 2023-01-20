import sqlite3
import datetime


class MCW_Tables:

    def create_table(self):
        # create a connection to the database?
        #conn2 = sqlite3.connect((r'C:\Users\Admin\PycharmProjects\MCU_Actuarial_Tables\MCU.db')
        conn = sqlite3.connect('MCWho.db')  # if the given database does not exist, it will be created

        # create a cursor
        cur = conn.cursor()

        # create a table
        cur.executescript(
            """
            CREATE TABLE MCW_Actors
            (
                actor_id text,
                movie_id text,
                name text     
            );
            
            CREATE TABLE MCW_Movies
            (
                movie_id text,
                title text     
            );
            
            CREATE TABLE MCW_Selected_Actors
            (
                actor_id text    
            );
            
            CREATE TABLE MCW_Selected_Movies
            (
                movie_id text
            );
            """)

        # commit the commands
        conn.commit()

        # good practice to close DB connections explicitly
        conn.close()

    def insert_one(self, list):
        conn = sqlite3.connect('MCU.db')
        cur = conn.cursor()

        cur.execute("INSERT INTO Cast_Members VALUES(?,?,?,?,?,?,?,?)", (list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7]))

        conn.commit()
        conn.close()

    def remove_values(self):
        conn = sqlite3.connect('MCU.db')
        cur = conn.cursor()

        today = str(datetime.date.today())

        cur.execute("DELETE FROM Cast_Members WHERE birth_date = (?)",today)#remove those without a proper birth date

        conn.commit()
        conn.close()

    def show_all(self):
        conn = sqlite3.connect('MCU.db')
        cur = conn.cursor()

        cur.execute("SELECT rowid, * FROM Cast_Members")

        items = cur.fetchall()
        for item in items:
            print(item)

        conn.commit()
        conn.close()

    def delete_rows(self):
        import sqlite3

        conn = sqlite3.connect('MCU.db')
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM Cast_Members;
        """)

        conn.commit()
        conn.close()

    def export_to_csv(self):
        import sqlite3 as sql
        import os
        import csv
        from sqlite3 import Error
        try:

            # Connect to database
            conn = sql.connect('MCU.db')



            # Export data into CSV file

            cursor = conn.cursor()
            cursor.execute("select * from Cast_Members")

            with open("MCU_death_table.csv", "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow([i[0] for i in cursor.description])
                csv_writer.writerows(cursor)

            dirpath = os.getcwd() + "N:/Data Analysis/MCU/MCU_death_table.csv"
            print
            "Data exported Successfully into {}".format(dirpath)

        except Error as e:
            print(e)

        # Close database connection
        finally:
            conn.close()

    def create_movie_dictionary(self):
        movie_dict = {}


d = MCW_Tables()



d.show_all()
# d.delete_rows()
#d.export_to_csv()
