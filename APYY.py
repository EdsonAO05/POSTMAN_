from flask import Flask, jsonify, request, make_response
import json
import yaml
from dicttoxml import dicttoxml
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_FOLDER = os.path.join(BASE_DIR, "DOCENTES")

app = Flask(__name__)

# --- Base de datos temporal en memoria ---
docentes = []

@app.route("/")
def home():
    return "API de Registro de Docentes"

# --- Registrar docente ---
@app.route("/profes", methods=["GET", "POST"])
def registrar_docente():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form  

        docente = {
            "nombre": data.get("nombre"),
            "num_empleado": data.get("num_empleado"),
            "carrera": data.get("carrera")
        }
        docentes.append(docente)
        return jsonify({"mensaje": "Docente registrado", "total": len(docentes)}), 201
    else:
        return '''
        <h2>Registrar Docente</h2>
        <form method="POST" action="/profes">
            Nombre: <input type="text" name="nombre"><br>
            Número de empleado: <input type="text" name="num_empleado"><br>
            Carrera: <input type="text" name="carrera"><br>
            <button type="submit">Registrar</button>
        </form>
        '''

# --- Listar todos los docentes ---
@app.route("/docentes", methods=["GET"])
def listar_docentes():
    return jsonify(docentes), 200


# --- Exportar JSON y devolverlo como archivo ---
@app.route("/exportar/json", methods=["GET"])
def exportar_json():
    json_data = json.dumps(docentes, ensure_ascii=False, indent=4)
    return app.response_class(
        response=json_data,
        status=200,
        mimetype="application/json"
    )



# --- Exportar YAML y devolverlo como archivo ---
@app.route("/exportar/yaml", methods=["GET"])
def exportar_yaml():
    yaml_data = yaml.dump(docentes, allow_unicode=True)
    return app.response_class(
        response=yaml_data,
        status=200,
        mimetype="text/yaml"
    )



# --- Exportar XML y devolverlo como archivo ---
@app.route("/exportar/xml", methods=["GET"])
def exportar_xml():
    xml_data = dicttoxml(docentes, custom_root="docentes", attr_type=False)
    return app.response_class(
        response=xml_data,
        status=200,
        mimetype="application/xml"
    )


if __name__ == "__main__":
    app.run(debug=True)
