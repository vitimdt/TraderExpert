from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp
from app.entities.Entities import Acao


class AcaoCarteiraForm(FlaskForm):
    acao = SelectField('Ação', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Length(1, 100,
                        "Não é permitido e-mail com tamanho maior que 100 caracteres.")])
    valor_compra = StringField('Valor de Compra', validators=[DataRequired(), Regexp(r'^[0-9]+(\,[0-9]{1,2})?$')])
    quantidade = IntegerField('Quantidade', validators=[DataRequired()])
    valor_taxas = StringField('Valor Taxas', validators=[DataRequired(), Regexp(r'^[0-9]+(\,[0-9]{1,2})?$')])
    data_compra = DateField('Data da Compra', validators=[DataRequired()])
    valor_total = StringField('Valor Total', validators=[DataRequired()])
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(AcaoCarteiraForm, self).__init__(*args, **kwargs)
        obj_acao = Acao()
        lista_acoes = obj_acao.retorna_lista_acoes()
        self.acao.choices = lista_acoes
