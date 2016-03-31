import psycopg2
#note that we have to import the Psycopg2 extras library!
import psycopg2.extras
import sys
 
def main():
    conn_string = "host='localhost' dbname='wifi' user='probecap' password='pass'"
    # print the connection string we will use to connect
    #print "Connecting to database\n ->%s" % (conn_string)
    try:
        conn = psycopg2.connect(conn_string)
     
        cursor = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT name,lat,long FROM ssid')
     
        resultList = []
        for data_out in cursor:
            resultList.append(data_out[0]) 
            
        outputquery = 'copy (SELECT name,lat,long FROM ssid LIMIT 5) to stdout with csv'.format(resultList)

        with open('resultsfile', 'w') as f:
            cursor.copy_expert(outputquery, f) 
                       
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)
    finally:
        if conn:
            conn.close()
        
    
 
if __name__ == "__main__":
    main()
    