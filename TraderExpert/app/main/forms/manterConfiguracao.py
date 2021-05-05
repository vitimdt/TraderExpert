from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ManterConfiguracaoForm(FlaskForm):
    chave = StringField('Chave', validators=[DataRequired(), Length(1, 50,
                                "A chave deve ter no máximo 50 caracteres.")])
    valor = StringField('Valor', validators=[DataRequired(), Length(1, 500,
                                "O valor deve ter no máximo 500 caracteres.")])
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(ManterConfiguracaoForm, self).__init__(*args, **kwargs)