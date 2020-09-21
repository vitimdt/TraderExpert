from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Regexp
from app.entities.Entities import Acao


class ConfigMonitorForm(FlaskForm):
    acao = SelectField('Ação', validators=[DataRequired()])
    valor_ref = StringField('Valor de Referência', validators=[DataRequired(), Regexp(r'^[0-9]+(\,[0-9]{1,2})?$')])
    operador = SelectField('Operador', choices=[('-', '-'), ('+', '+')], validators=[DataRequired()])
    valor_dif = StringField('Valor de Referência', validators=[DataRequired(), Regexp(r'^[0-9]+(\,[0-9]{1,2})?$')])
    sugestao = SelectField('Sugestao', choices=[('COMPRA', 'COMPRAR'), ('VENDA', 'VENDER')], validators=[DataRequired()])
    percentual = SelectField('Percentual', choices=[('N', 'Não'), ('S', 'Sim')], validators=[DataRequired()])
    ativo = SelectField('Ativo', choices=[('N', 'Não'), ('S', 'Sim')], validators=[DataRequired()])
    submit = SubmitField('Salvar')
    novo = None

    def __init__(self, *args, **kwargs):
        super(ConfigMonitorForm, self).__init__(*args, **kwargs)
        obj_acao = Acao()
        lista_acoes = obj_acao.retorna_lista_acoes()
        self.acao.choices = lista_acoes
        self.novo = True
