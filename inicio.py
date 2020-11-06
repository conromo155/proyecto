from flask import Flask, g, render_template, request, redirect, url_for, flash, session
import pymysql
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "cetis155"


# Carpeta de subida
app.config['UPLOAD_FOLDER'] = './pdfs'

#clase de usuarios
class user:
    def __init__(self,id,username, password, id_funcion, funcion):
        self.id = id
        self.username = username
        self.password = password
        self.id_funcion = id_funcion
        self.funcion=funcion
    def __repr__(self):
        return '<User:{self.username}>'

#objeto de la clase usuarios
users=[]






@app.before_request
def before_request():
    if 'user_id' in session:
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('select a.id_usuario, a.usuario, a.password, a.nombre, a.id_perfil, b.descripcion from usuario a, perfil_admo b where a.id_usuario = %s and b.id_perfil=a.id_perfil', (session['user_id']))
        dato = cursor.fetchone()
        users.clear()
        users.append(user(id=dato[0], username=dato[3], password=dato[2], id_funcion=dato[4], funcion=dato[5]))
        g.user=users[0]



@app.route('/')
def login():
    return render_template("login.html")


@app.route('/home')
def home():

    return render_template('home.html')



@app.route('/inicio', methods=['POST'])
def inicio():
    session.pop('user_id', None)
    if request.method == 'POST':
        username=request.form['usuario']
        password=request.form['passw']
        #busca en la base de datos de usuarios
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('select id_usuario, usuario, password, nombre, id_perfil from usuario where usuario = %s and password=%s', (username,password))
        dato = cursor.fetchone()
        if dato==None:
            return render_template("login.html")
        else:
            session['user_id'] = dato[0]
            return redirect(url_for('home'))

    return render_template("login.html")

@app.route('/salir')
def salir():
    session.pop('user_id')
    return render_template("login.html")



#------------------------------- nivel -------------------------------------------------
@app.route('/nivel')
def nivel():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
    datos=cursor.fetchall()
    return render_template("nivel.html", niveles = datos )

@app.route('/nvo_nivel')
def nvo_nivel():
    return render_template("agr_nivel.html")

@app.route('/agrega_nivel', methods=['POST'])
def agrega_nivel():
    if request.method == 'POST':
        aux_Descripcion=request.form['descripcion']
        if aux_Descripcion=="":
            error="La descripción del nivel no acepta valores nulos"
            return render_template("error.html", des_error=error)

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into nivelacademico (Descripcion) values (%s)',(aux_Descripcion))
        conn.commit()
    return redirect(url_for('nivel'))


