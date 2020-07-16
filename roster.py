import sqlite3
import datetime
import pandas as pd
import datetime as dt

def version():
    return "0.5"

def lista_jugadores()->list:
    todos=[]
    conn=sqlite3.connect(".\\mootsRost.sqlite")
    cur=conn.cursor()
    cur.execute("SELECT nombres, apellidos, id FROM Jugadores WHERE activo = 1")
    obt=cur.fetchall()
    if len(obt)<1:
        todos.append("No hay registros de jugadores hasta el momento.")
    else:
        for row in obt:
            todos.append([row[0],row[1],row[2]])
    cur.close()
    return todos

def lista_cumple(fecha:datetime)->list:
    lista=[]
    conn=sqlite3.connect(".\mootsRost.sqlite")
    cur=conn.cursor()
    cur.execute("SELECT nombres,apellidos,nacimiento FROM Jugadores")
    obt=cur.fetchall()
    if len(obt)<1:
        lista.append("No hay registros de jugadores hasta el momento.")
    else:
        for row in obt:
            mes=datetime.datetime.strptime(row[2],'%d/%m/%y').month
            anio=datetime.datetime.strptime(row[2],'%d/%m/y').year
            if mes==fecha.month:
                lista.append("{} {} cumple {} años.".format(row[0],row[1],(fecha.year-anio)))
            if len(lista)<1:
                lista.append("No hay cumpleaños este mes.")
    return lista

def activos()->tuple:
    cantidad=0
    total=0
    conn=sqlite3.connect(".\mootsRost.sqlite")
    cur=conn.cursor()
    cur.execute("SELECT activo FROM Jugadores")
    lista=cur.fetchall()
    if len(lista)>0:
        for row in lista:
            total+=1
            if row[0]==1:
                cantidad+=1
    resp=(total,cantidad)
    return resp

def numeros():
    conn=sqlite3.connect(".\mootsRost.sqlite")
    cur=conn.cursor()
    cur.execute("SELECT numero FROM Jugadores WHERE activo = 1")
    x=cur.fetchall()
    lista=[]
    for n in x:
        lista.append(n[0])
    return lista

def eps():
    conn=sqlite3.connect(".\mootsRost.sqlite")
    cur=conn.cursor()
    cur.execute('SELECT tipo FROM Rh')
    x=cur.fetchall()
    lista=[]
    for n in x:
        lista.append(n[0])
    return lista

