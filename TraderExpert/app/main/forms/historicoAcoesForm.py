from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired


class HistoricoAcoesForm(FlaskForm):
    acao = StringField('Código Ação', id='codigo_acao', validators=[DataRequired()])
    submit = SubmitField('Gerar Gráfico', id='submit')

    def __init__(self, *args, **kwargs):
        super(HistoricoAcoesForm, self).__init__(*args, **kwargs)
