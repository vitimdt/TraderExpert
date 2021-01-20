from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField


class AcessoAcoesForm(FlaskForm):
    acessoSel = HiddenField(id='acessoSel', default='0')
    submit = SubmitField('Configurar Acesso Ação')

    def __init__(self, *args, **kwargs):
        super(AcessoAcoesForm, self).__init__(*args, **kwargs)