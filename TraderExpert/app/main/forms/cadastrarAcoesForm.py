from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CadastrarAcoesForm(FlaskForm):
    codigo_acao = StringField('Código Ação', validators=[DataRequired(), Length(1, 8,
                                "O código da ação deve ter no máximo 8 caracteres.")])
    nome_acao = StringField('Nome Ação', validators=[DataRequired(), Length(1, 70,
                                "O nome da ação deve ter no máximo 70 caracteres.")])
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(CadastrarAcoesForm, self).__init__(*args, **kwargs)