@app.route('/ed_nivel/<string:id>')
def ed_nivel(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idNivelAcademico, Descripcion from nivelacademico where idNivelAcademico = %s', (id))
    dato=cursor.fetchall()
    return render_template("edi_nivel.html", nivel = dato[0])

@app.route('/modifica_nivel/<string:id>', methods=['POST'])
def modifica_nivel(id):
    if request.method == 'POST':
        descrip=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('update nivelacademico set  Descripcion=%s where idNivelAcademico=%s',(descrip,id))
        conn.commit()
    return redirect(url_for('nivel'))

@app.route('/bo_nivel/<string:id>')
def bo_nivel(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select 	count(*) from solicitud where idNivelAcademico = {0}'.format(id))
    solicitudes = cursor.fetchone()
    cursor.execute('select count(*) from candidato_has_nivelacademico where idNivelAcademico = {0}'.format(id))
    solicitantes = cursor.fetchone()
    if ((solicitudes[0]!=0) and (solicitantes[0] != 0)):
        error = "El nivel tiene dependientes no puede ser borrado"
        return render_template("error.html", des_error=error)
    else:
        cursor.execute('delete from nivelacademico where idNivelAcademico = {0}'.format(id))
        conn.commit()
        return redirect(url_for('nivel'))


#------------------------------- carrera -------------------------------------------------
@app.route('/carrera')
def carrera():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
    datos=cursor.fetchall()
    return render_template("carrera.html", carreras = datos )

@app.route('/agrega_carrera', methods=['POST'])
def agrega_carrera():
    if request.method == 'POST':
        aux_Descripcion=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into carrera (Descripcion) values (%s)',(aux_Descripcion))
        conn.commit()
    return redirect(url_for('carrera'))

@app.route('/nvo_carrera')
def nvo_carrera():
    return render_template("agr_carrera.html")

@app.route('/modifica_carrera/<string:id>', methods=['POST'])
def modifica_carrera(id):
    if request.method == 'POST':
        descrip=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('update carrera set  Descripcion=%s where idCarrera=%s',(descrip,id))
        conn.commit()
    return redirect(url_for('carrera'))

@app.route('/ed_carrera/<string:id>')
def ed_carrera(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idCarrera, Descripcion from carrera where idCarrera = %s', (id))
    dato=cursor.fetchall()
    return render_template("edi_carrera.html", carrera = dato[0])



@app.route('/bo_carrera/<string:id>')
def bo_carrera(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from carrera where idCarrera = {0}'.format(id))
    conn.commit()
    return redirect(url_for('carrera'))


#------------------------------- idioma -------------------------------------------------
@app.route('/idioma')
def idioma():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idIdioma, lenguaje from idioma order by lenguaje')
    datos=cursor.fetchall()
    return render_template("idioma.html", idiomas = datos )

@app.route('/agrega_idioma', methods=['POST'])
def agrega_idioma():
    if request.method == 'POST':
        aux_Descripcion=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into idioma (lenguaje) values (%s)',(aux_Descripcion))
        conn.commit()
    return redirect(url_for('idioma'))

@app.route('/nvo_idioma')
def nvo_idioma():
    return render_template("agr_idioma.html")

@app.route('/modifica_idioma/<string:id>', methods=['POST'])
def modifica_idioma(id):
    if request.method == 'POST':
        descrip=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('update idioma set  lenguaje=%s where idIdioma=%s',(descrip,id))
        conn.commit()
    return redirect(url_for('idioma'))

@app.route('/ed_idioma/<string:id>')
def ed_idioma(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idIdioma, lenguaje from idioma where idIdioma = %s', (id))
    dato=cursor.fetchall()
    return render_template("edi_idioma.html", idioma = dato[0])



@app.route('/bo_idioma/<string:id>')
def bo_idioma(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from idioma where idIdioma = {0}'.format(id))
    conn.commit()
    return redirect(url_for('idioma'))

#------------------------------- puesto -------------------------------------------------
@app.route('/puesto')
def puesto():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion from puesto order by Descripcion')

    datos=cursor.fetchall()
    return render_template("puesto.html", puestos = datos )

@app.route('/agrega_puesto', methods=['POST'])
def agrega_puesto():
    if request.method == 'POST':
        aux_des =request.form['descripcion']
        aux_sal = request.form['salario']
        aux_ben = request.form['beneficios']
        aux_bon = request.form['bonos']
        aux_aut = request.form['autorizar']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into puesto (Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion) values (%s,%s,%s,%s,%s)',(aux_des, aux_sal,aux_ben, aux_bon, aux_aut))
        conn.commit()

        cursor.execute('select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion '
                       'from  puesto where idPuesto=(select max(idPuesto) from puesto)')
        datos=cursor.fetchall()
        cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
                       ' from  puesto a, habilidad b,puesto_has_habilidad c '
                       ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=(select max(idPuesto) from puesto)')
        datos1 = cursor.fetchall()
        cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
                       'from  puesto a, idioma b,puesto_has_idioma c '
                       'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=(select max(idPuesto) from puesto)')
        datos2=cursor.fetchall()
        cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()
        cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()
    return render_template("edi_puesto.html", puestos = datos, pue_habs=datos1, pue_idis=datos2, habs=datos3, idiomas=datos4 )


@app.route('/nvo_puesto')
def nvo_puesto():
    return render_template("agr_puesto.html")

@app.route('/modifica_puesto/<string:id>', methods=['POST'])
def modifica_puesto(id):
    if request.method == 'POST':
        aux_des =request.form['descripcion']
        aux_sal = request.form['salario']
        aux_ben = request.form['beneficios']
        aux_bon = request.form['bonos']
        aux_aut = request.form['autorizar']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('update puesto set Descripcion=%s, SalarioAnual=%s, Beneficios=%s, Bonos=%s, Aprobacion=%s where idpuesto=%s', (aux_des, aux_sal,aux_ben, aux_bon, aux_aut,id))
        conn.commit()
    return redirect(url_for('puesto'))

@app.route('/ed_puesto/<string:id>')
def ed_puesto(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion '
                   'from  puesto where idPuesto=%s', (id))
    datos=cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
                   ' from  puesto a, habilidad b,puesto_has_habilidad c '
                   ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s', (id))
    datos1 = cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
                   'from  puesto a, idioma b,puesto_has_idioma c '
                   'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s', (id))
    datos2=cursor.fetchall()
    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    return render_template("edi_puesto.html", puestos = datos, pue_habs=datos1, pue_idis=datos2, habs=datos3, idiomas=datos4 )

@app.route('/bo_puesto/<string:id>')
def bo_puesto(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from puesto_has_Idioma where idPuesto = {0}'.format(id))
    conn.commit()
    cursor.execute('delete from puesto_has_habilidad where idPuesto = {0}'.format(id))
    conn.commit()
    cursor.execute('delete from puesto where idPuesto = {0}'.format(id))
    conn.commit()

    return redirect(url_for('puesto'))



@app.route('/agrega_hab_pto', methods=['POST'])
def agrega_hab_pto():
    if request.method == 'POST':
        aux_pto=request.form['pto']
        aux_hab = request.form['habil']
        aux_exp = request.form['expe']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into puesto_has_habilidad (idPuesto, idHabilidad, Experiencia) values (%s,%s,%s)',(aux_pto,aux_hab,aux_exp))
        conn.commit()

        cursor.execute('select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion '
                       'from  puesto where idPuesto=%s', (aux_pto))
        datos = cursor.fetchall()
        cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
                       ' from  puesto a, habilidad b,puesto_has_habilidad c '
                       ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s', (aux_pto))
        datos1 = cursor.fetchall()
        cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
                       'from  puesto a, idioma b,puesto_has_idioma c '
                       'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s', (aux_pto))
        datos2 = cursor.fetchall()
        cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()
        cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()
    return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3, idiomas=datos4)


@app.route('/agrega_idio_pto', methods=['POST'])
def agrega_idio_pto():
    if request.method == 'POST':
        aux_pto = request.form['ptoi']
        aux_idi = request.form['idio']
        aux_niv = request.form['nive']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into puesto_has_idioma (idPuesto, idIdioma, Nivel) values (%s,%s,%s)',(aux_pto,aux_idi,aux_niv))
        conn.commit()

        cursor.execute('select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion '
                       'from  puesto where idPuesto=%s', (aux_pto))
        datos = cursor.fetchall()
        cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
                       ' from  puesto a, habilidad b,puesto_has_habilidad c '
                       ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s', (aux_pto))
        datos1 = cursor.fetchall()
        cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
                       'from  puesto a, idioma b,puesto_has_idioma c '
                       'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s', (aux_pto))
        datos2 = cursor.fetchall()
        cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()
        cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()
    return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3, idiomas=datos4)


@app.route('/bo_hab_pto/<string:idP>/<string:idH>')
def bo_hab_pto(idP,idH):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from puesto_has_habilidad where idPuesto =%s and idHabilidad=%s ',(idP,idH))
    conn.commit()


    cursor.execute('select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion '
                   'from  puesto where idPuesto=%s', (idP))
    datos = cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
                   ' from  puesto a, habilidad b,puesto_has_habilidad c '
                   ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s', (idP))
    datos1 = cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
                   'from  puesto a, idioma b,puesto_has_idioma c '
                   'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s', (idP))
    datos2 = cursor.fetchall()
    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3, idiomas=datos4)


@app.route('/bo_idi_pto/<string:idP>/<string:idI>')
def bo_idi_pto(idP,idI):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from puesto_has_idioma where idPuesto =%s and idIdioma=%s ',(idP,idI))
    conn.commit()
    cursor.execute('select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion '
                   'from  puesto where idPuesto=%s', (idP))
    datos = cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
                   ' from  puesto a, habilidad b,puesto_has_habilidad c '
                   ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s', (idP))
    datos1 = cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
                   'from  puesto a, idioma b,puesto_has_idioma c '
                   'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s', (idP))
    datos2 = cursor.fetchall()
    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3, idiomas=datos4)




#------------------------------- medio -------------------------------------------------
@app.route('/medio')
def medio():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idMedioPublicidad, Descripcion from mediopublicidad order by descripcion')
    datos=cursor.fetchall()
    return render_template("medio.html", medios = datos )

@app.route('/agrega_medio', methods=['POST'])
def agrega_medio():
    if request.method == 'POST':
        aux_Descripcion=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into mediopublicidad (Descripcion) values (%s)',(aux_Descripcion))
        conn.commit()
    return redirect(url_for('medio'))

@app.route('/nvo_medio')
def nvo_medio():
    return render_template("agr_medio.html")

@app.route('/modifica_medio/<string:id>', methods=['POST'])
def modifica_medio(id):
    if request.method == 'POST':
        descrip=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('update mediopublicidad set  descripcion=%s where idMedioPublicidad=%s',(descrip,id))
        conn.commit()
    return redirect(url_for('medio'))