def nuevo_jugador(jnuevo):
    msg=""
    if len(jnuevo)==0:
        msg="El diccionario del nuevo jugador está vacío."
    elif "cancelado" in jnuevo.keys():
        msg="El proceso fue cancelado por el usuario."
    else:
        if jnuevo['ndoc']==-1:
            msg="El jugador no puede ser agregado. 'ndoc = -1'"
        else:
            # Definicion de encabezados
            hoja=pd.read_excel(".\datos\encabezados.xlsx")
            df=pd.DataFrame(hoja.values)
            df.columns=df.iloc[0,:]
            df.drop(df.index[0],inplace=True)
            df.drop(df.columns[[0]],axis=1,inplace=True)
            heads=df.columns.values
            try:
                conn=sqlite3.connect(".\mootsRost.sqlite")
                cur=conn.cursor()
            except:
                conn=None
            nuevo=[]
            for elem in heads:
                nuevo.append(jnuevo[elem])
            if conn is not None:
                try:
                    cur.execute('SELECT id FROM Jugadores WHERE (documento,ndoc) = (?,?)',(nuevo[6],nuevo[7]))
                    j_id=cur.fetchone()[0]
                except:
                    j_id=None
            if conn is not None and j_id is None:
                try:
                    #Tabla Ciudades
                    cur.execute('INSERT OR IGNORE INTO ciudades (nombre) VALUES (?)', (nuevo[39],))
                    cur.execute('SELECT id FROM Ciudades WHERE nombre = ?', (nuevo[39],))
                    id_ciur=cur.fetchone()[0]
                    conn.commit()
                    cur.execute('INSERT OR IGNORE INTO ciudades (nombre) VALUES (?)', (nuevo[40],))
                    cur.execute('SELECT id FROM Ciudades WHERE nombre = ?', (nuevo[40],))
                    id_ciun=cur.fetchone()[0]
                    conn.commit()
                    #Tabla Rh
                    cur.execute('INSERT OR IGNORE INTO Rh (tipo) VALUES (?)',(nuevo[41],))
                    cur.execute('SELECT id FROM Rh WHERE tipo = ?',(nuevo[41],))
                    id_rh=cur.fetchone()[0]
                    conn.commit()
                    #Tabla Eps
                    cur.execute('INSERT OR IGNORE INTO Eps (nombre) VALUES (?)', (nuevo[38],))
                    cur.execute('SELECT id FROM Eps WHERE nombre = ?', (nuevo[38],))
                    id_Eps=cur.fetchone()[0]
                    conn.commit()
                    #Tabla Salud
                    cur.execute('''INSERT OR IGNORE INTO Salud (id_eps,id_rh,talla,peso,enfermo,enfermedad,medicamentos,recomendaciones)
                                VALUES (?,?,?,?,?,?,?,?)''',(id_Eps,id_rh,nuevo[19],nuevo[20],nuevo[21],nuevo[22],nuevo[23],nuevo[24]))
                    id_salud=cur.lastrowid
                    conn.commit()
                    #Tabla Barrios
                    cur.execute('INSERT OR IGNORE INTO Barrios (nombre,id_ciudad) VALUES (?,?)',(nuevo[17],id_ciur))
                    cur.execute('SELECT id FROM Barrios WHERE nombre = ? AND id_ciudad = ?',(nuevo[17],id_ciur))
                    id_barrio=cur.fetchone()[0]
                    conn.commit()
                    #Tabla Residencia
                    cur.execute('INSERT INTO Residencia (id_ciudad,barrio,dir) VALUES (?,?,?)',(id_ciur,id_barrio,nuevo[18]))
                    id_residencia=cur.lastrowid
                    conn.commit()
                    #Tabla Instituciones
                    trab=False
                    if nuevo[15] in [1,2]:trab=True
                    cur.execute('INSERT OR IGNORE INTO Instituciones (nombre) VALUES (?)',(nuevo[37],))
                    cur.execute('SELECT id FROM Instituciones WHERE nombre = ?',(nuevo[37],))
                    id_insEd=cur.fetchone()[0]
                    conn.commit()
                    if trab:
                        #TODO pulir una vez se tenga la info actualizada de ocupacion -> trabajo
                        id_trab=-1
                    #Tabla Ocupaciones
                    id_toc=id_insEd
                    if trab:id_toc=id_trab
                    cur.execute('INSERT INTO Ocupacion (ocupacion,nivelEd,id_insti) VALUES (?,?,?)',(nuevo[15],nuevo[16],id_toc))
                    id_ocup=cur.lastrowid
                    conn.commit()
                    #Tabla Ultimate
                    cur.execute('''INSERT INTO Ultimate (anios,seleCol,dSeleCol,seleU,dSeleU,previos,logros,linea,pos,otros,intesidad,vision) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                                ''',(nuevo[25],nuevo[26],nuevo[27],nuevo[28],id_insEd,nuevo[30],nuevo[31],nuevo[32],nuevo[33],nuevo[34],nuevo[35],nuevo[36]))
                    id_ulti=cur.lastrowid
                    conn.commit()
                    #Tabla Jugador
                    hoy=dt.datetime.today()
                    nacim=dt.datetime.strptime(nuevo[4],"%d/%m/%Y")
                    edad=hoy.year-nacim.year
                    cur.execute('''INSERT INTO Jugadores (numero,nombres,apellidos,correo,nacimiento,edad,celular,documento,ndoc,pasaporte,npas,amVisa,apodo,aIngreso,alimentacion,contacto,nContacto,activo,id_ocup,id_res,id_salud,id_ulti,id_ciudad)
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(nuevo[0],nuevo[1],nuevo[2],nuevo[3],nuevo[4],edad,nuevo[5],nuevo[6],nuevo[7],nuevo[8],nuevo[9],nuevo[10],nuevo[11],nuevo[12],nuevo[13],nuevo[42],nuevo[43],nuevo[14],id_ocup,id_residencia,id_salud,id_ulti,id_ciun))
                    conn.commit()
                    id_j=cur.lastrowid
                    cur.execute('SELECT nombres,apellidos,documento,ndoc FROM Jugadores WHERE id = ?',(id_j,))
                    agg=cur.fetchone()
                    conn.close()
                    msg="Se agregó al jugador {} {} con {} No.{}".format(agg[0],agg[1],agg[2],agg[3])
                except ValueError as e:
                    msg="Error al agregar el jugador ({})".format(str(e))
            else:
                msg="El jugador ya está registrado. 'ndoc in db'"
    return msg

def nuevos_formato(ubic,num):
    msg=[]
    hoy=dt.datetime.today()
    listaJug=None
    try:
        df=pd.read_excel(ubic)
        listaJug=df.values
    except:
        msg.append("Hubo un erro al cargar el archivo")
    if listaJug is not None:
        for jugador in listaJug:
            try:
                conn=sqlite3.connect(".\mootsRost.sqlite")
                cur=conn.cursor()
            except:
                msg.append("Existe algún error en la base de datos")
            try:
                cur.execute("SELECT id FROM Jugadores WHERE (documento,ndoc) = (?,?)", (jugador[6],jugador[7]))
                id_e=cur.fetchone()[0]
                msg.append("El jugador {}, {} ya existe con la id: {}".format(jugador[2],jugador[1],id_e))
            except:
                #Tabla Ciudades
                cur.execute('INSERT OR IGNORE INTO ciudades (nombre) VALUES (?)', (jugador[39],))
                cur.execute('SELECT id FROM Ciudades WHERE nombre = ?', (jugador[39],))
                ciudadR=cur.fetchone()[0]
                cur.execute('INSERT OR IGNORE INTO ciudades (nombre) VALUES (?)', (jugador[40],))
                cur.execute('SELECT id FROM Ciudades WHERE nombre = ?', (jugador[40],))
                ciudadN=cur.fetchone()[0]
                #Tabla Rh
                cur.execute('INSERT OR IGNORE INTO Rh (tipo) VALUES (?)',(jugador[41].capitalize(),))
                cur.execute('SELECT id FROM Rh WHERE tipo = ?',(jugador[41],))
                id_rh=cur.fetchone()[0]
                #Tabla Eps
                cur.execute('INSERT OR IGNORE INTO Eps (nombre) VALUES (?)', (jugador[38],))
                cur.execute('SELECT id FROM Eps WHERE nombre = ?', (jugador[38],))
                id_Eps=cur.fetchone()[0]
                #Tabla Salud
                cur.execute('''INSERT OR IGNORE INTO Salud (id_eps,id_rh,talla,peso,enfermo,enfermedad,medicamentos,recomendaciones)
                            VALUES (?,?,?,?,?,?,?,?)''',(id_Eps,id_rh,jugador[19],jugador[20],jugador[21],jugador[22],jugador[23],jugador[24]))
                id_salud=cur.lastrowid
                conn.commit()
                #Tabla Barrios
                cur.execute('INSERT OR IGNORE INTO Barrios (nombre,id_ciudad) VALUES (?,?)',(jugador[17],ciudadR))
                cur.execute('SELECT id FROM Barrios WHERE nombre = ? AND id_ciudad = ?',(jugador[17],ciudadR))
                id_barrio=cur.fetchone()[0]
                #Tabla Residencia
                cur.execute('INSERT INTO Residencia (id_ciudad,barrio,dir) VALUES (?,?,?)',(ciudadR,id_barrio,jugador[18]))
                id_residencia=cur.lastrowid
                #Tabla Instituciones
                trab=False
                if jugador[15] in [1,2]:trab=True
                cur.execute('INSERT OR IGNORE INTO Instituciones (nombre) VALUES (?)',(jugador[37],))
                cur.execute('SELECT id FROM Instituciones WHERE nombre = ?',(jugador[37],))
                id_insEd=cur.fetchone()[0]
                if trab:
                    #TODO pulir una vez se tenga la info actualizada de ocupacion -> trabajo
                    id_trab=-1
                #Tabla Ocupaciones
                id_toc=id_insEd
                if trab:id_toc=id_trab
                cur.execute('INSERT INTO Ocupacion (ocupacion,nivelEd,id_insti) VALUES (?,?,?)',(jugador[15],jugador[16],id_toc))
                id_ocup=cur.lastrowid
                #Tabla Ultimate
                cur.execute('''INSERT INTO Ultimate (anios,seleCol,dSeleCol,seleU,dSeleU,previos,logros,linea,pos,otros,intesidad,vision) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                            ''',(jugador[25],jugador[26],jugador[27],jugador[28],id_insEd,jugador[30],jugador[31],jugador[32],jugador[33],jugador[34],jugador[35],jugador[36]))
                id_ulti=cur.lastrowid
                #Tabla Jugador
                n=jugador[0]
                cur.execute('SELECT numero FROM Jugadores')
                if n in num:n=-1
                nacim=dt.datetime.strftime(jugador[4],"%d/%m/%Y")
                edad=hoy.year-jugador[4].year
                cur.execute('''INSERT INTO Jugadores (numero,nombres,apellidos,correo,nacimiento,edad,celular,documento,ndoc,pasaporte,npas,amVisa,apodo,aIngreso,alimentacion,contacto,nContacto,activo,id_ocup,id_res,id_salud,id_ulti,id_ciudad)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(jugador[0],jugador[1],jugador[2],jugador[3],nacim,edad,jugador[5],jugador[6],jugador[7],jugador[8],jugador[9],jugador[10],jugador[11],jugador[12],jugador[13],jugador[42],jugador[43],jugador[14],id_ocup,id_residencia,id_salud,id_ulti,ciudadN))
                conn.commit()
                idn=cur.lastrowid()
                msg.append("Se agrego al jugador {}, {} con id: {}".format(jugador[2],jugador[1],idn))
        cur.close()
    return msg

def borrar_jugador(idd):
    msg=""
    try:
        conn=sqlite3.connect(".\mootsRost.sqlite")
        cur=conn.cursor()
        try:
            print(idd)
            print(type(idd))
            cur.execute('SELECT id_ocup,id_res,id_salud,id_ulti FROM Jugadores WHERE id = ?',(idd,))
            print(cur.fetchall())
            try:
                ids=cur.fetchone()
                cur.execute('DELETE FROM Ocupacion WHERE id = ?',(ids[0],))
                cur.execute('DELETE FROM Residencia WHERE id = ?',(ids[1],))
                cur.execute('DELETE FROM Salud WHERE id = ?',(ids[2],))
                cur.execute('DELETE FROM Ultimate WHERE id = ?',(ids[3],))
                msg="El jugador con id {} fue borrado de la base de datos.".format(idd)
            except Exception as e:
                msg="Error al intentar borrar al jugador con id: {} ({})".format(idd,str(e))
        except Exception as e:
            msg="El Jugador con el id {} no está registrado en la base de datos.".format(idd)
    except:
        msg="Hubo un problema al cargar la base de datos"
    return msg