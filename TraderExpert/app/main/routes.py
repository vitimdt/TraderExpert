from flask import render_template, request
from app.main import bp
from app.entities.Entities import CotacaoTempoReal, Monitoramento
from app.helper.WebForms import WebEditableForm

@bp.route('/traderexpert/', methods=['GET', 'POST'])
@bp.route('/traderexpert/index', methods=['GET', 'POST'])
def index():
    cols, rs, tot = CotacaoTempoReal.buscaCotacaoTR()
    return render_template('index.html', title='Home', columns=cols, items=rs,
                           tot_invest=tot[0], tot_cotacao=tot[1], dif_total=tot[2],
                           dif_percentual=tot[3])

@bp.route('/traderexpert/monitor', methods=['GET', 'POST'])
def monitor():
    cols, rs = Monitoramento.buscaMonitoramentos()
    return render_template('monitoramento.html', title='Monitoramento Ações', columns=cols, items=rs)


@bp.route('/traderexpert/config_monitor', methods=['POST', 'GET'])
def config_monitor():
    form = WebEditableForm(request.form)
    if (request.method == "POST") and form.validate():
        for x in form:
            print("POST Params: " + str(x))
            # last_index will be set if a field is submitted
            # if getattr(x, 'last_index', None):
            #    model = Model1.query.get(x.last_index)
            #    setattr(model, x.name, x.data.pop())
            #    db.session.commit()
    elif (request.method == "POST") and not form.validate():
        print("Errors", form.errors)
    monitores = Monitoramento()
    for x in monitores.find_by_ativos():
        print(x.acao_id, x.acao.nome)
    return render_template('config_monitoramentos.html', title='Configurar Monitoramentos', form=form)
