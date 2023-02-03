from ast import Return
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bcrypt import check_password_hash
from distutils.util import execute
from re import A, U
from telnetlib import SE
from flask import Flask, redirect,url_for,session
from flask import render_template,request,redirect, url_for,session, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from flaskext.mysql import MySQL
from datetime import datetime

import bcrypt
import os
from flask import send_from_directory
NoneType = type(None)
app= Flask(__name__)    
mysql= MySQL()

app.config['MYSQL_DATABASE_HOST']='us-cdbr-east-06.cleardb.net'
app.config['MYSQL_DATABASE_USER']='b72abba5681628'
app.config['MYSQL_DATABASE_PASSWORD']='ee391464'
app.config['MYSQL_DATABASE_DB']='heroku_323cf7babebbf2c'
app.config['MYSQL_CURSORCLASS']=''
mysql.init_app(app)


mysql=MySQL(app)
NoneType = type(None)
CARPETA=os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)





#####VISTA DE REPUESTOS######
@app.route('/view')
def home():
    sql= "select NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO  from repuesto inner join AUTO on REPUESTO.CODIGO_AUTO = AUTO.CODIGO_AUTO "
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    datos=cursor.fetchall()
    print (datos)
    conn.commit
    return render_template('empleados/view.html', datos=datos) 

####FIN VISTA DE REPUESTOS####

####CREAR NUEVO REPUESTO####

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _REPUESTO=request.form['txtREPUESTO']
    _MODELO=request.form['txtMODELO']
    _MARCA=request.form['txtMARCA']
    _ANIO=request.form['txtANIO']
    _UBICACION=request.form['txtUBICACION']
    _CODIGOBARRA=request.form['txtCODIGO']
    _PRECIO=request.form['txtPrecio']
    _FOTO=request.files['txtFoto']
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    
    if _FOTO.filename!='':
        nuevoNombreFoto=tiempo+_FOTO.filename
        _FOTO.save("uploads/"+nuevoNombreFoto)
        
    #####VERIFICAR SI EXISTE EL AUTO####
    sql1="SELECT CODIGO_AUTO FROM AUTO WHERE MARCA=%s AND MODELO =%s and ANIO=%s"
    datos1=(_MARCA,_MODELO,_ANIO)
    #####SELECT DEL ULTIMO CODIGO DE AUTO####
    sql3 ="SELECT CODIGO_AUTO + 1 FROM auto ORDER BY CODIGO_AUTO DESC LIMIT 1;"

    #####OBTENER EL CODIGO DEL AUTO SI ES QUE EXISTE#####
    sql9='select CODIGO_AUTO from auto where upper(MARCA)=%s and upper(MODELO)=%s and upper(ANIO)=%s'
    datos9=(_MARCA,_MODELO,_ANIO)

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql1,datos1)
    auto=cursor.fetchone()

    conn.commit()
    
    if auto[0] < 1:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql3)
        codigoauto=0
        codigoauto=cursor.fetchone()
        CODIGOAUTONUEVO = codigoauto[0]
        ######INSERT DE TIPO DE AUTO#######
        sql="INSERT INTO auto (MARCA,MODELO,ANIO,CODIGO_AUTO) VALUES (%s,%s,%s,%s);"
        datosauto=(_MARCA, _MODELO, _ANIO, CODIGOAUTONUEVO)
        
        ######INSERT DE REPUESTO#####
        sql2="INSERT INTO repuesto (NOMBRE_REPUESTO, UBICACION, CODIGO_AUTO, CODIGO_BARRA, PRECIO, FOTO) VALUES (%s,%s,%s,%s,%s,%s)"
        datosRepuesto=(_REPUESTO,_UBICACION,CODIGOAUTONUEVO,_CODIGOBARRA,_PRECIO,nuevoNombreFoto)
    
        cursor.execute(sql,datosauto)
        cursor.execute(sql2,datosRepuesto)
        conn.commit()
    else:
        
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql9,datos9)
        codigoauto=cursor.fetchone()
        sql45="INSERT INTO repuesto (NOMBRE_REPUESTO, UBICACION, CODIGO_AUTO, CODIGO_BARRA, PRECIO,FOTO) VALUES (%s,%s,%s,%s,%s,%s)"
        datosRepuesto=(_REPUESTO,_UBICACION,codigoauto,_CODIGOBARRA, _PRECIO,nuevoNombreFoto)
        cursor.execute(sql45,datosRepuesto)
        conn.commit()

    
    return redirect ('/view')

####FIN CREAR NUEVO REPUESTO####




####FILTRAR REPUESTOS####

