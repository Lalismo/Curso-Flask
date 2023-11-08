from flask import Flask, request, make_response, redirect,render_template,abort
app = Flask(__name__)

todos = ['Comprar cafe', 'enviar solicitud de compra', 'Entregar video a productor']

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
    response = make_response(redirect('/hello'))
    #Almacenamos la ip en un cookie
    response.set_cookie('user_ip', user_ip)
    #Retonamos la respuesta
    return response

 #Creamos la ruta de hello y definimos su función
@app.route('/hello')
def hello():
    #Creamos la variable user_ip para poder tener el request de la ip que se almaceno en la cookie
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip': user_ip,
        'todos': todos
    }
   
    return render_template('hello.html', **context )


if __name__ == '__main__':
     app.run(port = 5000, debug = True)