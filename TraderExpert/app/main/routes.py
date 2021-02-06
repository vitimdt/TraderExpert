from flask import render_template, request, url_for, redirect, flash, jsonify
from app import db
from app.main import bp
from app.entities.Entities import CotacaoTempoReal, Monitoramento, Carteira, AcessoAPI, Configuracao, Acao
from app.main.forms.configMonitorForm import ConfigMonitorForm
from app.main.forms.monitoramentoForm import MonitoramentoForm
from app.main.forms.carteiraForm import CarteiraForm
from app.main.forms.acaoCarteiraForm import AcaoCarteiraForm
from app.main.forms.acessoAcoesForm import AcessoAcoesForm
from app.main.forms.manterAcessoAcaoForm import ManterAcessoAcaoForm
from app.main.forms.cadastrarAcoesForm import CadastrarAcoesForm
from app.main.forms.manterConfiguracao import ManterConfiguracaoForm
from app.main.forms.configuracoesForm import ConfiguracoesForm


@bp.route('/traderexpert/', methods=['GET'])
@bp.route('/traderexpert/index', methods=['GET'])
def index():
    cols, rs, tot = CotacaoTempoReal.buscaCotacaoTR()
    return render_template('index.html', title='Home', columns=cols, items=rs,
                           tot_invest=tot[0], tot_cotacao=tot[1], dif_total=tot[2],
                           dif_percentual=tot[3])


@bp.route('/traderexpert/cotacoestr', methods=['GET'])
def cotacoestr():
    cols, rs, tot = CotacaoTempoReal.buscaCotacaoTR()
    return render_template('_cotacoesTempoReal.html', columns=cols, items=rs,
                           tot_invest=tot[0], tot_cotacao=tot[1], dif_total=tot[2],
                           dif_percentual=tot[3])


