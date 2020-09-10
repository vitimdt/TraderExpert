from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField

class MonitoramentoForm(FlaskForm):
    monitorSel = HiddenField(id='monitorSel', default='0')
    submit = SubmitField('Configurar Monitoramento')

    def __init__(self, *args, **kwargs):
        super(MonitoramentoForm, self).__init__(*args, **kwargs)