###TOMA DATOS FORM###
@app.route("/store10", methods=['POST'])
def func():
    _nombrerepuesto=request.form['txtNombreRepuesto']
    _marca=request.form['txtMarca']
    _modelo=request.form['txtModelo']
    _anio=request.form['txtANIO']
    _codigo=request.form['txtCodigo']
    global CODIGOBARRAFILTRO
    CODIGOBARRAFILTRO = _codigo
    global NOMBREREPUESTO
    NOMBREREPUESTO =_nombrerepuesto
    global MARCA
    MARCA=_marca
    global MODELO
    MODELO=_modelo
    global ANIO
    ANIO=_anio
    global DATOSBUSQUEDA
    DATOSBUSQUEDA = (NOMBREREPUESTO,MARCA,MODELO,ANIO)
    return redirect ('/viewfiltrado')
###FIN TOMA DATOS FORM###

@app.route('/viewfiltrado')
def viewfiltrado2():

    if NOMBREREPUESTO!='NOMBRE REPUESTO' and MODELO!='MODELO' and ANIO!='AÑO':
        sql="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO WHERE NOMBRE_REPUESTO=%s AND MODELO=%s AND ANIO=%d;"
        conn=mysql.connect()
        cursor=conn.cursor()
        DATOSFILTRO=(NOMBREREPUESTO,MODELO,ANIO)
        cursor.execute(sql,DATOSFILTRO)
        datos=cursor.fetchall()
        conn.commit
    

    elif NOMBREREPUESTO!='NOMBRE REPUESTO' and MARCA!='MARCA':
        sql="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO WHERE NOMBRE_REPUESTO=%s AND MARCA=%s;"
        conn=mysql.connect()
        cursor=conn.cursor()
        DATOSFILTRO=(NOMBREREPUESTO,MARCA)
        cursor.execute(sql,DATOSFILTRO)
        datos=cursor.fetchall()
        conn.commit    


     
    elif NOMBREREPUESTO!='NOMBRE REPUESTO' and MODELO!='MODELO':
        sql="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO WHERE NOMBRE_REPUESTO=%s AND MODELO=%s;"
        conn=mysql.connect()
        cursor=conn.cursor()
        DATOSFILTRO=(NOMBREREPUESTO,MODELO)
        cursor.execute(sql,DATOSFILTRO)
        datos=cursor.fetchall()
        conn.commit
    
    elif NOMBREREPUESTO!='NOMBRE REPUESTO' and ANIO!='AÑO':
        sql="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO WHERE NOMBRE_REPUESTO=%s AND ANIO=%s;"
        conn=mysql.connect()
        cursor=conn.cursor()
        DATOSFILTRO=(NOMBREREPUESTO,ANIO)
        cursor.execute(sql,DATOSFILTRO)
        datos=cursor.fetchall()
        conn.commit

    elif MARCA!='MARCA' and ANIO!='AÑO':
        sql="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO WHERE MARCA=%s AND ANIO=%s;"
        conn=mysql.connect()
        cursor=conn.cursor()
        DATOSFILTRO=(MARCA,ANIO)
        cursor.execute(sql,DATOSFILTRO)
        datos=cursor.fetchall()
        conn.commit
    
    elif MODELO!='MODELO' and ANIO!='AÑO':
        sql="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO WHERE MODELO=%s AND ANIO=%s;"
        conn=mysql.connect()
        cursor=conn.cursor()
        DATOSFILTRO=(MODELO,ANIO)
        cursor.execute(sql,DATOSFILTRO)
        datos=cursor.fetchall()
        conn.commit    
    

    elif NOMBREREPUESTO!='NOMBRE REPUESTO':
        sql="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO WHERE NOMBRE_REPUESTO = %s"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,NOMBREREPUESTO)
        datos=cursor.fetchall()
        conn.commit
    
    elif MARCA!='MARCA':
        sql="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO WHERE MARCA=%s"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,MARCA)
        datos=cursor.fetchall()
        conn.commit



    elif MODELO!='MODELO':
        sql="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO WHERE MODELO=%s"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,MODELO)
        datos=cursor.fetchall()
        conn.commit
    
    elif ANIO!='AÑO':
        sql="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO WHERE ANIO=%s"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,ANIO)
        datos=cursor.fetchall()
        conn.commit
        
    elif CODIGOBARRAFILTRO!='CODIGO':
        sql="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO WHERE CODIGO_BARRA=%s"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,CODIGOBARRAFILTRO)
        datos=cursor.fetchall()
        conn.commit
    
    else:
        sql ="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO,FOTO,CODIGO_BARRA FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO" 
        conn= mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)
        datos=cursor.fetchall()
        conn.commit 
    return render_template('empleados/view.html', datos=datos)
    
