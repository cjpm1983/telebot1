import sqlite3

def get_response(msg): 
     con = sqlite3.connect('/home/cjpm1983/telebot1/db/RVA.SQLite3')

     cur = con.cursor()
     salida="pi pi pi :)"

     if (msg.find('__')!=-1):
        #salida="cita"
        libro_cita = msg.split('_')
        libro = libro_cita[0]
        salida = libro
        
        cita = libro_cita[1]
        cap_v = cita.split('_')
        cap = cap_v[0]

        b=cur.execute('select * from books where short_name = :sn',{'sn':libro})
        bn = b.fetchone()[0]
        cur.execute('select * from verses where  book_number = :bn and chapter = :cap ',{'bn':bn,'cap':cap})
        versos = cur.fetchall()
        
        salida = versos[1][3]
       


     else: 

        search = str.replace(msg," ",'%')

        cur.execute('select * from verses where LOWER(text) like LOWER(:p1) ',{'p1':"%{}%".format(search)})

        r = cur.fetchall()

        if bool(r):
           for v in r:
               b=cur.execute('select * from books where book_number=:libro',{'libro':v[0]})     
               salida = "%s \n%s"%(salida,format(" - /%s__%s_%s - \n %s \n"%( b.fetchone()[2] , v[1] , v[2] , v[3] ) ) )
        else:
           salida="Sin resultados - No result /Apocalipsis_de_Juan__3_14"

     con.close  

     return salida


