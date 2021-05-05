from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField

class ConfiguracoesForm(FlaskForm):
    configSel = HiddenField(id='configSel', default='0')
    submit = SubmitField('Manter Configuração')

    def __init__(self, *args, **kwargs):
        super(ConfiguracoesForm, self).__init__(*args, **kwargs)
