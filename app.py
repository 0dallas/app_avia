from flask import Flask, jsonify, request, render_template,redirect,url_for,flash,session

import pandas as pd
from datetime import datetime
import joblib
import csv

from func import enviar_email,generar_codigo, existe_usuario_correo, consultar_contra, guardar_usuario,modificar_password,guardar_data,es_correo_valido

pipeline = joblib.load('model_pipeline.pkl')


def predecir(data):
    prediction = pipeline.predict_proba(data)[:, 1][0].tolist()
    if prediction >= 0.05:
        prediction = 'POSITIVO'
    else:
        prediction = 'NEGATIVO'
    return prediction


app = Flask(__name__)

app.secret_key = 'secret'

mail = ''
cod = ''
user_global = ''
df = pd.DataFrame([{'user':'init'}])


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
        if consultar_contra(username,password):
            session['logged_in'] = True
            # flash('Login exitoso', 'success')
            global user_global
            user_global = username
            return redirect(url_for('formulario'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')


@app.route('/recuperar',methods=['GET','POST'])
def recuperar():
    codigo=""
    if request.method == 'POST':
        try:
            correo = request.form['correo']
            if existe_usuario_correo('dfpdspfñlvkdskfiweifekdvsdl',correo):   
                global mail
                mail = correo
                global cod
                cod = generar_codigo()
                enviar_email(mail,cod)
                return render_template("codigo.html",correo=correo)
            else: 
                pass
        except:
            pass
        try:
            codigo = request.form['codigo']
            if codigo == cod:  
                return render_template("nuevac.html")
            else:
                flash('Usuario o contraseña incorrectos', 'danger')       
        except:
                pass  
        try:
            cont_1 = request.form['password1']
            cont_2 = request.form['password2']
            codigo = 'x'
            if cont_1 == cont_2:
                modificar_password(mail,cont_1)
                return redirect(url_for('login'))
            else:
                flash('Las contraseñas no son iguales', 'danger')   
        except:
            pass

    if codigo == '':
        return render_template("recuperar.html")
    elif codigo == 'x':
        return render_template("nuevac.html")
    else:
        return render_template("codigo.html",correo=mail)   
    

@app.route('/registrar',methods=['GET','POST'])
def registrar():
    if request.method == 'POST':
        usuario = request.form['user']
        contra1 = request.form['contra1']
        contra2 = request.form['contra2']
        correo = request.form['correo']
        if existe_usuario_correo(usuario,correo):
            flash('El usuario y/o contraseña ya existe!', 'danger')  
        elif es_correo_valido(correo) == None:
            flash('Correo no válido') 
        elif contra1 == contra2:
            guardar_usuario(usuario,contra1,correo,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            return redirect(url_for('login'))
        else:
            flash('Las contraseñas no son iguales', 'danger')  

    return render_template("registrar.html")


def calcular_fragilidad(form_data):
    # Inicializar variable 'fragil' en 0
    fragil = 0
    # Sumar 1 si la respuesta de fatigabilidad es "todo" o "mayor_parte"
    fragil += 1 if form_data.get('fatigabilidad') in ['todo', 'mayor_parte'] else 0
    # Sumar 1 si la respuesta de resistencia es "si"
    fragil += 1 if form_data.get('resistencia') == 'si' else 0
    # Sumar 1 si la respuesta de deambulación es "si"
    fragil += 1 if form_data.get('deambulacion') == 'si' else 0
    # Sumar 1 si hay entre 5 y 11 comorbilidades seleccionadas
    fragil += 1 if 5 <= len(form_data.getlist('comorbilidad')) <= 11 else 0
    # Sumar 1 si la respuesta de pérdida de peso es "si"
    fragil += 1 if form_data.get('perdida_peso') == 'si' else 0
    return fragil


# Cargar las recomendaciones y servicios desde el archivo CSV
recomendaciones_df = pd.read_csv('recomendaciones.csv')


def generar_informe(datos_respuesta):
    recomendaciones = []
    servicios = []

    # Condiciones para las recomendaciones y servicios
    if datos_respuesta.get('fuma') == 'si':
        recomendaciones.append(recomendaciones_df.loc[0, 'Recomendaciones'])
        # servicios.append(recomendaciones_df.loc[0, 'Servicios'])
    if datos_respuesta.get('alcohol') in ['1', '2', '3']:
        recomendaciones.append(recomendaciones_df.loc[1, 'Recomendaciones'])
        # servicios.append(recomendaciones_df.loc[1, 'Servicios'])
    if datos_respuesta.get('diabetes') == 'si':
        recomendaciones.append(recomendaciones_df.loc[8, 'Recomendaciones'])  # Cambiado a 8
        # servicios.append(recomendaciones_df.loc[8, 'Servicios'])  # Cambiado a 8
    if datos_respuesta.get('epoc') == 'si':
        recomendaciones.append(recomendaciones_df.loc[9, 'Recomendaciones'])  # Cambiado a 9
        # servicios.append(recomendaciones_df.loc[9, 'Servicios'])  # Cambiado a 9
    if datos_respuesta.get('artrosis') == 'si':
        recomendaciones.append(recomendaciones_df.loc[10, 'Recomendaciones'])  # Cambiado a 10
        # servicios.append(recomendaciones_df.loc[10, 'Servicios'])  # Cambiado a 10
    if datos_respuesta.get('osteoporosis') == 'si':
        recomendaciones.append(recomendaciones_df.loc[12, 'Recomendaciones'])  # Cambiado a 12
        # servicios.append(recomendaciones_df.loc[12, 'Servicios'])  # Cambiado a 12
    if datos_respuesta.get('continencia') == 'si':
        recomendaciones.append(recomendaciones_df.loc[15, 'Recomendaciones'])  # Cambiado a 15
        # servicios.append(recomendaciones_df.loc[15, 'Servicios'])  # Cambiado a 15
    if datos_respuesta.get('d_mentales') == 'si':
        recomendaciones.append(recomendaciones_df.loc[16, 'Recomendaciones'])  # Cambiado a 16
        # servicios.append(recomendaciones_df.loc[16, 'Servicios'])  # Cambiado a 16

    # Leer el archivo HTML existente
    with open('templates/informe.html', 'r') as file:
        contenido = file.read()

    # Rellenar las recomendaciones y servicios en el contenido del HTML
    recomendaciones_html = ''.join(f'<li>{recomendacion}</li>' for recomendacion in recomendaciones)
    servicios_html = ''.join(f'<li>{servicio}</li>' for servicio in servicios if pd.notna(servicio))

    # Reemplazar las secciones en el contenido del HTML
    contenido = contenido.replace('{% for recomendacion in recomendaciones %}', recomendaciones_html)
    contenido = contenido.replace('{% endfor %}', '')
    # contenido = contenido.replace('{% for servicio in servicios %}', servicios_html)
    # contenido = contenido.replace('{% endfor %}', '')

    # Guardar el contenido modificado en el mismo archivo
    with open('templates/informe.html', 'w') as file:
        file.write(contenido)


@app.route('/formulario',methods=['GET','POST'])
def formulario():
    
    if not session.get('logged_in'):
        flash('Por favor, inicie sesión primero.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == "POST":
        global df
        print('USUSARIO POST: ',df['user'][0])
        if df['user'][0] == 'init':
            
            df['user']=user_global
            ### prueba ###
            df['fecha_nacimiento'] = request.form.get('fecha_nacimiento')
            df['edad'] = ((datetime.now() - pd.to_datetime(df['fecha_nacimiento']))).dt.total_seconds()
            df['edad'] = df['edad'] /(3600*24*365)
            df['fecha_nacimiento'] = pd.to_datetime(df['fecha_nacimiento']).dt.strftime('%Y-%m-%d')
            df['estado_civil'] = request.form.get('estado_civil')
            df['sexo'] = request.form.get('sexo')
            try:
                df['escolaridad'] = int(request.form.get('escolaridad', 0))
            except ValueError:
                df['escolaridad'] = 0
            df['ocupacion'] = request.form.get('ocupacion')
            df['clase_ingresos'] = request.form.get('clase_ingresos')
            df['fatigabilidad'] = request.form.get('fatigabilidad')
            df['resistencia'] = request.form.get('resistencia')
            df['deambulacion'] = request.form.get('deambulacion')

            comorbilidad = request.form.getlist('comorbilidad')
            df['comorbilidad'] = comorbilidad if comorbilidad else ['Ninguna']

            df['perdida_peso'] = request.form.get('perdida_peso')

            clasificacion = calcular_fragilidad(request.form)

            if clasificacion == 0:
                df['escala_frail'] = 'robusto'
                return render_template('formulario_2.html')
            elif clasificacion <= 2:
                df['escala_frail'] = 'pre_fragil'
                return render_template('formulario_2.html')
            else:
                print("FRAGIL")
                df['comorbilidad'] = df['comorbilidad'].astype(str)
                df['escala_frail'] = 'fragil'
                df['hora_actual'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                df['hipertension'] = None
                df['angina'] = None
                df['insuficiencia_card'] = None
                df['infarto'] =  None
                df['acv'] =  None
                df['diabetes'] =  None
                df['epoc'] =  None
                df['artrosis'] =  None
                df['osteoporosis'] =  None
                df['continencia'] =  None
                df['d_mentales'] =  None
                df['fuma'] =  None
                df['audicion'] =  None
                df['vision'] =  None
                df['equilibrio'] =  None
                df['soporte_social'] =  None
                df['repetir_3_palabras'] =  None
                df['test_reloj'] =  None
                df['estado_animo'] =  None
                df['palabras_recordadas'] =  None
                df['agente'] =  None
                df["estado_salud"] =  None
                df['actividad_fisica_2'] =  None
                df['tiempo_caminar_promedio'] =  None
                df['dolor'] =  None
                df['usa_internet_email'] =  None
                df['test_silla'] =  None
                df['fatigabilidad_1'] =  None
                df['obesidad_abdominal'] =  None
                df['fatigabilidad_2'] =  None
                df['caidas'] =  None
                df['suenio'] =  None
                df['peso'] =  None
                df['altura'] =  None
                df['indice_masa_corporal'] =  None
                df['actividad_fisica_1'] =  None
                df['soledad'] =  None
                df['tiene_celular'] =  None
                df['actividad_fisica_3'] =  None
                df['alcohol'] =  None
                df['memoria'] =  None
                df['diag_fragilidad'] = None
                # df.to_csv('columnas_fragil.csv',index=False)
                guardar_data(tuple(df.iloc[0]))
                df['user'] = 'init' ### OJO
            return render_template('recomendacion.html', estado='FRAGIL')
        
        else:
            df['hora_actual'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df['hora_actual'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df['hipertension'] = request.form.get('hipertension', None)
            df['angina'] = request.form.get('angina', None)
            df['insuficiencia_card'] = request.form.get('insuficiencia_card', None)
            df['infarto'] = request.form.get('infarto', None)
            df['acv'] = request.form.get('acv', None)
            df['diabetes'] = request.form.get('diabetes', None)
            df['epoc'] = request.form.get('epoc', None)
            df['artrosis'] = request.form.get('artrosis', None)
            df['osteoporosis'] = request.form.get('osteoporosis', None)
            df['continencia'] = request.form.get('continencia', None)
            df['d_mentales'] = request.form.get('d_mentales', None)
            df['fuma'] = request.form.get('fuma', None)
            df['audicion'] = request.form.get('audicion', None)
            df['vision'] = request.form.get('vision', None)
            df['equilibrio'] = request.form.get('equilibrio', None)
            df['soporte_social'] = request.form.get('soporte_social', None)
            df['repetir_3_palabras'] = request.form.get('repetir_3_palabras', '')

            estado_animo = request.form.getlist('estado_animo')
            if estado_animo:
                df['estado_animo'] = [str(animo) for animo in estado_animo]
            else:
                df['estado_animo'] = [None]

            df['palabras_recordadas'] = int(request.form.get('palabras_recordadas', 0))
            df['agente'] = request.form.get('agente', None)
            # --------------------------------- df[''] = request.form.get('')
            df["estado_salud"] = int(request.form.get('estado_salud', 0))
            df['actividad_fisica_2'] = int(request.form.get('actividad_fisica_2', 0))
            df['tiempo_caminar_promedio'] = float(request.form.get('tiempo_caminar_promedio', 0.0))
            df['dolor'] = int(request.form.get('dolor', 0))
            df['usa_internet_email'] = int(request.form.get('usa_internet_email', 0))
            df['test_silla'] = int(request.form.get('test_silla', 0))
            df['fatigabilidad_1'] = int(request.form.get('fatigabilidad_1', 0))
            df['obesidad_abdominal'] = float(request.form.get('obesidad_abdominal', 0.0))
            df['fatigabilidad_2'] = int(request.form.get('fatigabilidad_2', 0))
            df['caidas'] = int(request.form.get('caidas', 0))
            df['suenio'] = int(request.form.get('suenio', 0))
            df['peso'] = float(request.form.get('peso', 0.0))
            df['altura'] = float(request.form.get('altura', 0.0))
            df['indice_masa_corporal'] = df['peso'] / (df['altura'] * df['altura'])
            df['altura'] = df['altura'] * 100
            df['actividad_fisica_1'] = int(request.form.get('actividad_fisica_1', 0))
            df['soledad'] = int(request.form.get('soledad', 0))
            df['tiene_celular'] = int(request.form.get('tiene_celular', 0))
            df['actividad_fisica_3'] = int(request.form.get('actividad_fisica_3', 0))
            df['alcohol'] = int(request.form.get('alcohol', 0))
            df['memoria'] = int(request.form.get('memoria', 0))
            df['diag_fragilidad'] = predecir(df)

            # Si comorbilidad está vacío, asigna un valor genérico
            if df['comorbilidad'].empty:
                df['comorbilidad'] = ['Ninguna']  # Puedes cambiar 'Ninguna' por el valor genérico que prefieras

            df['comorbilidad'] = df['comorbilidad'].astype(str)

            # Recorrer todas las columnas del dataframe y verificar si tienen valores nulos
            # for column in df.columns:
            #    if pd.isnull(df[column][0]) or df[column][0] == '':
            #       return f"El campo '{column}' está vacío o es null."
                    # df[column][0] = None  # Asignar None al campo vacío o nulo


            #guardar_data(tuple(df.iloc[0])) REVISAR

            # print("Datos que se intentan insertar:", tuple(df.iloc[0]))

            # print(df.head())
            # df.to_csv('columnas_no_fragil.csv',index=False)

            # df['user'] = 'init'  # OJO

            generar_informe(request.form)

            return render_template('informe.html')
        ##############

    return render_template("formulario.html")


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    # flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('main'))


# @app.route('/json')
# def hello_world():
#     return jsonify({"message": "¡Hola, Flask!"})

# @app.route('/estilo')
# def estilo():
#     return render_template('estilo.html')

@app.route('/juego')
def juego():
    return render_template('game.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080)


