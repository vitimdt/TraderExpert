from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class ConfigMonitorForm(FlaskForm):
    listaAcoes = [('1', 'Ambev ON'), ('2', 'Petrobras PN'), ('3', 'Via Varejo ON')]
    acao = SelectField('Ação', choices=listaAcoes, validators=[DataRequired()])
    valor_ref = StringField('Valor de Referência', validators=[DataRequired()])
    operador = SelectField('Operador', choices=[('-', '-'), ('+', '+')], validators=[DataRequired()])
    valor_dif = StringField('Valor de Referência', validators=[DataRequired()])
    sugestao = SelectField('Sugestao', choices=[('COMPRA', 'COMPRAR'), ('VENDA', 'VENDER')], validators=[DataRequired()])
    percentual = SelectField('Percentual', choices=[('N', 'Não'), ('S', 'Sim')], validators=[DataRequired()])
    ativo = SelectField('Ativo', choices=[('N', 'Não'), ('S', 'Sim')], validators=[DataRequired()])
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(ConfigMonitorForm, self).__init__(*args, **kwargs)
        # self.original_username = original_username

    def validate_acao(self, acao):
        print("Ação: " + str(acao.data))
