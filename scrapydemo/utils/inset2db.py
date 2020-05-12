import psycopg2

from configdb import configdb

if __name__ == "__main__":

    import json

    # arr = json.loads("../patent.json")

    arr = []

    with open('../patent.json', 'r') as data_file:
        json_data = data_file.read()
        arr = json.loads(json_data)

    for entry in arr:


        #print(entry)
        if entry['id'] != "null" and (entry['Location'] != "null" or entry['Headquarters'] != "null"):

            """ update vendor name based on the vendor id """
            sql = """ UPDATE bd_patent2
                        SET mark = %s, mark2 = %s
                        WHERE idx = %s"""
            conn = None
            updated_rows = 0

            try:
                # read database configuration
                params = configdb()
                # connect to the PostgreSQL database
                conn = psycopg2.connect(**params)
                # create a new cursor
                cur = conn.cursor()
                # execute the UPDATE  statement
                cur.execute(sql, (str(entry['Location']), str(entry['Headquarters']), entry['id']))
                print("successfully update 1 row")
                # get the number of updated rows
                updated_rows = cur.rowcount
                # Commit the changes to the database
                conn.commit()
                # Close communication with the PostgreSQL database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
