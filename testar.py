from backend.geral.config import *
from backend.testar import *

# inserindo a aplicação em um contexto :-/
with app.app_context():

    testar_jogador.run()