@bp.route('/traderexpert/monitor', methods=['GET'])
def monitor():
    form = MonitoramentoForm()
    cols, rs = Monitoramento.buscaMonitoramentos()
    return render_template('monitoramento.html', title='Monitoramento Ações', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/configmonitor', methods=['GET', 'POST'])
def configmonitor():
    monitor_form = ConfigMonitorForm()
    obj_monitoramento = Monitoramento()
    monitoramento = None
    id = "0"
    params = request.args
    if "monitorSel" in params:
        monitorsel = params["monitorSel"]
        if monitorsel != "0":
            id = str(monitorsel).split('_')[1]
        else:
            id = "0"
    if monitor_form.validate_on_submit():
        if id != "0":
            monitoramento = obj_monitoramento.find_by_id(id_monitoramento=int(id))
        else:
            monitoramento = Monitoramento()
        monitoramento.acao_id = monitor_form.acao.data
        monitoramento.valor_ref = monitor_form.valor_ref.data.replace(',', '.')
        monitoramento.operador = monitor_form.operador.data
        monitoramento.valor_meta_dif = monitor_form.valor_dif.data.replace(',', '.')
        monitoramento.sugestao = monitor_form.sugestao.data
        monitoramento.flg_percentual = monitor_form.percentual.data
        monitoramento.flg_ativo = monitor_form.ativo.data
        if id == "0":
            db.session.add(monitoramento)
        db.session.commit()
        flash('Suas alterações foram gravadas com sucesso.')
        return redirect(url_for('main.configmonitor'))
    elif request.method == 'GET':
        if id != "0":
            monitoramento = obj_monitoramento.find_by_id(id_monitoramento=int(id))
            monitor_form.novo = False
            monitor_form.acao.data = str(monitoramento.acao_id)
            monitor_form.valor_ref.data = str(monitoramento.valor_ref).replace('.', ',')
            monitor_form.operador.data = monitoramento.operador
            monitor_form.valor_dif.data = str(monitoramento.valor_meta_dif).replace('.', ',')
            monitor_form.sugestao.data = monitoramento.sugestao
            monitor_form.percentual.data = monitoramento.flg_percentual
            monitor_form.ativo.data = monitoramento.flg_ativo
    return render_template('configMonitoramento.html', title='Configurar Monitoramento', form=monitor_form)


@bp.route('/traderexpert/todosmonitores', methods=['GET'])
def todosmonitores():
    form = MonitoramentoForm()
    cols, rs = Monitoramento.todosMonitoramentos()
    return render_template('monitores.html', title='Monitoramentos', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/removermonitor', methods=['GET'])
def removermonitor():
    id_monitor = request.args.get('monitorid')
    itemMonitor = Monitoramento.query.filter_by(id=id_monitor).first_or_404()
    db.session.delete(itemMonitor)
    db.session.commit()
    form = MonitoramentoForm()
    cols, rs = Monitoramento.todosMonitoramentos()
    return render_template('_monitores.html', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/acessoacoes', methods=['GET'])
def acessoacoes():
    form = AcessoAcoesForm()
    cols, rs = AcessoAPI.retornarAcessosAPI()
    return render_template('acessoAcoes.html', title='Ações Cadastradas', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/manteracessoacao', methods=['GET', 'POST'])
def manteracessoacao():
    acessoacao_form = ManterAcessoAcaoForm()
    obj_acessoApi = AcessoAPI()
    acessoApi = None
    id = "0"
    params = request.args
    if "acessoSel" in params:
        acessoSel = params["acessoSel"]
        if acessoSel != "0":
            id = str(acessoSel).split('_')[1]
        else:
            id = "0"
    if acessoacao_form.validate_on_submit():
        if id != "0":
            acessoApi = obj_acessoApi.find_by_id(idAcessoAPI=int(id))
        else:
            acessoApi = AcessoAPI()
            acessoApi.acao_id = acessoacao_form.acao.data
            acessoApi.api_id = acessoacao_form.API.data
        acessoApi.nome_api = acessoacao_form.nome_api.data
        if id == "0":
            acessoAux = obj_acessoApi.find_by_idAcao_idAPI(idAcao=acessoApi.acao_id, idAPI=acessoApi.api_id)
            if acessoAux is None:
                db.session.add(acessoApi)
            else:
                error = 'Já existe o acesso ação cadastrado no sistema.'
                acessoacao_form.nome_api.data = ""
                return render_template('manterAcessoAcao.html', title='Manter Acesso Ação',
                                       form=acessoacao_form, error=error)
        db.session.commit()
        flash('Suas alterações foram gravadas com sucesso.')
        return redirect(url_for('main.manteracessoacao'))
    elif request.method == 'GET':
        if id != "0":
            acessoApi = obj_acessoApi.find_by_id(idAcessoAPI=int(id))
            acessoacao_form.acao.data = str(acessoApi.acao_id)
            acessoacao_form.API.data = str(acessoApi.api_id)
            acessoacao_form.nome_api.data = acessoApi.nome_api
    return render_template('manterAcessoAcao.html', title='Manter Acesso Ação', form=acessoacao_form)


@bp.route('/traderexpert/removeracessoacao', methods=['GET'])
def removeracessoacao():
    id_acesso = request.args.get('acessoid')
    itemAcesso = AcessoAPI.query.filter_by(id=id_acesso).first_or_404()
    db.session.delete(itemAcesso)
    db.session.commit()
    form = AcessoAcoesForm()
    cols, rs = AcessoAPI.retornarAcessosAPI()
    return render_template('_acessoAcoes.html', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/minhacarteira', methods=['GET'])
def minhacarteira():
    form = CarteiraForm()
    cols, rs = Carteira.retornarCarteira()
    return render_template('carteira.html', title='Minha Carteira', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/mantercarteira', methods=['GET', 'POST'])
def mantercarteira():
    carteira_form = AcaoCarteiraForm()
    obj_carteira = Carteira()
    acao_carteira = None
    id = "0"
    params = request.args
    if "carteiraSel" in params:
        carteira_sel = params["carteiraSel"]
        if carteira_sel != "0":
            id = str(carteira_sel).split('_')[1]
        else:
            id = "0"
    if carteira_form.validate_on_submit():
        if id != "0":
            acao_carteira = obj_carteira.find_by_id(id_carteira=int(id))
        else:
            acao_carteira = Carteira()
        acao_carteira.acao_id = carteira_form.acao.data
        acao_carteira.email = carteira_form.email.data
        acao_carteira.valor = carteira_form.valor_compra.data.replace(',', '.')
        acao_carteira.quantidade = carteira_form.quantidade.data
        acao_carteira.valor_taxas = carteira_form.valor_taxas.data.replace(',', '.')
        acao_carteira.data_compra = carteira_form.data_compra.data
        acao_carteira.valor_total = carteira_form.valor_total.data.replace(',', '.')
        if id == "0":
            db.session.add(acao_carteira)
        db.session.commit()
        flash('Suas alterações foram gravadas com sucesso.')
        return redirect(url_for('main.mantercarteira'))
    elif request.method == 'GET':
        if id != "0":
            acao_carteira = obj_carteira.find_by_id(id_carteira=int(id))
            carteira_form.acao.data = str(acao_carteira.acao_id)
            carteira_form.email.data = str(acao_carteira.email)
            carteira_form.valor_compra.data = str(acao_carteira.valor).replace('.', ',')
            carteira_form.quantidade.data = acao_carteira.quantidade
            carteira_form.valor_taxas.data = str(acao_carteira.valor_taxas).replace('.', ',')
            carteira_form.data_compra.data = acao_carteira.data_compra
            carteira_form.valor_total.data = str(acao_carteira.valor_total).replace('.', ',')
    return render_template('manterAcaoCarteira.html', title='Manter Carteira', form=carteira_form)


@bp.route('/traderexpert/cadastraracoes', methods=['POST', 'GET'])
def cadastraracoes():
    form = CadastrarAcoesForm()
    obj_acao = Acao()
    if form.validate_on_submit():
        obj_acao.codigo = form.codigo_acao.data
        obj_acao.nome = form.nome_acao.data
        acaoAux = obj_acao.find_by_code(codigo=obj_acao.codigo)
        if acaoAux is None:
            db.session.add(obj_acao)
        else:
            error = 'Já existe o código de ação ( ' + obj_acao.codigo + ') cadastrado no sistema.'
            form.codigo_acao.data = ""
            form.nome_acao.data = ""
            return render_template('cadastrarAcoes.html', title='Cadastrar Ações', form=form, error=error)
        db.session.commit()
        flash('Suas alterações foram gravadas com sucesso.')
        return redirect(url_for('main.manteracessoacao'))
    return render_template('cadastrarAcoes.html', title='Cadastrar Ações', form=form)


@bp.route('/traderexpert/configuracoes', methods=['GET'])
def configuracoes():
    form = ConfiguracoesForm()
    cols, rs = Configuracao.retornarConfiguracoes()
    return render_template('configuracoes.html', title='Configurações', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/removerconfiguracao', methods=['GET'])
def removerconfiguracao():
    id_config = request.args.get('configid')
    itemConfig = Configuracao.query.filter_by(id=id_config).first_or_404()
    db.session.delete(itemConfig)
    db.session.commit()
    form = ConfiguracoesForm()
    cols, rs = Configuracao.retornarConfiguracoes()
    return render_template('_configuracoes.html', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/manterconfiguracao', methods=['GET', 'POST'])
def manterconfiguracao():
    form = ManterConfiguracaoForm()
    obj_config = Configuracao()
    config = None
    id = "0"
    params = request.args
    if "configSel" in params:
        config_sel = params["configSel"]
        if config_sel != "0":
            id = str(config_sel).split('_')[1]
            config = obj_config.find_by_id(idConfig=int(id))
            form.chave.data = config.chave
        else:
            id = "0"
    if form.validate_on_submit():
        if id == "0":
            config = Configuracao()
            config.chave = form.chave.data
        config.valor = form.valor.data
        if id == "0":
            configAux = obj_config.find_by_key(chave=config.chave)
            if configAux is None:
                db.session.add(config)
            else:
                error = 'Já existe a chave (' + config.chave + ') cadastrada no sistema.'
                form.chave.data = ""
                form.valor.data = ""
                return render_template('manterConfiguracao.html', title='Manter Configuração', form=form, error=error)
        db.session.commit()
        flash('Suas alterações foram gravadas com sucesso.')
        return redirect(url_for('main.configuracoes'))
    elif request.method == 'GET':
        if id != "0":
            config = obj_config.find_by_id(idConfig=int(id))
            form.chave.data = str(config.chave)
            form.valor.data = str(config.valor)
    return render_template('manterConfiguracao.html', title='Manter Configuração', form=form)


@bp.route('/traderexpert/removeracao', methods=['GET'])
def removeracao():
    id_acao = request.args.get('acaoid')
    itemCarteira = Carteira.query.filter_by(id=id_acao).first_or_404()
    db.session.delete(itemCarteira)
    db.session.commit()
    form = CarteiraForm()
    cols, rs = Carteira.retornarCarteira()
    return render_template('_acoesCarteira.html', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/notifications')
def notifications():
    # Buscar ações sugeridas OK
    cols, rs = Monitoramento.buscaMonitoramentos()
    count = 0
    for row in rs:
        if row['Status'] == 'OK':
            count += 1
    return jsonify([{
        'name': 'acoes_sugeridas',
        'data': str(count)
    }])
