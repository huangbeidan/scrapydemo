import re
from urllib.request import urlopen

import psycopg2

from configdb import configdb


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    name_list = []
    try:
        # read connection parameters
        params = configdb()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute('select assigneeid, name from patentassignees where validurl is null;')

        # display the PostgreSQL database server version
        db_version = cur.fetchall()


        for row in db_version:
            id = row[0]
            name = row[1]
            name = name.replace(" ", "_")
            name = re.sub(r"\(.*\)", "", name)
            url = "https://en.wikipedia.org/wiki/" + name
            val_url = False
            try:

                code = urlopen(url).code
                if (code == 200):
                    print("connect success!")
                    print(url)
                    val_url = True
            except Exception as e:
                pass


            try:
                sql = """ UPDATE patentassignees
                            SET wikiurl = %s, validurl = %s
                            WHERE assigneeid = %s"""

                cur = conn.cursor()
                cur.execute(sql, (url, val_url, id))
                updated_rows = cur.rowcount
                print("successfully update rows: " + str(updated_rows))
                conn.commit()

            except Exception as e:
                print(e)
                print("update fails")


       # name_list = [tuple[0] for tuple in db_version]

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            return name_list


if __name__ == '__main__':
    connect()
