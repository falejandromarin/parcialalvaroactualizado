import json
from flask import Flask, make_response, render_template, request, redirect, url_for
import requests
import webbrowser
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Conexión con firebase para el login 
        url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyCUJur-sA5o1bXTjwXy5kRyyFGj5scvpIA"
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            # Si el inicio de sesión es 200 dirije a la pagina de inicio
            return redirect(url_for('inicio'))
        else:
            # Mostrar mensaje de error en caso de inicio de sesión fallido
            error_message = response.json().get('error', {}).get('message')
            return render_template('login.html', error_message=error_message)
    
    # Si es una solicitud GET, muestra el formulario de inicio de sesión
    return render_template('login.html')



@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Conexion a la api para el registro de  usuario 
        url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyCUJur-sA5o1bXTjwXy5kRyyFGj5scvpIA"
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            # Si el registro es exitoso me redirige al login 
            return redirect(url_for('login'))
        else:
            # Saca un mensaje de error si ya existe el registro 
            error_message = response.json().get('error', {}).get('message')
            return render_template('registro.html', error_message=error_message)
    
    # Muestra el formulario de registro
    return render_template('registro.html')




@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    if request.method == 'POST':
        date = request.form['date']
        api_key = 'UINe5U2L9Uhss1HbaiXNyR4NFYKdpHLv6Iv0hTb9'
        url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}'
        response = requests.get(url)
        data = json.loads(response.text)
        return render_template('inicio.html', data=data)  # Pasar el objeto 'data' a la plantilla
    return render_template('inicio.html')





@app.route('/descargar-pdf')
def descargar_pdf():
    # Obtener los datos de la plantilla 'inicio.html'
    data = {
        'title': request.args.get('title', ''),
        'explanation': request.args.get('explanation', ''),
        'date': request.args.get('date', ''),
        'url': request.args.get('url', '')
    }

    # Generar el contenido del PDF utilizando la biblioteca reportlab
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Agregar contenido al PDF
    p.setFont("Helvetica", 12)
    p.drawString(100, 700, data['title'])
    p.drawString(100, 630, data['date'])
    p.drawImage(data['url'], 100, 350, width=400, height=300)

    # Agregar descripción
    x = 100  # Posición x inicial
    y = 300  # Posición y inicial
    line_height = 15  # Altura de línea
    max_width = 400  # Ancho máximo para ajustar el texto

    lines = data['explanation'].split('\n')  # Separar el texto en líneas
    for line in lines:
        if p.stringWidth(line) <= max_width:
            p.drawString(x, y, line)  # Dibujar línea completa si cabe en el ancho máximo
            y -= line_height
        else:
            words = line.split(' ')  # Separar palabras en la línea
            line_text = ''
            for word in words:
                test_line = line_text + word + ' '
                if p.stringWidth(test_line) <= max_width:
                    line_text = test_line
                else:
                    p.drawString(x, y, line_text)  # Dibujar línea parcial si excede el ancho máximo
                    y -= line_height
                    line_text = word + ' '
            if line_text:
                p.drawString(x, y, line_text)  # Dibujar la última línea parcial o completa si queda alguna



    # Guardar el PDF
    p.showPage()
    p.save()

    # Reiniciar el búfer y establecer la posición en 0
    buffer.seek(0)

    # Crear una respuesta HTTP con el contenido del PDF
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=archivo.pdf'

    return response






@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

if __name__ == '__main__':
    # Ejecuta la aplicación Flask en modo de depuración
    app.run(debug=True)
    
    # Abre la URL en el navegador predeterminado
    webbrowser.open_new('http://127.0.0.1:5000')
