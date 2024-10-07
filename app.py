from flask import Flask, jsonify, request, render_template,redirect,url_for,flash,session

import pandas as pd
from datetime import datetime
import joblib

from func import enviar_email,generar_codigo, hash_password, verify_password

pipeline = joblib.load('model_pipeline.pkl')

app = Flask(__name__)

app.secret_key = 'secret'

mail = ''
cod = ''
df = pd.DataFrame([{'user':'init'}])

USER_CREDENTIALS = {
    "username": "user",
    "password": "pass"
}


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['logged_in'] = True
            # flash('Login exitoso', 'success')
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
            global mail
            mail = correo
            global cod
            cod = generar_codigo()
            # print("Codigo:",cod)
            enviar_email(mail,cod)
            return render_template("codigo.html",correo=correo)
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
        if contra1 == contra2:
            return redirect(url_for('login'))
        else:
            flash('Las contraseñas no son iguales', 'danger')  

    return render_template("registrar.html")

@app.route('/formulario',methods=['GET','POST'])
def formulario():

    if not session.get('logged_in'):
        flash('Por favor, inicie sesión primero.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == "POST":
        global df
        print('USUSARIO POST: ',df['user'][0])
        if df['user'][0] == 'init':
            
            df['user']='prueba'
            ### prueba ###
            df['fecha_nacimiento'] = request.form.get('fecha_nacimiento')
            df['edad'] = ((datetime.now() - pd.to_datetime(df['fecha_nacimiento']))).dt.total_seconds()
            df['edad'] = df['edad'] /(3600*24*365)
            df['estado_civil'] = request.form.get('estado_civil')
            df['sexo'] = request.form.get('sexo')
            df['escolaridad'] = int(request.form.get('escolaridad'))
            df['ocupacion'] = request.form.get('ocupacion')
            df['clase_ingresos'] = request.form.get('clase_ingresos')
            df['fatigabilidad'] = request.form.get('fatigabilidad')
            df['resistencia'] = request.form.get('resistencia')
            df['deambulacion'] = request.form.get('deambulacion')
            df['comorbilidad'] = [request.form.getlist('comorbilidad')]
            df['perdida_peso'] = request.form.get('perdida_peso')
            
            if request.form.getlist('comorbilidad') == None:
                df['escala_frail'] = 'robusto'
                return render_template('formulario_2.html')
            elif len(request.form.getlist('comorbilidad')) <= 2:
                df['escala_frail'] = 'pre_fragil'
                return render_template('formulario_2.html')
            else:
                print("FRAGIL")
                df['escala_frail'] = 'fragil'
                df['user'] = 'init' ### OJO
            return render_template('recomendacion.html',estado='FRAGIL')
        
        else:
            df['hora_actual'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df['hipertension'] = request.form.get('hipertension')
            df['angina'] = request.form.get('angina')
            df['insuficiencia_card'] = request.form.get('insuficiencia_card')
            df['infarto'] = request.form.get('infarto')
            df['acv'] = request.form.get('acv')
            df['diabetes'] = request.form.get('diabetes')
            df['epoc'] = request.form.get('epoc')
            df['artrosis'] = request.form.get('artrosis')
            df['osteoporosis'] = request.form.get('osteoporosis')
            df['continencia'] = request.form.get('continencia')
            df['d_mentales'] = request.form.get('d_mentales')
            df['fuma'] = request.form.get('fuma')
            df['audicion'] = request.form.get('audicion')
            df['vision'] = request.form.get('vision')
            df['equilibrio'] = request.form.get('equilibrio')
            df['soporte_social'] = request.form.get('soporte_social')
            df['repetir_3_palabras'] = request.form.get('repetir_3_palabras')
            df['test_reloj'] = request.form.get('test_reloj')
            df['estado_animo'] = request.form.get('estado_animo')
            # --------------------------------- df[''] = request.form.get('')
            df["estado_salud"] = int(request.form.get('estado_salud'))
            df['actividad_fisica_2'] = int(request.form.get('actividad_fisica_2'))
            df['tiempo_caminar_promedio'] = float(request.form.get('tiempo_caminar_promedio'))
            df['dolor'] = int(request.form.get('dolor'))
            df['usa_internet_email'] = int(request.form.get('usa_internet_email'))
            df['test_silla'] = int(request.form.get('test_silla'))
            df['fatigabilidad_1'] = int(request.form.get('fatigabilidad_1'))
            df['obesidad_abdominal'] = float(request.form.get('obesidad_abdominal'))
            df['fatigabilidad_2'] = int(request.form.get('fatigabilidad_2'))
            df['caidas'] = int(request.form.get('caidas'))
            df['suenio'] = int(request.form.get('suenio'))
            df['peso'] = float(request.form.get('peso'))
            df['altura'] = float(request.form.get('altura'))
            df['indice_masa_corporal'] = df['peso']/(df['altura']*df['altura'])
            df['altura'] = df['altura']*100
            df['actividad_fisica_1'] = int(request.form.get('actividad_fisica_1'))
            df['soledad'] = int(request.form.get('soledad'))
            df['tiene_celular'] = int(request.form.get('tiene_celular'))
            df['actividad_fisica_3'] = int(request.form.get('actividad_fisica_3'))
            df['alcohol'] = int(request.form.get('alcohol'))
            df['memoria'] = int(request.form.get('memoria'))

            print(df.head())

            df['user'] = 'init' ### OJO
            
            return render_template('recomendacion.html',estado='NO FRAGIL')
        ##############

        # df['hora_actual'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # df['estado_civil'] = request.form.get('estado_civil')
        # df['sexo'] = request.form.get('sexo')
        # df['ocupacion'] = request.form.get('ocupacion')
        # df['clase_ingresos'] = request.form.get('clase_ingresos')
        # df['fatigabilidad'] = request.form.get('fatigabilidad')
        # df['resistencia'] = request.form.get('resistencia')
        # df['deambulacion'] = request.form.get('deambulacion')
        # df['comorbilidad'] = request.form.get('comorbilidad')
        # df['perdida_peso'] = request.form.get('perdida_peso')
        # df['hipertension'] = request.form.get('hipertension')
        # df['angina'] = request.form.get('angina')
        # df['insuficiencia_card'] = request.form.get('insuficiencia_card')
        # df['infarto'] = request.form.get('infarto')
        # df['acv'] = request.form.get('acv')
        # df['diabetes'] = request.form.get('diabetes')
        # df['epoc'] = request.form.get('epoc')
        # df['artrosis'] = request.form.get('artrosis')
        # df['osteoporosis'] = request.form.get('osteoporosis')
        # df['continencia'] = request.form.get('continencia')
        # df['d_mentales'] = request.form.get('d_mentales')
        # df['fuma'] = request.form.get('fuma')
        # df['audicion'] = request.form.get('audicion')
        # df['vision'] = request.form.get('vision')
        # df['equilibrio'] = request.form.get('equilibrio')
        # df['soporte_social'] = request.form.get('soporte_social')
        # df['repetir_3_palabras'] = request.form.get('repetir_3_palabras')
        # df['test_reloj'] = request.form.get('test_reloj')
        # df['estado_animo'] = request.form.get('estado_animo')
        # # --------------------------------- df[''] = request.form.get('')
        # df["estado_salud"] = int(request.form.get('estado_salud'))
        # df['actividad_fisica_2'] = int(request.form.get('actividad_fisica_2'))
        # df['tiempo_caminar_promedio'] = float(request.form.get('tiempo_caminar_promedio'))
        # df['dolor'] = int(request.form.get('dolor'))
        # df['usa_internet_email'] = int(request.form.get('usa_internet_email'))
        # df['fecha_nacimiento'] = request.form.get('fecha_nacimiento')
        # df['edad'] = ((datetime.now() - pd.to_datetime(df['fecha_nacimiento']))).dt.total_seconds()
        # df['edad'] = df['edad'] /(3600*24*365)
        # df['test_silla'] = int(request.form.get('test_silla'))
        # df['fatigabilidad_1'] = int(request.form.get('fatigabilidad_1'))
        # df['obesidad_abdominal'] = float(request.form.get('obesidad_abdominal'))
        # df['fatigabilidad_2'] = int(request.form.get('fatigabilidad_2'))
        # df['escolaridad'] = int(request.form.get('escolaridad'))
        # df['caidas'] = int(request.form.get('caidas'))
        # df['suenio'] = int(request.form.get('suenio'))
        # df['peso'] = float(request.form.get('peso'))
        # df['altura'] = float(request.form.get('altura'))
        # df['indice_masa_corporal'] = df['peso']/(df['altura']*df['altura'])
        # df['altura'] = df['altura']*100
        # df['actividad_fisica_1'] = int(request.form.get('actividad_fisica_1'))
        # df['soledad'] = int(request.form.get('soledad'))
        # df['tiene_celular'] = int(request.form.get('tiene_celular'))
        # df['actividad_fisica_3'] = int(request.form.get('actividad_fisica_3'))
        # df['alcohol'] = int(request.form.get('alcohol'))
        # df['memoria'] = int(request.form.get('memoria'))
        
        prediction = pipeline.predict_proba(df)[:, 1][0].tolist()
        if prediction >= 0.05:
            prediction = 'POSITIVO'
        else:
            prediction = 'NEGATIVO'
        
        return render_template("formulario.html",
                           prediction=prediction)

    return render_template("formulario.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    # flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('main'))


@app.route('/json')
def hello_world():
    return jsonify({"message": "¡Hola, Flask!"})

@app.route('/estilo')
def estilo():
    return render_template('estilo.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5002)


