import sqlite3

def get_response(msg): 
     con = sqlite3.connect('/home/cjpm1983/telebot1/db/RVA.SQLite3')

     cur = con.cursor()
     salida=""

    
     if (msg=="/start"):
                cur.execute('select short_name from books')
                r = cur.fetchall()
                libros = " "
                botones=[]
                #botones.append([])
                #subbotones.append([])
                i=0
                for l in r:
                    #print(l)
                    
                    #libros = libros + "/" + l[0] + "   "
                    
                    #libros como botones

                    if (i%6==0):
                       botones.append([])
                    botones[len(botones)-1].append({'text': l[0], 'callback_data': "/%s"%(l[0])})

                    #botones[0].append({'text': l[0], 'callback_data': 'Return value 1'})
                    #botones[1].append({'text': l[0], 'callback_data': 'Return value 1'})
                    i=i+1

                markup = {'inline_keyboard': botones}

                #markup = {'inline_keyboard': [[{'text': 'Gn', 'callback_data': 'Return value 1'},
                #         {'text': 'Mt', 'callback_data': 'Return value 2'}]]}

                bundle = {"txt":"------\nlibros\n------","btns":markup}
                return  bundle



      #No tiene  undescore
     if ( (msg.find('_')==-1) and (msg.find('/')!=-1) ):
            m = str.replace(msg,"/",'')

            b=cur.execute('select * from books where short_name=:libro',{'libro':m})
            t = b.fetchone()
            bn = t[1]
            bl = t[3]
        

            d = cur.execute('select max( chapter) from verses where book_number = :p1 ',{'p1':bn})
            cantidadCap=d.fetchone()[0]            
            capitulos = bl + "\n "
            #for i in range(1,int(cantidadCap)+1):
            #   capitulos = capitulos + "  /" + m + "_" + str(i)
            
            #return {"txt":capitulos}
            botonesc=[]
            #j=0
            for j in range(0,int(cantidadCap)):
                    #capitulos = capitulos + "  /" + m + "_" + str(i)
                
                    if (j%6==0):
                       botonesc.append([])
                    botonesc[len(botonesc)-1].append({'text': m + " " + str(j+1), 'callback_data': "/%s"%(m + "_" + str(j+1))})

                    #botones[0].append({'text': l[0], 'callback_data': 'Return value 1'})
                    #botones[1].append({'text': l[0], 'callback_data': 'Return value 1'})
                    j=j+1

            markup = {'inline_keyboard': botonesc}

                #markup = {'inline_keyboard': [[{'text': 'Gn', 'callback_data': 'Return value 1'},
                #         {'text': 'Mt', 'callback_data': 'Return value 2'}]]}

            bundle = {"txt":f"------\n{bl}\n------","btns":markup}
            return  bundle

     if ( (msg.find('_')!=-1) and (msg.find('/')!=-1) ):

        cita = str.replace(msg,"/",'')

        partes = cita.split("_")

        b=cur.execute('select * from books where short_name=:libro',{'libro':partes[0]})
        t = b.fetchone()
        bn = t[1]
        bl = t[2]

        cur.execute('select * from verses where book_number = :p1 and chapter = :p2 ',{'p1':bn, "p2":partes[1]})
        r = cur.fetchall()

        salida=""
        salida=bl + " " + str(partes[1]) + "\n" 
        for v in r:
            cital1 = str.replace(v[3],"<J>","")
            cital2 = str.replace(cital1,"</J>","")
            #cital3 = str.replace(cital2,"<t>","")
            #cital4 = str.replace(cital3,"</t>","")
            salida = salida + str(v[2]) + ") " + cital2 + "\n"

        d = cur.execute('select max( chapter) from verses where book_number = :p1 ',{'p1':bn})

        cantidadCap=d.fetchone()[0]

        salida = salida + "\n"
        botones = []
        botones.append([])
        if (int(partes[1]) > 1):
            #salida = salida + "/" + bl + "_" + str(int(partes[1])-1)  + " < "
            botones[0].append({"text":"< " + bl + " " + str(int(partes[1])-1),"callback_data" :"/" + bl + "_" + str(int(partes[1])-1)})
        if (int(partes[1]) < cantidadCap):
            #salida = salida  + " >" + " /" + bl + "_" + str(int(partes[1])+1)
            botones[0].append({"text":"" + bl + " " + str(int(partes[1])+1) + " >","callback_data" :"/" + bl + "_" + str(int(partes[1])+1)})
        markup = {'inline_keyboard': botones}
        return {"txt":salida,"btns":markup}

     

     search = str.replace(msg," ",'%')

     cur.execute('select * from verses where LOWER(text) like LOWER(:p1) ',{'p1':"%{}%".format(search)})

     r = cur.fetchall()

     if bool(r):
           for v in r:
               b=cur.execute('select * from books where book_number=:libro',{'libro':v[0]})     
               salida = "%s \n%s"%(salida,format(" - /%s_%s_%s - \n %s \n"%( b.fetchone()[2] , v[1] , v[2] , v[3] ) ) )
     else:
           salida="Sin resultados - Por el momento solo Buscador. Escriba una palabra o frase a buscar en la Biblia"

     con.close  

     return {"txt":salida}


