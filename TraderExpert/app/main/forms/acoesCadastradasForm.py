from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField


class AcoesCadastradasForm(FlaskForm):
    acessoSel = HiddenField(id='acessoSel', default='0')
    submit = SubmitField('Configurar Ação')

    def __init__(self, *args, **kwargs):
        super(AcoesCadastradasForm, self).__init__(*args, **kwargs)