from app import create_app, db
from app.entities.Entities import Acao, Configuracao, CotacaoTempoReal, Carteira

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Acao': Acao,
            'Configuracao': Configuracao,
            'CotacaoTempoReal': CotacaoTempoReal,
            'Carteira': Carteira}
