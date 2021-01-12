from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField

class CarteiraForm(FlaskForm):
    carteiraSel = HiddenField(id='carteiraSel', default='0')
    submit = SubmitField('Manter Carteira')

    def __init__(self, *args, **kwargs):
        super(CarteiraForm, self).__init__(*args, **kwargs)
