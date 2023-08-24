from backend.geral.config import *
from backend.modelo.jogador import Jogador

@app.route("/listar")
def listar():
    # obter os dados da classe
    dados = db.session.query(Jogador).all()
    if dados:
      # converter dados para json
      lista_jsons = [x.json() for x in dados]

      meujson = {"resultado": "ok"}
      meujson.update({"detalhes": lista_jsons})
      return jsonify(meujson)
    else:
      return jsonify({"resultado":"erro", "detalhes":"classe informada inválida: "})
