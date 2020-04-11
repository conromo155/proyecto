from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql


app = Flask(__name__)

# sesion
app.secret_key = 'mysecretkey'


@app.route('/')
def home():
	return render_template("home.html")



#------------------------------- nivel -------------------------------------------------
@app.route('/nivel')
def nivel():
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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

		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
		cursor = conn.cursor()
		cursor.execute('insert into nivelacademico (Descripcion) values (%s)',(aux_Descripcion))
		conn.commit()
	return redirect(url_for('nivel'))


@app.route('/ed_nivel/<string:id>')
def ed_nivel(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('select idNivelAcademico, Descripcion from nivelacademico where idNivelAcademico = %s', (id))
	dato=cursor.fetchall()
	return render_template("edi_nivel.html", nivel = dato[0])

@app.route('/modifica_nivel/<string:id>', methods=['POST'])
def modifica_nivel(id):
	if request.method == 'POST':
		descrip=request.form['descripcion']
		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
		cursor = conn.cursor()
		cursor.execute('update nivelacademico set  Descripcion=%s where idNivelAcademico=%s',(descrip,id))
		conn.commit()
	return redirect(url_for('nivel'))

@app.route('/bo_nivel/<string:id>')
def bo_nivel(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('delete from nivelacademico where idNivelAcademico = {0}'.format(id))
	conn.commit()
	return redirect(url_for('nivel'))


#------------------------------- carrera -------------------------------------------------
@app.route('/carrera')
def carrera():
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('select idCarrera, Descripcion from carrera order by Descripcion')
	datos=cursor.fetchall()
	return render_template("carrera.html", carreras = datos )

@app.route('/agrega_carrera', methods=['POST'])
def agrega_carrera():
	if request.method == 'POST':
		aux_Descripcion=request.form['descripcion']
		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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
		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
		cursor = conn.cursor()
		cursor.execute('update carrera set  Descripcion=%s where idCarrera=%s',(descrip,id))
		conn.commit()
	return redirect(url_for('carrera'))

@app.route('/ed_carrera/<string:id>')
def ed_carrera(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('select idCarrera, Descripcion from carrera where idCarrera = %s', (id))
	dato=cursor.fetchall()
	return render_template("edi_carrera.html", carrera = dato[0])



@app.route('/bo_carrera/<string:id>')
def bo_carrera(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('delete from carrera where idCarrera = {0}'.format(id))
	conn.commit()
	return redirect(url_for('carrera'))


#------------------------------- idioma -------------------------------------------------
@app.route('/idioma')
def idioma():
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('select idIdioma, lenguaje from idioma order by lenguaje')
	datos=cursor.fetchall()
	return render_template("idioma.html", idiomas = datos )

@app.route('/agrega_idioma', methods=['POST'])
def agrega_idioma():
	if request.method == 'POST':
		aux_Descripcion=request.form['descripcion']
		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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
		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
		cursor = conn.cursor()
		cursor.execute('update idioma set  lenguaje=%s where idIdioma=%s',(descrip,id))
		conn.commit()
	return redirect(url_for('idioma'))

@app.route('/ed_idioma/<string:id>')
def ed_idioma(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('select idIdioma, lenguaje from idioma where idIdioma = %s', (id))
	dato=cursor.fetchall()
	return render_template("edi_idioma.html", idioma = dato[0])



@app.route('/bo_idioma/<string:id>')
def bo_idioma(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('delete from idioma where idIdioma = {0}'.format(id))
	conn.commit()
	return redirect(url_for('idioma'))

#------------------------------- puesto -------------------------------------------------
@app.route('/puesto')
def puesto():
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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

		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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

		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
		cursor = conn.cursor()
		cursor.execute('update puesto set Descripcion=%s, SalarioAnual=%s, Beneficios=%s, Bonos=%s, Aprobacion=%s where idpuesto=%s', (aux_des, aux_sal,aux_ben, aux_bon, aux_aut,id))
		conn.commit()
	return redirect(url_for('puesto'))

@app.route('/ed_puesto/<string:id>')
def ed_puesto(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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

		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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

		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('select idMedioPublicidad, Descripcion from mediopublicidad order by descripcion')
	datos=cursor.fetchall()
	return render_template("medio.html", medios = datos )

@app.route('/agrega_medio', methods=['POST'])
def agrega_medio():
	if request.method == 'POST':
		aux_Descripcion=request.form['descripcion']
		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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
		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
		cursor = conn.cursor()
		cursor.execute('update mediopublicidad set  descripcion=%s where idMedioPublicidad=%s',(descrip,id))
		conn.commit()
	return redirect(url_for('medio'))

@app.route('/ed_medio/<string:id>')
def ed_medio(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('select idMedioPublicidad, Descripcion from mediopublicidad where idMedioPublicidad = %s', (id))
	dato=cursor.fetchall()
	return render_template("edi_medio.html", medio = dato[0])


@app.route('/bo_medio/<string:id>')
def bo_medio(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('delete from mediopublicidad where idMedioPublicidad = {0}'.format(id))
	conn.commit()
	return redirect(url_for('medio'))


#------------------------------- contacto -------------------------------------------------
@app.route('/contacto')
def contacto():
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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
		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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
		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
		cursor = conn.cursor()
		cursor.execute('update contacto set Nombre=%s,Domicilio=%s,Razon_social=%s,Telefono=%s where idContacto=%s',(aux_nom, aux_dom,aux_raz, aux_tel,id))
		conn.commit()
	return redirect(url_for('contacto'))

@app.route('/ed_contacto/<string:id>')
def ed_contacto(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('select idContacto, Nombre, Domicilio, Razon_social, telefono from contacto where idContacto = %s', (id))
	dato=cursor.fetchall()
	return render_template("edi_contacto.html", contacto = dato[0])



@app.route('/bo_contacto/<string:id>')
def bo_contacto(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('delete from contacto where idContacto = {0}'.format(id))
	conn.commit()
	return redirect(url_for('contacto'))

#------------------------------- contacto -------------------------------------------------
@app.route('/empresa')
def empresa():
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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
		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
		cursor = conn.cursor()
		cursor.execute(''
		'update datos_de_empresa set Nombre_de_empresa=%s, Descripcion=%s, telefono=%s, domicilio=%s, E_mail=%s, RazonSocial=%s' 
		', Estructura_Juridica=%s, Encargado=%s, CIF_Empresa=%s',(aux_nom,aux_des,aux_tel,aux_dom,aux_cor,aux_raz,aux_est,aux_enc,aux_cif))
		conn.commit()
	return redirect(url_for('empresa'))

@app.route('/ed_empresa/<string:id>')
def ed_empresa(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute(''
				   'SELECT idEmpresa, Nombre_de_empresa, Descripcion, telefono, domicilio, E_mail, RazonSocial, Estructura_Juridica'
				   ', Encargado, CIF_Empresa FROM datos_de_empresa ORDER BY nombre_de_empresa')

	dato=cursor.fetchall()
	return render_template("edi_empresa.html", empresa = dato[0])


#------------------------------- habilidad -------------------------------------------------
@app.route('/habilidad')
def habilidad():
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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

		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
		cursor = conn.cursor()
		cursor.execute('insert into habilidad (Descripcion) values (%s)',(aux_Descripcion))
		conn.commit()
	return redirect(url_for('habilidad'))


@app.route('/ed_habilidad/<string:id>')
def ed_habilidad(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('select idhabilidad, Descripcion from habilidad where idhabilidad = %s', (id))
	dato=cursor.fetchall()
	return render_template("edi_habilidad.html", habilidad = dato[0])

@app.route('/modifica_habilidad/<string:id>', methods=['POST'])
def modifica_habilidad(id):
	if request.method == 'POST':
		descrip=request.form['descripcion']
		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
		cursor = conn.cursor()
		cursor.execute('update habilidad set  Descripcion=%s where idhabilidad=%s',(descrip,id))
		conn.commit()
	return redirect(url_for('habilidad'))

@app.route('/bo_habilidad/<string:id>')
def bo_habilidad(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('delete from habilidad where idhabilidad = {0}'.format(id))
	conn.commit()
	return redirect(url_for('habilidad'))

#------------------------------- puesto -------------------------------------------------
@app.route('/solicitud')
def solicitud():
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante '   
                    'from solicitud a, area b, puesto c '
                    'where b.idArea=a.idArea and c.idPuesto=a.idPuesto')

	datos=cursor.fetchall()
	return render_template("solicitud.html", solicitudes = datos )

@app.route('/nvo_solicitud')
def nvo_solicitud():
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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

		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
		cursor = conn.cursor()
		cursor.execute('insert into solicitud (FechaSolicitud, idArea, idPuesto, idNivelAcademico, idCarrera, NumeroVacante, idEstatus_Solicitud) '
					   'values (%s,%s,%s,%s,%s,%s,1)',(aux_fec,aux_are,aux_pue,aux_niv,aux_car,aux_vac))
		conn.commit()

		cursor.execute(
			'select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante '
			'from solicitud a, area b, puesto c '
			'where b.idArea=a.idArea and c.idPuesto=a.idPuesto')

		datos = cursor.fetchall()
	return render_template("solicitud.html", solicitudes=datos)

@app.route('/ed_solicitud/<string:id>')
def ed_solicitud(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
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

		conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
		cursor = conn.cursor()
		cursor.execute('update solicitud set FechaSolicitud=%s, NumeroVacante=%s, idArea=%s,'
					   ' idPuesto=%s, idNivelAcademico=%s, idCarrera=%s, idEstatus_Solicitud=%s '
					   ' where idSolicitud=%s',(aux_fec, aux_vac, aux_are, aux_pue, aux_niv, aux_car, aux_est, id ))
		conn.commit()
		cursor.execute('select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante '   
                    'from solicitud a, area b, puesto c '
                    'where b.idArea=a.idArea and c.idPuesto=a.idPuesto')

		datos=cursor.fetchall()
	return render_template("solicitud.html", solicitudes = datos )

@app.route('/bo_solicitud/<string:id>')
def bo_solicitud(id):
	conn = pymysql.connect(host='localhost', user='root', passwd='desarrollo', db='r_humanos')
	cursor = conn.cursor()
	cursor.execute('delete from solicitud where idsolicitud = {0}'.format(id))
	conn.commit()
	cursor.execute(
		'select a.idSolicitud,a.FechaSolicitud,a.idArea,b.AreaNombre,a.idPuesto,c.Descripcion, a.NumeroVacante '
		'from solicitud a, area b, puesto c '
		'where b.idArea=a.idArea and c.idPuesto=a.idPuesto')

	datos = cursor.fetchall()
	return render_template("solicitud.html", solicitudes = datos )

if __name__ == "__main__":
	app.run()