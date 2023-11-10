from flask import Flask, request, make_response, redirect,render_template,abort,session, url_for,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest
from app import create_app

app = create_app()

todos = ['Comprar cafe', 'enviar solicitud de compra', 'Entregar video a productor']

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    sumit = SubmitField('Enviar')
    
@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    context = {
        'error':error,
        'texto':"Lo sentimos no encontramos lo que buscas",
        'status':404
    }
    return render_template('error.html', **context)

@app.route('/error')
def error_500():
    abort(500)
    
@app.errorhandler(500)
def server_error(error):
    context = {
        'error':error,
        'texto':"Algo salio mal",
        'status':500
    }
    return render_template('error.html', **context)
    
#Indicación para poner la ruta,
@app.route('/')
#Declaramos función para el inicio de nuestra pagina
def index():
    #Inicializamos la variable user_ip para mandar un request donde extrae la ip
    user_ip = request.remote_addr
    #creamos la variable response para poder crear la respuesta redireccionando a la ruta
    #Donde tenemos el mensaje de hello world
    response = make_response(redirect(url_for('hello', _external=True)))
    #Almacenamos la ip en la session que tenemos
    session['user_ip'] = user_ip
    #Retonamos la respuesta
    return response

 #Creamos la ruta de hello y definimos su función
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    #Creamos la variable user_ip para poder tener el request de la ip que se almacena en la session
    user_ip = session.get('user_ip')
    login_form =LoginForm()
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form':login_form,
        'username': username
    }
   
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        
        flash('Nombre de usuario registrado con éxito')
        
        return redirect(url_for('index', _external=True))
    
    return render_template('hello.html', **context )


if __name__ == '__main__':
    

    app.run(port = 5000, debug = True)