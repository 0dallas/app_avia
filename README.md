<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Avia</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='index.css') }}">
</head>
<body>
    <div class="encabezado">
        <img src="{{ url_for('static', filename='img/logo_avia.png') }}" class="logo" width="200" height="100">
        <div class="info">
            <a href="#como_funciona">CÓMO FUNCIONA</a>
            <a href="#que_es_avia">QUÉ ES AVIA</a>
        </div>
    </div>
    
    <div class="container">
        <div class="cont_izq">
            <h3>¡Hola! Bienvenido a</h3>
            <img src="{{ url_for('static', filename='img/logo_avia2.png') }}" class="logo2" width="200" height="100">
            <p>ALGORITMO DE VALIDACIÓN DE INDEPENDENCIA Y AUTONOMÍA</p><br>
            <a href="{{url_for('login')}}" class="btn">INGRESAR</a>
        </div>
        <div class="cont_der">
            <img src="{{ url_for('static', filename='img/viejo.png') }}" class="viejo" width="300" height="350">
        </div>
    </div>
    <div class="container2" id="como_funciona">
        <div class="cont_2_1">
            <p class="tit_2">Cómo funciona</p>
        </div>
        <div class="cont_2_2">
            <div class="cont_2_2_1">
                <h2>1</h2>
                <div class="cont_2_2_1_1">
                    <p class="tit">Crear un usuario</p><br>
                    <p>Puede crearlo la misma persona o su cuidador. Consiste en completar una en cuestiones demográficas y de salud.</p>
                </div>
            </div>
            <div class="cont_2_2_1">
                <h2>2</h2>
                <div class="cont_2_2_1_1">
                    <p class="tit">Predicción</p><br>
                    <p>A partir de tus respuestas nuestro algoritmo establecerá un riesgo de pérdida de autonomía con 4 años de anticipación.</p>
                </div>
            </div>
            <div class="cont_2_2_1">
                <h2>3</h2>
                <div class="cont_2_2_1_1">
                    <p class="tit">Informe personalizado</p><br>
                    <p>Recibirá en su correo electrónico un informe personalizado sobre la base de los resultados predictivos con consejos específicos.</p>
                </div>
            </div>
            <div class="cont_2_2_1">
                <h2>4</h2>
                <div class="cont_2_2_1_1">
                    <p class="tit">Seguir</p><br>
                    <p>Nuestro newsletter personalizado hará un seguimiento según los criterios de fragilidad y trabajará fomentando rutinas de autocuidado.</p>
                </div>
            </div>
        </div>
    </div>

    <div class="container3">
        <p class="tit_3">POR QUÉ ES IMPORTANTE PREVENIR LA FRAGILDAD</p>
        <div class="cont_3_1">
            <p class="parrafo">El aumento de la expectativa de vida va a poner a nuestras sociedades frente al desafío en las tareas de cuidado. Es imprescindible mejorar la calidad de vida de los adultos mayores</p>
            <p class="parrafo">A nivel de los sistemas de salud la fragilidad implica un desafío a nivel de costos pues consumen más recursos tanto en atención primaria como en los niveles superiores.</p>
            <p class="parrafo">Las familias entran en tensión para poder garantizar el cuidado. Esto implica una carga que recae principalmente en las mujeres de la familia aumentando la carga de tareas no remuneradas y con costos económicos que pueden ser catastróficos.</p>
        </div>
    </div>

    <div class="container4" id="que_es_avia">
        <div class="cont_4_1">
            <p class="tit_4">QUÉ ES AVIA</p><br>
            <p>El <b>Algoritmo de Validación de Independencia y Autonomía (AVIA)</b> busca ​ayudar a prevenir fragilidad en adultos mayores a partir de una serie de ​preguntas ponderadas que utilizan un <b>algoritmo que desarrolla modelos ​predictivos con cuatro años de anticipación.</b> Es decir, intentamos predecir ​a partir de sencillas preguntas la posibilidad de <b>perder algún grado de ​autonomía en los próximos años y permitir a la persona trabajar en los ​aspectos relevantes para postergar esa pérdida de autonomía</b> y mejorar ​la calidad de vida de las personas mayores.</p><br><br>
            <p class="tit_4">CÓMO SE HIZO</p><br>
            <p>El algoritmo está validado utilizando el estudio de ELSA de Gran Bretaña y ​se apoya en evidencia científica que plantea la posibilidad de predecir ​fragilidad utilizando machine learning.</p><br>
            <p>AVIA fue desarrollado en el marco del <b>Laboratorio de Innovación ​Ciudadana impulsado por la Secretaría General Iberoamericana y la ​Universidad de A Coruña con la colaboración del Municipio de ​Reconquista, Santa Fe, Argentina y la Fundación Cuidados de Salud</b></p>
        </div>
        <img src="{{ url_for('static', filename='img/logo_coruna.png') }}">
        
        
    </div>

   
  
</body>
</html>