####FIN FILTRAR REPUESTOS####




####ELIMINAR REPUESTOS####

@app.route('/eliminar/<int:CODIGO_BARRA>')
def delete (CODIGO_BARRA):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM repuesto WHERE CODIGO_BARRA=%s",(CODIGO_BARRA))
    conn.commit()
    return redirect ('/view')
####FIN ELIMINAR REPUESTOS####


####EDITAR REPUESTOS####
@app.route('/edit/<int:CODIGO_BARRA>')
def edit (CODIGO_BARRA):
    conn=mysql.connect()
    cursor=conn.cursor()
    global CODIGOBARRAGLOBAL
    CODIGOBARRAGLOBAL = CODIGO_BARRA
    sql="SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO, CODIGO_BARRA,FOTO FROM repuesto INNER JOIN auto ON repuesto.codigo_auto = auto.codigo_auto WHERE CODIGO_BARRA=%s;"
    cursor.execute(sql, CODIGOBARRAGLOBAL)
    datos=cursor.fetchall()
    print (datos)
    conn.commit()
    return render_template ('empleados/edit.html', datos=datos)

    ####FUNCION EDITAR  REPUESTOS####
@app.route("/store76", methods=['POST'])
def store76():
    _nombrerepuesto=request.form['txtNombreRepuesto']
    _MARCA=request.form['txtMarca']
    _MODELO=request.form['txtModelo']
    _ANIO=request.form['txtAnio']
    _ubicacion=request.form['txtUbicacion']
    _precio=request.form['txtPrecio']
    _codigobarra=request.form['txtCodigoBarra']
    _FOTO=request.files['txtFoto']
    
    
    now=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    
    if _FOTO.filename!='':
        nuevoNombreFoto=tiempo+_FOTO.filename
        _FOTO.save("uploads/"+nuevoNombreFoto)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("SELECT FOTO FROM repuesto WHERE CODIGO_BARRA=%s",CODIGOBARRAGLOBAL)
        fila=cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE repuesto SET foto=%s WHERE CODIGO_BARRA=%s",(nuevoNombreFoto,CODIGOBARRAGLOBAL))
        conn.commit()
    
    ####VERIFICA SI EL AUTO EXISTE####
    sql2="SELECT COUNT(*) FROM heroku_2f50abf59f2ecd3.auto WHERE MARCA = %s and MODELO =%s and ANIO=%s"
    datos1=(_MARCA,_MODELO,_ANIO)
    ##################################  
    sql3 ="SELECT CODIGO_AUTO + 1 FROM auto ORDER BY CODIGO_AUTO DESC LIMIT 1;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql2,datos1)
    auto=cursor.fetchone()
    conn.commit()
    
    if auto[0] < 1:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql3)
        codigoauto=0
        codigoauto=cursor.fetchone()

        CODIGOAUTONUEVO = codigoauto[0]
        
        ######INSERT DE TIPO DE AUTO#######
        sql="INSERT INTO heroku_2f50abf59f2ecd3.auto (MARCA,MODELO,ANIO,CODIGO_AUTO) VALUES (%s,%s,%s,%s);"
        datosauto=(_MARCA, _MODELO, _ANIO, CODIGOAUTONUEVO)
        #####UPDATE REPUESTO#####
        sql1="UPDATE repuesto SET CODIGO_AUTO=%s,NOMBRE_REPUESTO=%s,UBICACION=%s,precio=%s,CODIGO_BARRA=%s where CODIGO_BARRA=%s"
        editrepuesto=(CODIGOAUTONUEVO,_nombrerepuesto,_ubicacion,_precio,_codigobarra, CODIGOBARRAGLOBAL)
        cursor.execute(sql,datosauto)
        cursor.execute(sql1,editrepuesto)
        conn.commit()
    
    else:
        sql1="UPDATE repuesto SET NOMBRE_REPUESTO=%s,UBICACION=%s,precio=%s,CODIGO_BARRA=%s where codigo_barra=%s"
        editrepuesto=(_nombrerepuesto,_ubicacion,_precio,_codigobarra, CODIGOBARRAGLOBAL)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql1,editrepuesto)
        conn.commit()
    return redirect ('/view')
    ####FIN EDITAR REPUESTOS####
    
