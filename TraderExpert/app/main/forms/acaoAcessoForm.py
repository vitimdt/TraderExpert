from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from app.entities.Entities import Configuracao, Acao


class AcaoAcessoForm(FlaskForm):
    acao = SelectField('Ação', validators=[DataRequired()])
    API = SelectField('API', validators=[DataRequired()])
    nome_api = StringField('Nome API Ação', validators=[DataRequired(), Length(1, 255,
                                "O nome da ação deve ter no máximo 255 caracteres.")])
    submit = SubmitField('Salvar')
    novo = None

    def __init__(self, *args, **kwargs):
        super(AcaoAcessoForm, self).__init__(*args, **kwargs)
        obj_acao = Acao()
        obj_config = Configuracao()
        self.acao.choices = obj_acao.retorna_lista_acoes()
        self.API.choices = obj_config.retorna_lista_configuracoes()
        self.novo = True