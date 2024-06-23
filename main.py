# Motor de Consultas Inteligentes (MCI)
# Importar las librerías necesarias
import os
from flask import Flask, request, jsonify, render_template
# from langchain.sql_database import SQLDatabase
# from langchain.chat_models import openai
# from langchain.chains import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Establecer la clave de la API de OpenAI desde las variables de entorno
openai_api_key = os.getenv("OPENAI_API_KEY")

# Verificar que la clave de la API de OpenAI esté configurada correctamente
if not openai_api_key:
    raise ValueError("No se ha configurado la clave de la API de OpenAI en las variables de entorno.")

# Cargar la base de datos
db = SQLDatabase.from_uri("sqlite:///MCI_DB.db3")

# Crear el LLM
llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

# Crear la cadena
cadena = SQLDatabaseChain(llm=llm, database=db, verbose=False)

# Formato personalizado de respuesta
formato = """
El usuario puede preguntar por alguna incidencia en particular:
1. Si el usuario te saluda, respóndele con un saludo.
2. Con la pregunta del usuario, crea y ejecuta una consulta SQLite3 sobre las tablas de la base de datos para proporcionar la respuesta necesaria.
3. La consulta SQLite debe ser capaz de generar una consulta correcta sin tener en cuenta signos de puntuación ni discriminar entre mayúsculas y minúsculas.
4. Solo devuelve información existente en la base de datos y nunca inventes información.
5. No muestres la consulta SQL ejecutada al usuario, a menos que él lo solicite.
6. Si el usuario pregunta por una incidencia, alarma, alerta, requerimiento o escalamiento, proporciona la información correspondiente.
7. Siempre responde en español.
8. Da la respuesta en formato texto limpio, sin caracteres especiales, ni caracteres de escape, a menos que el usuario especifique otro formato.
9. Si ocurre un error, no muestres el error al usuario. Solo indica que no fue posible consultar la información y sugiere reformular la pregunta con más detalles.
10. No ejecutes ninguna sentencia sql que conetnga delete o drop.
A continuación, la pregunta del usuario: #{question}
"""

# Función para hacer la consulta
def consulta(input_usuario):
    consulta = formato.format(question=input_usuario)
    print(consulta)
    resultado = cadena.run(consulta)
    return resultado

app = Flask(__name__, static_folder='static', static_url_path='/static', template_folder='templates')

# Endpoint para servir la página HTML
@app.route('/')
def index():
    return render_template('index.html')

# El resto de tu código sigue igual
@app.route('/query', methods=['POST'])
def consulta_endpoint():
    data = request.get_json()
    input_usuario = data.get('message')
    if not input_usuario:
        return jsonify({"error": "No message provided"}), 400

    try:
        respuesta = consulta(input_usuario)
        return jsonify({"response": respuesta})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)