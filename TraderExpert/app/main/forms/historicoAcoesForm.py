import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class HistoricoAcoesForm(FlaskForm):
    date_str = '01/01/0001'
    datetime_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
    acao = StringField('Código Ação', id='codigo_acao', validators=[DataRequired()])
    data_inicial = DateField('Data Inicial', default=datetime_obj.date())
    data_final = DateField('Data Final', default=datetime_obj.date())
    submit = SubmitField('Gerar Gráfico', id='submit')

    def __init__(self, *args, **kwargs):
        super(HistoricoAcoesForm, self).__init__(*args, **kwargs)