@app.route('/ed_medio/<string:id>')
def ed_medio(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idMedioPublicidad, Descripcion from mediopublicidad where idMedioPublicidad = %s', (id))
    dato=cursor.fetchall()
    return render_template("edi_medio.html", medio = dato[0])


@app.route('/bo_medio/<string:id>')
def bo_medio(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from mediopublicidad where idMedioPublicidad = {0}'.format(id))
    conn.commit()
    return redirect(url_for('medio'))


#------------------------------- contacto -------------------------------------------------
@app.route('/contacto')
def contacto():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()

    cursor.execute('select idcontacto, Nombre, Domicilio, Razon_Social, Telefono from contacto order by nombre')
    datos=cursor.fetchall()
    return render_template("contacto.html", contactos = datos )

@app.route('/agrega_contacto', methods=['POST'])
def agrega_contacto():
    if request.method == 'POST':
        aux_nom =request.form['nombre']
        aux_dom = request.form['domicilio']
        aux_raz = request.form['razon']
        aux_tel = request.form['telefono']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into contacto (Nombre,Domicilio,Razon_social,Telefono) values (%s,%s,%s,%s)',(aux_nom, aux_dom,aux_raz, aux_tel))
        conn.commit()
    return redirect(url_for('contacto'))

@app.route('/nvo_contacto')
def nvo_contacto():
    return render_template("agr_contacto.html")

@app.route('/modifica_contacto/<string:id>', methods=['POST'])
def modifica_contacto(id):
    if request.method == 'POST':
        aux_nom =request.form['nombre']
        aux_dom = request.form['domicilio']
        aux_raz = request.form['razon']
        aux_tel = request.form['telefono']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('update contacto set Nombre=%s,Domicilio=%s,Razon_social=%s,Telefono=%s where idContacto=%s',(aux_nom, aux_dom,aux_raz, aux_tel,id))
        conn.commit()
    return redirect(url_for('contacto'))

@app.route('/ed_contacto/<string:id>')
def ed_contacto(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idContacto, Nombre, Domicilio, Razon_social, telefono from contacto where idContacto = %s', (id))
    dato=cursor.fetchall()
    return render_template("edi_contacto.html", contacto = dato[0])



@app.route('/bo_contacto/<string:id>')
def bo_contacto(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from contacto where idContacto = {0}'.format(id))
    conn.commit()
    return redirect(url_for('contacto'))

#------------------------------- contacto -------------------------------------------------
@app.route('/empresa')
def empresa():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('SELECT idEmpresa, Nombre_de_empresa, Descripcion, telefono, domicilio, E_mail, RazonSocial, EStructura_Juridica, Encargado, CIF_Empresa FROM datos_de_empresa ORDER BY nombre_de_empresa')
    datos=cursor.fetchall()
    return render_template("empresa.html", empresas = datos )


@app.route('/modifica_empresa/<string:id>', methods=['POST'])
def modifica_empresa(id):
    if request.method == 'POST':
        aux_nom =request.form['nombre']
        aux_raz = request.form['razon']
        aux_des = request.form['descripcion']
        aux_dom = request.form['domicilio']

        aux_tel =request.form['telefono']
        aux_cor = request.form['correoe']
        aux_est = request.form['estructura']
        aux_enc = request.form['encargado']
        aux_cif = request.form['CIF']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute(''
        'update datos_de_empresa set Nombre_de_empresa=%s, Descripcion=%s, telefono=%s, domicilio=%s, E_mail=%s, RazonSocial=%s' 
        ', Estructura_Juridica=%s, Encargado=%s, CIF_Empresa=%s',(aux_nom,aux_des,aux_tel,aux_dom,aux_cor,aux_raz,aux_est,aux_enc,aux_cif))
        conn.commit()
    return redirect(url_for('empresa'))

@app.route('/ed_empresa/<string:id>')
def ed_empresa(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute(''
                   'SELECT idEmpresa, Nombre_de_empresa, Descripcion, telefono, domicilio, E_mail, RazonSocial, Estructura_Juridica'
                   ', Encargado, CIF_Empresa FROM datos_de_empresa ORDER BY nombre_de_empresa')

    dato=cursor.fetchall()
    return render_template("edi_empresa.html", empresa = dato[0])


#------------------------------- habilidad -------------------------------------------------
@app.route('/habilidad')
def habilidad():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos=cursor.fetchall()
    return render_template("habilidad.html", habilidades = datos )

@app.route('/nvo_habilidad')
def nvo_habilidad():
    return render_template("agr_habilidad.html")

@app.route('/agrega_habilidad', methods=['POST'])
def agrega_habilidad():
    if request.method == 'POST':
        aux_Descripcion=request.form['descripcion']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into habilidad (Descripcion) values (%s)',(aux_Descripcion))
        conn.commit()
    return redirect(url_for('habilidad'))


@app.route('/ed_habilidad/<string:id>')
def ed_habilidad(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idhabilidad, Descripcion from habilidad where idhabilidad = %s', (id))
    dato=cursor.fetchall()
    return render_template("edi_habilidad.html", habilidad = dato[0])

@app.route('/modifica_habilidad/<string:id>', methods=['POST'])
def modifica_habilidad(id):
    if request.method == 'POST':
        descrip=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('update habilidad set  Descripcion=%s where idhabilidad=%s',(descrip,id))
        conn.commit()
    return redirect(url_for('habilidad'))

@app.route('/bo_habilidad/<string:id>')
def bo_habilidad(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from habilidad where idhabilidad = {0}'.format(id))
    conn.commit()
    return redirect(url_for('habilidad'))

#------------------------------- solicitud -------------------------------------------------
@app.route('/solicitud')
def solicitud():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '   
                    'from solicitud a, area b, puesto c, estatus_solicitud d '
                    'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud')

    datos=cursor.fetchall()
    return render_template("solicitud.html", solicitudes = datos )

@app.route('/nvo_solicitud')
def nvo_solicitud():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idArea, AreaNombre  from  area')
    datos=cursor.fetchall()
    cursor.execute('select idPuesto, Descripcion  from  puesto')
    datos1=cursor.fetchall()
    cursor.execute('select idNivelAcademico, Descripcion  from  nivelacademico')
    datos2=cursor.fetchall()
    cursor.execute('select idCarrera, Descripcion  from  carrera')
    datos3=cursor.fetchall()

    return render_template("agr_solicitud.html", areas = datos, puestos=datos1, niveles=datos2, carreras=datos3)


@app.route('/agrega_solicitud', methods=['POST'])
def agrega_solicitud():
    if request.method == 'POST':
        aux_fec = request.form['fecha']
        aux_are = request.form['area_sol']
        aux_pue = request.form['Puesto_sol']
        aux_niv = request.form['Nivel_sol']
        aux_car = request.form['Carrera_sol']
        aux_vac = request.form['Vacantes_sol']


        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()

        #---------- estatus de la solicitud 1 pendeiente de aprobación, 2 Aprobada (si el puesto no requiere de aprobación)
        cursor.execute('select Aprobacion from puesto where idPuesto= %s', (aux_pue))
        req_ap= cursor.fetchone()

        if req_ap[0]==0:
            # el puesto requiere de autorización
            cursor.execute('insert into solicitud (FechaSolicitud, idArea, idPuesto, idNivelAcademico, idCarrera, NumeroVacante, idEstatus_Solicitud) '
                       'values (%s,%s,%s,%s,%s,%s,1)',(aux_fec,aux_are,aux_pue,aux_niv,aux_car,aux_vac))
        else:
            # el puesto NO requiere de autorización
            cursor.execute(
                'insert into solicitud (FechaSolicitud, idArea, idPuesto, idNivelAcademico, idCarrera, NumeroVacante, idEstatus_Solicitud) '
                'values (%s,%s,%s,%s,%s,%s,2)', (aux_fec, aux_are, aux_pue, aux_niv, aux_car, aux_vac))
        # --------------------------------------)
        conn.commit()

        cursor.execute(
            'select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante '
            'from solicitud a, area b, puesto c '
            'where b.idArea=a.idArea and c.idPuesto=a.idPuesto')
        cursor.execute(
            'select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
            'from solicitud a, area b, puesto c, estatus_solicitud d '
            'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud')

        datos = cursor.fetchall()
    return render_template("solicitud.html", solicitudes=datos)

@app.route('/ed_solicitud/<string:id>')
def ed_solicitud(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idSolicitud, FechaSolicitud, NumeroVacante, idArea, idPuesto, idNivelAcademico, idCarrera, idEstatus_Solicitud '   
                    'from solicitud  where idSolicitud=%s', (id))
    datos=cursor.fetchall()

    cursor.execute('select idArea, AreaNombre  from  area')
    datos1=cursor.fetchall()
    cursor.execute('select idPuesto, Descripcion  from  puesto')
    datos2=cursor.fetchall()
    cursor.execute('select idNivelAcademico, Descripcion  from  nivelacademico')
    datos3=cursor.fetchall()
    cursor.execute('select idCarrera, Descripcion  from  carrera')
    datos4=cursor.fetchall()
    cursor.execute('select idEstatus_Solicitud, Descripcion  from  estatus_solicitud')
    datos5=cursor.fetchall()
    return render_template("edi_solicitud.html", solicitud=datos, areas = datos1, puestos=datos2, niveles=datos3, carreras=datos4, estatus=datos5)


@app.route('/modifica_solicitud/<string:id>', methods=['POST'])
def modifica_solicitud(id):
    if request.method == 'POST':
        aux_fec = request.form['fecha']
        aux_are = request.form['area_sol']
        aux_pue = request.form['Puesto_sol']
        aux_niv = request.form['Nivel_sol']
        aux_car = request.form['Carrera_sol']
        aux_vac = request.form['Vacantes_sol']
        aux_est = request.form['Estatus_sol']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        #------------------------------------------------------------------------------------------------------
        cursor.execute('update solicitud set FechaSolicitud=%s, NumeroVacante=%s, idArea=%s,'
                       ' idPuesto=%s, idNivelAcademico=%s, idCarrera=%s, idEstatus_Solicitud=%s '
                       ' where idSolicitud=%s',(aux_fec, aux_vac, aux_are, aux_pue, aux_niv, aux_car, aux_est, id ))
        conn.commit()
        cursor.execute(
            'select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
            'from solicitud a, area b, puesto c, estatus_solicitud d '
            'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud')

        datos=cursor.fetchall()
    return render_template("solicitud.html", solicitudes = datos )

@app.route('/bo_solicitud/<string:id>')
def bo_solicitud(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from solicitud where idsolicitud = {0}'.format(id))
    conn.commit()
    #-----------------------------------------------------------------------
    cursor.execute(
        'select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        'from solicitud a, area b, puesto c, estatus_solicitud d '
        'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud')

    datos = cursor.fetchall()
    return render_template("solicitud.html", solicitudes = datos )

#------------------------------- autorización de la solicitud -------------------------------------------------
@app.route('/autoriza')
def autoriza():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '   
                    'from solicitud a, area b, puesto c, estatus_solicitud d '
                    'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud')

    datos=cursor.fetchall()
    return render_template("autoriza_solicitud.html", solicitudes = datos )

@app.route('/aut_solicitud/<string:id>')
def aut_solicitud(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('update solicitud set idEstatus_Solicitud=2 where idSolicitud=%s',(id ))
    conn.commit()
    cursor.execute(
        'select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        'from solicitud a, area b, puesto c, estatus_solicitud d '
        'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud')
    datos=cursor.fetchall()
    return render_template("autoriza_solicitud.html", solicitudes = datos )

@app.route('/can_solicitud/<string:id>')
def can_solicitud(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('update solicitud set idEstatus_Solicitud=6 where idSolicitud=%s',(id ))
    conn.commit()
    cursor.execute(
        'select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        'from solicitud a, area b, puesto c, estatus_solicitud d '
        'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud')
    datos=cursor.fetchall()
    return render_template("autoriza_solicitud.html", solicitudes = datos )


#------------------------------- publicación de la solicitud -------------------------------------------------
@app.route('/a_publicar')
def a_publicar():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '   
                    'from solicitud a, area b, puesto c, estatus_solicitud d '
                    'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
                    ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3)')

    datos=cursor.fetchall()
    return render_template("publicacion.html", solicitudes = datos )

@app.route('/crea_pub/<string:id>')
def crea_pub(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute(
        'select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        'from solicitud a, area b, puesto c, estatus_solicitud d '
        'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3) and idSolicitud=%s',(id))

    dato = cursor.fetchone()
    cursor.execute(
        'SELECT a.idAnuncio, a.Num_Solicitantes, a.FechaPublicacion, a.FechaCierre, b.Nombre, c.Descripcion '
        'from anuncio a, contacto b, mediopublicidad c '
        'where b.idcontacto=a.idcontacto and c.idMedioPublicidad=a.idMedioPublicidad and a.idSolicitud=%s',(id))

    datos = cursor.fetchall()

    cursor.execute('select idcontacto, nombre from contacto order by nombre')
    datos1 = cursor.fetchall()
    cursor.execute('select idMedioPublicidad, Descripcion from mediopublicidad order by Descripcion')
    datos2 = cursor.fetchall()
    return render_template("crea_publicacion.html", sol=dato, publicaciones=datos, contactos=datos1, medios=datos2)

@app.route('/agrega_publicacion', methods=['POST'])
def agrega_publicacion():
    if request.method == 'POST':
        aux_sol = request.form['n_solicitud']
        aux_fep = request.form['fecha_pub']
        aux_fec = request.form['fecha_cie']
        aux_solicitantes = request.form['n_solitantes']
        aux_con = request.form['contacto']
        aux_med = request.form['medio']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()

        # el puesto requiere de autorización
        cursor.execute('insert into anuncio (idSolicitud, Num_Solicitantes, FechaPublicacion, FechaCierre, idContacto, idMedioPublicidad) '
                   'values (%s,%s,%s,%s,%s,%s)',(aux_sol,aux_solicitantes,aux_fep,aux_fec, aux_con, aux_med))
        conn.commit()
        cursor.execute('update solicitud set idEstatus_Solicitud=3 where idSolicitud=%s', (aux_sol))
        conn.commit()
        cursor.execute(
                'select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
                'from solicitud a, area b, puesto c, estatus_solicitud d '
                'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
                ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3) and idSolicitud=%s', (aux_sol))
        dato = cursor.fetchone()
        cursor.execute(
                'SELECT a.idAnuncio, a.Num_Solicitantes, a.FechaPublicacion, a.FechaCierre, b.Nombre, c.Descripcion '
                'from anuncio a, contacto b, mediopublicidad c '
                'where b.idcontacto=a.idcontacto and c.idMedioPublicidad=a.idMedioPublicidad and a.idSolicitud=%s', (aux_sol))
        datos = cursor.fetchall()
        cursor.execute('select idcontacto, nombre from contacto order by nombre')
        datos1 = cursor.fetchall()
        cursor.execute('select idMedioPublicidad, Descripcion from mediopublicidad order by Descripcion')
        datos2 = cursor.fetchall()
    return render_template("crea_publicacion.html", sol=dato, publicaciones=datos, contactos=datos1, medios=datos2)


@app.route('/bo_publicacion/<string:id>')
def bo_publicacion(id):

    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idSolicitud from anuncio where idanuncio = {0}'.format(id))
    aux_sol=cursor.fetchone()
    cursor.execute('delete from anuncio where idanuncio = {0}'.format(id))
    conn.commit()
    cursor.execute(
        'select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        'from solicitud a, area b, puesto c, estatus_solicitud d '
        'where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3) and idSolicitud=%s',(aux_sol[0]))
    dato = cursor.fetchone()
    cursor.execute(
        'SELECT a.idAnuncio, a.Num_Solicitantes, a.FechaPublicacion, a.FechaCierre, b.Nombre, c.Descripcion '
        'from anuncio a, contacto b, mediopublicidad c '
        'where b.idcontacto=a.idcontacto and c.idMedioPublicidad=a.idMedioPublicidad and a.idSolicitud=%s',(aux_sol[0]))

    datos = cursor.fetchall()
    cursor.execute('select idcontacto, nombre from contacto order by nombre')
    datos1 = cursor.fetchall()
    cursor.execute('select idMedioPublicidad, Descripcion from mediopublicidad order by Descripcion')
    datos2 = cursor.fetchall()
    return render_template("crea_publicacion.html", sol=dato, publicaciones=datos, contactos=datos1, medios=datos2)


#------------------------------- candidato -------------------------------------------------
@app.route('/candidato')
def candidato():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select Curp, Nombre from candidato order by Nombre')
    datos=cursor.fetchall()
    return render_template("candidato.html", candidatos = datos )


@app.route('/nvo_candidato')
def nvo_candidato():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select idEstadoCivil, Descripcion  from  estadocivil')
    datos = cursor.fetchall()
    return render_template("agr_candidato.html", ecivil=datos)


@app.route('/agrega_candidato', methods=['POST'])
def agrega_candidato():
    if request.method == 'POST':
        aux_cur =request.form['curp']
        aux_nom = request.form['nombre']
        aux_dom = request.form['domicilio']
        aux_tel = request.form['telefono']
        aux_cor = request.form['correoe']
        aux_eda = request.form['edad']
        aux_nss = request.form['nss']
        aux_sex = request.form['sexo']
        aux_eci = request.form['edociv']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into candidato (Curp, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS,idEstadoCivil)'
                       ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(aux_cur, aux_nom, aux_dom, aux_tel, aux_cor, aux_sex, aux_eda, aux_nss, aux_eci ))
        conn.commit()
        # --------   Candidato
        cursor.execute('select Curp, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil '
                       'from  candidato where curp=%s',(aux_cur))
        datos=cursor.fetchall()
        # --------   Habilidad-CAndidato
        cursor.execute('select a.Curp, b.idHabilidad,b.Descripcion,c.Curp, c.idHabilidad, c.Experiencia '
                       ' from  candidato a, habilidad b,candidato_has_habilidad c '
                       ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(aux_cur))
        datos1 = cursor.fetchall()
        # --------   Idioma-Candidato
        cursor.execute('select a.Curp, b.idIdioma,b.Lenguaje,c.Curp, c.idIdioma, c.Nivel '
                       'from  candidato a, idioma b,candidato_has_idioma c '
                       'where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(aux_cur))
        datos2=cursor.fetchall()
        #---------    Catalogo de habilidades
        cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()
        # ---------    Catalogo de idiomas
        cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()
        # ---------    Catalogo de Estados civiles
        cursor.execute('select idEstadoCivil, Descripcion  from  estadocivil')
        datos5 = cursor.fetchall()
        # --------   Nivel Academico-Candidato
        cursor.execute('select a.Curp, b.descripcion, c.descripcion, d.Curp, d.idNivelAcademico,d.idCarrera,d.Institucion  '
                       ' from  candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d '
                       ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s', (aux_cur))
        datos6 = cursor.fetchall()
        #---------    Catalogo de nivel Academico
        cursor.execute('select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()
        # ---------    Catalogo de carreras
        cursor.execute('select idCarrera, descripcion from carrera order by Descripcion')
        datos8 = cursor.fetchall()

    return render_template("edi_candidato.html", candidatos = datos, can_habs=datos1, can_idis=datos2, habs=datos3, idiomas=datos4, ecivil=datos5, can_nacas=datos6, nacas=datos7, carreras=datos8 )

@app.route('/modifica_candidato', methods=['POST'])
def modifica_candidato():
    if request.method == 'POST':
        aux_cur =request.form['curp']
        aux_nom = request.form['nombre']
        aux_dom = request.form['domicilio']
        aux_tel = request.form['telefono']
        aux_cor = request.form['correoe']
        aux_eda = request.form['edad']
        aux_nss = request.form['nss']
        aux_sex = request.form['sexo']
        aux_eci = request.form['edociv']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('update candidato set Curp=%s, Nombre=%s, Domicilio=%s, Telefono=%s, E_Mail=%s, Sexo=%s, Edad=%s, NSS=%s,idEstadoCivil=%s '
                       'where Curp=%s ',(aux_cur, aux_nom, aux_dom, aux_tel, aux_cor, aux_sex, aux_eda, aux_nss, aux_eci, aux_cur))
        conn.commit()

        cursor.execute('select Curp, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil '
                       'from  candidato where curp=%s',(aux_cur))
        datos=cursor.fetchall()

        cursor.execute('select a.Curp, b.idHabilidad,b.Descripcion,c.Curp, c.idHabilidad, c.Experiencia '
                       ' from  candidato a, habilidad b,candidato_has_habilidad c '
                       ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s',(aux_cur))
        datos1 = cursor.fetchall()

        cursor.execute('select a.Curp, b.idIdioma,b.Lenguaje,c.Curp, c.idIdioma, c.Nivel '
                       'from  candidato a, idioma b,candidato_has_idioma c '
                       'where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s',(aux_cur))
        datos2=cursor.fetchall()

        cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()
        cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()
        cursor.execute('select idEstadoCivil, Descripcion  from  estadocivil')
        datos5 = cursor.fetchall()
        # --------   Nivel Academico-Candidato
        cursor.execute(
            'select a.Curp, b.descripcion, c.descripcion, d.Curp, d.idNivelAcademico,d.idCarrera,d.Institucion  '
            ' from  candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d '
            ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
            (aux_cur))
        datos6 = cursor.fetchall()
        # ---------    Catalogo de nivel Academico
        cursor.execute('select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()
        # ---------    Catalogo de carreras
        cursor.execute('select idCarrera, descripcion from carrera order by Descripcion')
        datos8 = cursor.fetchall()


    return render_template("edi_candidato.html", candidatos = datos, can_habs=datos1, can_idis=datos2, habs=datos3, idiomas=datos4, ecivil=datos5, can_nacas=datos6, nacas=datos7, carreras=datos8 )



@app.route('/ed_candidato/<string:id>')
def ed_candidato(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor =  conn.cursor()
    cursor.execute('select Curp, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS, idEstadoCivil '
                   'from  candidato where curp=%s', (id))
    datos = cursor.fetchall()

    cursor.execute('select a.Curp, b.idHabilidad,b.Descripcion,c.Curp, c.idHabilidad, c.Experiencia '
                   ' from  candidato a, habilidad b,candidato_has_habilidad c '
                   ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (id))
    datos1 = cursor.fetchall()

    cursor.execute('select a.Curp, b.idIdioma,b.Lenguaje,c.Curp, c.idIdioma, c.Nivel '
                   'from  candidato a, idioma b,candidato_has_idioma c '
                   'where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (id))
    datos2 = cursor.fetchall()

    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    cursor.execute('select idEstadoCivil, Descripcion  from  estadocivil')
    datos5 = cursor.fetchall()
    # --------   Nivel Academico-Candidato
    cursor.execute('select a.Curp, b.descripcion, c.descripcion, d.Curp, d.idNivelAcademico,d.idCarrera,d.Institucion  '
                   ' from  candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d '
                   ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                   (id))
    datos6 = cursor.fetchall()
    # ---------    Catalogo de nivel Academico
    cursor.execute('select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
    datos7 = cursor.fetchall()
    # ---------    Catalogo de carreras
    cursor.execute('select idCarrera, descripcion from carrera order by Descripcion')
    datos8 = cursor.fetchall()


    return render_template("edi_candidato.html", candidatos=datos, can_habs=datos1, can_idis=datos2, habs=datos3,idiomas=datos4, ecivil=datos5, can_nacas=datos6, nacas=datos7, carreras=datos8 )

@app.route('/agrega_hab_can', methods=['POST'])
def agrega_hab_can():
    if request.method == 'POST':
        aux_cur=request.form['curph']
        aux_hab = request.form['habil']
        aux_exp = request.form['expe']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into candidato_has_habilidad (Curp, idHabilidad, Experiencia) values (%s,%s,%s)',(aux_cur,aux_hab,aux_exp))
        conn.commit()
        cursor.execute('select Curp, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS  from  candidato where curp=%s', (aux_cur))
        datos = cursor.fetchall()

        cursor.execute('select a.Curp, b.idHabilidad,b.Descripcion,c.Curp, c.idHabilidad, c.Experiencia '
               ' from  candidato a, habilidad b,candidato_has_habilidad c '
               ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (aux_cur))
        datos1 = cursor.fetchall()

        cursor.execute('select a.Curp, b.idIdioma,b.Lenguaje,c.Curp, c.idIdioma, c.Nivel '
               'from  candidato a, idioma b,candidato_has_idioma c '
               'where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (aux_cur))
        datos2 = cursor.fetchall()

        cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()
        cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()
        cursor.execute('select idEstadoCivil, Descripcion  from  estadocivil')
        datos5 = cursor.fetchall()
        # --------   Nivel Academico-Candidato
        cursor.execute('select a.Curp, b.descripcion, c.descripcion, d.Curp, d.idNivelAcademico,d.idCarrera,d.Institucion  '
                   ' from  candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d '
                   ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                   (aux_cur))
        datos6 = cursor.fetchall()
        # ---------    Catalogo de nivel Academico
        cursor.execute('select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()
        # ---------    Catalogo de carreras
        cursor.execute('select idCarrera, descripcion from carrera order by Descripcion')
        datos8 = cursor.fetchall()

    return render_template("edi_candidato.html", candidatos=datos, can_habs=datos1, can_idis=datos2, habs=datos3,idiomas=datos4, ecivil=datos5, can_nacas=datos6, nacas=datos7, carreras=datos8 )

@app.route('/agrega_idio_can', methods=['POST'])
def agrega_idio_can():
    if request.method == 'POST':
        aux_cur =request.form['curpi']
        aux_idi = request.form['idio']
        aux_niv = request.form['nive']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into candidato_has_idioma (Curp, idIdioma, Nivel) values (%s,%s,%s)',(aux_cur,aux_idi,aux_niv))
        conn.commit()
        cursor.execute('select Curp, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS  from  candidato where curp=%s', (aux_cur))
        datos = cursor.fetchall()

        cursor.execute('select a.Curp, b.idHabilidad,b.Descripcion,c.Curp, c.idHabilidad, c.Experiencia '
               ' from  candidato a, habilidad b,candidato_has_habilidad c '
               ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (aux_cur))
        datos1 = cursor.fetchall()

        cursor.execute('select a.Curp, b.idIdioma,b.Lenguaje,c.Curp, c.idIdioma, c.Nivel '
               'from  candidato a, idioma b,candidato_has_idioma c '
               'where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (aux_cur))
        datos2 = cursor.fetchall()

        cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()
        cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()
        cursor.execute('select idEstadoCivil, Descripcion  from  estadocivil')
        datos5 = cursor.fetchall()
        # --------   Nivel Academico-Candidato
        cursor.execute('select a.Curp, b.descripcion, c.descripcion, d.Curp, d.idNivelAcademico,d.idCarrera,d.Institucion  '
                   ' from  candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d '
                   ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                   (aux_cur))
        datos6 = cursor.fetchall()
        # ---------    Catalogo de nivel Academico
        cursor.execute('select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()
        # ---------    Catalogo de carreras
        cursor.execute('select idCarrera, descripcion from carrera order by Descripcion')
        datos8 = cursor.fetchall()

    return render_template("edi_candidato.html", candidatos=datos, can_habs=datos1, can_idis=datos2, habs=datos3,idiomas=datos4, ecivil=datos5, can_nacas=datos6, nacas=datos7, carreras=datos8 )


@app.route('/agrega_estudio_can', methods=['POST'])
def agrega_estudio_can():
    if request.method == 'POST':
        aux_cur =request.form['curpe']
        aux_niv = request.form['nivest']
        aux_car = request.form['carre']
        aux_ins = request.form['insti']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into candidato_has_nivelacademico (Curp, idNivelAcademico, idCarrera, Institucion) values (%s,%s,%s,%s)',(aux_cur,aux_niv,aux_car,aux_ins))
        conn.commit()
        cursor.execute('select Curp, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS  from  candidato where curp=%s', (aux_cur))
        datos = cursor.fetchall()

        cursor.execute('select a.Curp, b.idHabilidad,b.Descripcion,c.Curp, c.idHabilidad, c.Experiencia '
               ' from  candidato a, habilidad b,candidato_has_habilidad c '
               ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (aux_cur))
        datos1 = cursor.fetchall()

        cursor.execute('select a.Curp, b.idIdioma,b.Lenguaje,c.Curp, c.idIdioma, c.Nivel '
               'from  candidato a, idioma b,candidato_has_idioma c '
               'where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (aux_cur))
        datos2 = cursor.fetchall()

        cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()
        cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()
        cursor.execute('select idEstadoCivil, Descripcion  from  estadocivil')
        datos5 = cursor.fetchall()
        # --------   Nivel Academico-Candidato
        cursor.execute('select a.Curp, b.descripcion, c.descripcion, d.Curp, d.idNivelAcademico,d.idCarrera,d.Institucion  '
                   ' from  candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d '
                   ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                   (aux_cur))
        datos6 = cursor.fetchall()
        # ---------    Catalogo de nivel Academico
        cursor.execute('select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
        datos7 = cursor.fetchall()
        # ---------    Catalogo de carreras
        cursor.execute('select idCarrera, descripcion from carrera order by Descripcion')
        datos8 = cursor.fetchall()

    return render_template("edi_candidato.html", candidatos=datos, can_habs=datos1, can_idis=datos2, habs=datos3,idiomas=datos4, ecivil=datos5, can_nacas=datos6, nacas=datos7, carreras=datos8 )




@app.route('/bo_hab_can/<string:aux_cur>/<string:idH>')
def bo_hab_can(aux_cur,idH):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from candidato_has_habilidad where Curp =%s and idHabilidad=%s ',(aux_cur,idH))
    conn.commit()
    cursor.execute('select Curp, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS  from  candidato where curp=%s', (aux_cur))
    datos = cursor.fetchall()
    cursor.execute('select a.Curp, b.idHabilidad,b.Descripcion,c.Curp, c.idHabilidad, c.Experiencia '
          ' from  candidato a, habilidad b,candidato_has_habilidad c '
          ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (aux_cur))
    datos1 = cursor.fetchall()

    cursor.execute('select a.Curp, b.idIdioma,b.Lenguaje,c.Curp, c.idIdioma, c.Nivel '
           'from  candidato a, idioma b,candidato_has_idioma c '
           'where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (aux_cur))
    datos2 = cursor.fetchall()

    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    cursor.execute('select idEstadoCivil, Descripcion  from  estadocivil')
    datos5 = cursor.fetchall()
    # --------   Nivel Academico-Candidato
    cursor.execute('select a.Curp, b.descripcion, c.descripcion, d.Curp, d.idNivelAcademico,d.idCarrera,d.Institucion  '
                   ' from  candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d '
                   ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                   (aux_cur))
    datos6 = cursor.fetchall()
    # ---------    Catalogo de nivel Academico
    cursor.execute('select idNivelAc'
                   'ademico, Descripcion from nivelacademico order by Descripcion')
    datos7 = cursor.fetchall()
    # ---------    Catalogo de carreras
    cursor.execute('select idCarrera, descripcion from carrera order by Descripcion')
    datos8 = cursor.fetchall()
    return render_template("edi_candidato.html", candidatos=datos, can_habs=datos1, can_idis=datos2, habs=datos3,idiomas=datos4, ecivil=datos5, can_nacas=datos6, nacas=datos7, carreras=datos8 )


@app.route('/bo_idi_can/<string:aux_cur>/<string:idI>')
def bo_idi_can(aux_cur,idI):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from candidato_has_idioma where Curp =%s and idIdioma=%s ',(aux_cur,idI))
    conn.commit()
    cursor.execute('select Curp, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS  from  candidato where curp=%s', (aux_cur))
    datos = cursor.fetchall()
    cursor.execute('select a.Curp, b.idHabilidad,b.Descripcion,c.Curp, c.idHabilidad, c.Experiencia '
          ' from  candidato a, habilidad b,candidato_has_habilidad c '
          ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (aux_cur))
    datos1 = cursor.fetchall()

    cursor.execute('select a.Curp, b.idIdioma,b.Lenguaje,c.Curp, c.idIdioma, c.Nivel '
           'from  candidato a, idioma b,candidato_has_idioma c '
           'where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (aux_cur))
    datos2 = cursor.fetchall()

    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    cursor.execute('select idEstadoCivil, Descripcion  from  estadocivil')
    datos5 = cursor.fetchall()
    # --------   Nivel Academico-Candidato
    cursor.execute('select a.Curp, b.descripcion, c.descripcion, d.Curp, d.idNivelAcademico,d.idCarrera,d.Institucion  '
                   ' from  candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d '
                   ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',(aux_cur))
    datos6 = cursor.fetchall()
    # ---------    Catalogo de nivel Academico
    cursor.execute('select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
    datos7 = cursor.fetchall()
    # ---------    Catalogo de carreras
    cursor.execute('select idCarrera, descripcion from carrera order by Descripcion')
    datos8 = cursor.fetchall()

    return render_template("edi_candidato.html", candidatos=datos, can_habs=datos1, can_idis=datos2, habs=datos3,idiomas=datos4, ecivil=datos5, can_nacas=datos6, nacas=datos7, carreras=datos8 )

@app.route('/bo_est_can/<string:aux_cur>/<string:idN>/<string:idC>')
def bo_est_can(aux_cur,idN,idC):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from candidato_has_nivelacademico where Curp =%s and idNivelAcademico=%s and idCarrera=%s',(aux_cur,idN, idC))
    conn.commit()
    cursor.execute('select Curp, Nombre, Domicilio, Telefono, E_Mail, Sexo, Edad, NSS  from  candidato where curp=%s', (aux_cur))
    datos = cursor.fetchall()
    cursor.execute('select a.Curp, b.idHabilidad,b.Descripcion,c.Curp, c.idHabilidad, c.Experiencia '
          ' from  candidato a, habilidad b,candidato_has_habilidad c '
          ' where a.Curp=c.Curp and b.idHabilidad=c.idHabilidad and c.Curp=%s', (aux_cur))
    datos1 = cursor.fetchall()

    cursor.execute('select a.Curp, b.idIdioma,b.Lenguaje,c.Curp, c.idIdioma, c.Nivel '
           'from  candidato a, idioma b,candidato_has_idioma c '
           'where a.Curp=c.Curp and b.idIdioma=c.idIdioma and c.Curp=%s', (aux_cur))
    datos2 = cursor.fetchall()

    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    cursor.execute('select idEstadoCivil, Descripcion  from  estadocivil')
    datos5 = cursor.fetchall()
    # --------   Nivel Academico-Candidato
    cursor.execute('select a.Curp, b.descripcion, c.descripcion, d.Curp, d.idNivelAcademico,d.idCarrera,d.Institucion  '
                   ' from  candidato a, nivelacademico b, carrera c, candidato_has_nivelacademico d '
                   ' where a.Curp=d.Curp and b.idNivelAcademico=d.idNivelAcademico and c.idCarrera=d.idCarrera and d.Curp=%s',
                   (aux_cur))
    datos6 = cursor.fetchall()
    # ---------    Catalogo de nivel Academico
    cursor.execute('select idNivelAcademico, Descripcion from nivelacademico order by Descripcion')
    datos7 = cursor.fetchall()
    # ---------    Catalogo de carreras
    cursor.execute('select idCarrera, descripcion from carrera order by Descripcion')
    datos8 = cursor.fetchall()

    return render_template("edi_candidato.html", candidatos=datos, can_habs=datos1, can_idis=datos2, habs=datos3,idiomas=datos4, ecivil=datos5, can_nacas=datos6, nacas=datos7, carreras=datos8 )



@app.route('/bo_candidato/<string:aux_cur>')
def bo_candidato(aux_cur):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from candidato_has_Idioma where Curp = "{0}"'.format(aux_cur))
    conn.commit()
    cursor.execute('delete from candidato_has_habilidad where Curp = "{0}"'.format(aux_cur))
    conn.commit()
    cursor.execute('delete from candidato_has_nivelacademico where Curp = "{0}"'.format(aux_cur))
    conn.commit()
    cursor.execute('delete from candidato where Curp = "{0}"'.format(aux_cur))
    conn.commit()

    return redirect(url_for('candidato'))















#------------------------------- usuario -------------------------------------------------

@app.route('/usuario')
def usuario():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select a.usuario, a.nombre, b.descripcion from usuario a, perfil_admo b order by a.usuario')

    datos=cursor.fetchall()
    return render_template("usuario.html", usuarios = datos )

@app.route('/agrega_usuario', methods=['POST'])
def agrega_usuario():
    if request.method == 'POST':
        aux_cve =request.form['cve_usuario']
        aux_nom = request.form['nom_usuario']
        aux_pas = request.form['pass_usuario']
        aux_per = request.form['per_usuario']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into usuario (usuario, nombre, password, id_perfil) values (%s,%s,%s,%s)',(aux_cve,aux_nom,aux_pas,aux_per))
        conn.commit()

    return redirect(url_for('usuario'))


@app.route('/nvo_usuario')
def nvo_usuario():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select id_perfil, Descripcion from perfil_admo order by Descripcion')
    datos = cursor.fetchall()
    return render_template("agr_usuario.html", perfiles=datos)

@app.route('/modifica_usuario/<string:id>', methods=['POST'])
def modifica_usuario(id):
    if request.method == 'POST':
        aux_cve =request.form['cve_usuario']
        aux_nom = request.form['nom_usuario']
        aux_pas = request.form['pass_usuario']
        aux_per = request.form['per_usuario']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('update usuario set usuario=%s, nombre=%s, password=%s, id_perfil=%s where idpuesto=%s', (aux_cve, aux_nom,aux_pas, aux_per,id))
        conn.commit()
    return redirect(url_for('usuario'))

@app.route('/ed_usuario/<string:id>')
def ed_usuario(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select id_perfil, Descripcion from perfil_admo order by Descripcion')
    datos = cursor.fetchall()
    return render_template("agr_usuario.html", perfiles=datos)
    return render_template("edi_puesto.html", puestos = datos, pue_habs=datos1, pue_idis=datos2, habs=datos3, idiomas=datos4 )

@app.route('/bo_usuario/<string:id>')
def bo_usuario(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from puesto_has_Idioma where idPuesto = {0}'.format(id))
    conn.commit()
    cursor.execute('delete from puesto_has_habilidad where idPuesto = {0}'.format(id))
    conn.commit()
    cursor.execute('delete from puesto where idPuesto = {0}'.format(id))
    conn.commit()

    return redirect(url_for('puesto'))



@app.route('/agrega_proc_usuario', methods=['POST'])
def agrega_proc_usuario():
    if request.method == 'POST':
        aux_pto=request.form['pto']
        aux_hab = request.form['habil']
        aux_exp = request.form['expe']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into puesto_has_habilidad (idPuesto, idHabilidad, Experiencia) values (%s,%s,%s)',(aux_pto,aux_hab,aux_exp))
        conn.commit()

        cursor.execute('select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion '
                       'from  puesto where idPuesto=%s', (aux_pto))
        datos = cursor.fetchall()
        cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
                       ' from  puesto a, habilidad b,puesto_has_habilidad c '
                       ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s', (aux_pto))
        datos1 = cursor.fetchall()
        cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
                       'from  puesto a, idioma b,puesto_has_idioma c '
                       'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s', (aux_pto))
        datos2 = cursor.fetchall()
        cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()
        cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()
    return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3, idiomas=datos4)


@app.route('/bo_proc_usuario/<string:idP>/<string:idH>')
def bo_proc_usuario(idP,idH):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('delete from puesto_has_habilidad where idPuesto =%s and idHabilidad=%s ',(idP,idH))
    conn.commit()


    cursor.execute('select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion '
                   'from  puesto where idPuesto=%s', (idP))
    datos = cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
                   ' from  puesto a, habilidad b,puesto_has_habilidad c '
                   ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s', (idP))
    datos1 = cursor.fetchall()
    cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
                   'from  puesto a, idioma b,puesto_has_idioma c '
                   'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s', (idP))
    datos2 = cursor.fetchall()
    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3, idiomas=datos4)



#----------------------------------------------------------------------------------------------------------------------------------------




#------------------------------- perfil -------------------------------------------------
@app.route('/perfil')
def perfil():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
    cursor = conn.cursor()
    cursor.execute('select id_perfil, Descripcion from perfil_admo order by Descripcion')
    datos=cursor.fetchall()
    return render_template("perfil.html", perfiles = datos )


@app.route('/nvo_perfil')
def nvo_perfil():
    return render_template("agr_perfil.html")


@app.route('/agrega_perfil', methods=['POST'])
def agrega_perfil():
    if request.method == 'POST':
        aux_des =request.form['descripcion']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into perfil_admo (Descripcion) values (%s)',(aux_des))
        conn.commit()

        cursor.execute('select id_perfil, Descripcion from   perfil_admo where id_Perfil=(select max(id_perfil) from perfil_admo)')
        datos=cursor.fetchall()

        cursor.execute('select a.id_perfil, b.id_proceso,b.Descripcion,c.id_perfil, c.id_proceso, c.id_permiso '
                       ' from   perfil_admo a, proceso b,perfil_has_proceso c '
                       ' where a.id_perfil=c.id_perfil and b.id_proceso=c.id_proceso and c.id_perfil=(select max(id_perfil) from perfil_admo)')
        datos1 = cursor.fetchall()


        cursor.execute('select id_proceso, Descripcion from proceso order by Descripcion')
        datos2 = cursor.fetchall()

        cursor.execute('select id_permiso, Descripcion from permisos order by Descripcion')
        datos3 = cursor.fetchall()
    return render_template("edi_perfil.html", perfiles = datos, per_proc=datos1, procesos=datos2, permisos=datos3 )

@app.route('/agrega_proceso_perfil', methods=['POST'])
def agrega_proceso_perfil():
    if request.method == 'POST':
        aux_per = request.form['per']
        aux_pro = request.form['proceso']
        aux_perm = request.form['permiso']

        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rhumanos')
        cursor = conn.cursor()
        cursor.execute('insert into perfil_has_proceso (id_perfil, id_proceso, id_permiso) values (%s,%s,%s)',(aux_per,aux_pro,aux_perm))
        conn.commit()

        cursor.execute('select id_perfil, Descripcion from   perfil_admo where id_Perfil=%s',(aux_per))
        datos=cursor.fetchall()

        cursor.execute('select a.id_perfil, b.id_proceso,b.Descripcion,c.id_perfil, c.id_proceso, c.id_permiso '
                       ' from   perfil_admo a, proceso b,perfil_has_proceso c '
                       ' where a.id_perfil=c.id_perfil and b.id_proceso=c.id_proceso and c.id_perfil=%s',(aux_per))
        datos1 = cursor.fetchall()


        cursor.execute('select id_proceso, Descripcion from proceso order by Descripcion')
        datos2 = cursor.fetchall()

        cursor.execute('select id_permiso, Descripcion from permisos order by Descripcion')
        datos3 = cursor.fetchall()
    return render_template("edi_perfil.html", perfiles = datos, per_proc=datos1, procesos=datos2, permisos=datos3 )



















@app.route('/archivos')
def archivos():
    return render_template("archivos.html")

@app.route('/sube_archivo', methods=['POST'])
def sube_archivo():
    if request.method == 'POST':
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio "Archivos PDF"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Retornamos una respuesta satisfactoria#

    return render_template("abrir_archivo.html", file_a=filename)




if __name__ == "__main__":
    app.run(port=3000, debug=True)