####AGREGAR AL CARRITO####
@app.route("/agregar/<int:CODIGO_BARRA>")
def agregar(CODIGO_BARRA):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute ("INSERT INTO `resumen_ventas`(`NOMBRE_REPUESTO`, `MARCA`, `MODELO`, `ANIO`, `UBICACION`, `PRECIO`, `CODIGO_BARRA`,FOTO, CODIGO_AUTO) SELECT NOMBRE_REPUESTO, MARCA, MODELO, ANIO, UBICACION, PRECIO ,CODIGO_BARRA,FOTO, repuesto.CODIGO_AUTO FROM repuesto INNER JOIN auto ON repuesto.CODIGO_AUTO = auto.CODIGO_AUTO WHERE CODIGO_BARRA = %s",(CODIGO_BARRA))
    cursor.execute("DELETE FROM repuesto where CODIGO_BARRA = %s",(CODIGO_BARRA))
    conn.commit()
    return redirect('/view')

@app.route("/dismiss/<int:CODIGO_BARRA>")
def dismiss(CODIGO_BARRA):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO repuesto SELECT NOMBRE_REPUESTO, UBICACION ,PRECIO,CODIGO_AUTO, CODIGO_BARRA, FOTO from resumen_ventas WHERE CODIGO_BARRA=%s",(CODIGO_BARRA))
    cursor.execute("DELETE FROM resumen_ventas WHERE CODIGO_BARRA=%s",(CODIGO_BARRA))    
    conn.commit()
    return redirect('/sell')    


#####VENTA####

@app.route("/sell")
def sell():
    conn=mysql.connect()
    cursor=conn.cursor()
    sql="SELECT * FROM resumen_ventas;"
    sql1="select SUM(PRECIO) from resumen_ventas;"
    cursor.execute(sql)
    datos=cursor.fetchall() 
    cursor.execute(sql1)
    datos1=cursor.fetchall()
    conn.commit()
    return render_template('empleados/sell.html',datos=datos,datos1=datos1)

@app.route("/carrito", methods=['POST'])
def carrito():
    if "btnVender" in request.form:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO registro_ventas SELECT NOMBRE_REPUESTO,MARCA,MODELO,ANIO,UBICACION,PRECIO,CODIGO_BARRA,CURRENT_TIMESTAMP from resumen_ventas;")    
        cursor.execute("DELETE from repuesto where CODIGO_BARRA IN (select CODIGO_BARRA from resumen_ventas);")
        cursor.execute("DELETE FROM resumen_ventas;")
        conn.commit()
        return redirect("/view")
    elif "btnLimpiar" in request.form:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO repuesto SELECT NOMBRE_REPUESTO, UBICACION , PRECIO, CODIGO_AUTO, CODIGO_BARRA, FOTO from resumen_ventas")
        cursor.execute("DELETE FROM resumen_ventas;")
        conn.commit()
        return redirect("/sell")

#####FIN VENTA####

#####REGISTRO DE VENTAS#####
@app.route("/registroventa")
def registroventa():


    sql= "SELECT * FROM registro_ventas order by FECHA_VENTA desc"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    datos=cursor.fetchall()
    conn.commit
    return render_template("empleados/registroventa.html",datos=datos)
     
#####FIN REGISTRO VENTAS####

####INCIO LOGIN#####

@app.route("/")
def home_register():
    return render_template("empleados/login.html")

@app.route("/login_error")
def login_error():
    return render_template("empleados/login_error.html")

@app.route("/storereg", methods=['POST'])
def storereg():
    username=request.form['txtUser']
    password=request.form['txtPass'].encode('utf-8')

    print(password)
    hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
    conn=mysql.connect()
    cursor=conn.cursor()
    sql45="INSERT INTO user (username, password) VALUES (%s,%s)"
    datos=(username,hash_password)
    cursor.execute(sql45,datos)
    conn.commit()
    return redirect("/view")



@app.route("/login", methods=['GET' , 'POST'])
def login():
    if request.method=="POST":
        username= request.form['txtUser']
        password= request.form['txtPass']
        conn=mysql.connect()
        cursor=conn.cursor()
        error_msje=""
        flash(error_msje)
        cursor.execute("SELECT password FROM user where username =%s",(username,))
        hash = cursor.fetchone()
        conn.commit()
        bcrypt = Bcrypt(app)
        if len(username) > 0:
            if bcrypt.check_password_hash(hash[0], password):
                print ("PASOOOOOO")
                return redirect('/view')
            else:
                flash("Uuario y/o password incorrectos")
                return redirect("/")
        else:
            return redirect("/")
    else:
        return render_template("empleados/login.html")





if __name__== '__main__':
    app.secret_key='KADJWumeisOSD##!#&'
 

    app.run(debug=True)

