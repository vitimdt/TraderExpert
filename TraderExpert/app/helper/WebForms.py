import wtforms
from wtforms.widgets import HTMLString, html_params


class WebEditableWidget(object):
    def __call__(self, field, **kwargs):
        # get Field from FieldList and create x-editable link based on it
        subfield = field.pop_entry()
        value = kwargs.pop("value", "")

        kwargs.setdefault('data-role', 'x-editable')
        kwargs.setdefault('data-url', '/')

        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)
        kwargs.setdefault('href', '#')

        if not kwargs.get('pk'):
            raise Exception('pk required')
        kwargs['data-pk'] = kwargs.pop("pk")

        if isinstance(subfield, wtforms.StringField):
            kwargs['data-type'] = 'text'
        elif isinstance(subfield, wtforms.BooleanField):
            kwargs['data-type'] = 'select'
        elif isinstance(subfield, wtforms.RadioField):
            kwargs['data-type'] = 'select'
        elif isinstance(subfield, wtforms.SelectField):
            kwargs['data-type'] = 'select'
        elif isinstance(subfield, wtforms.DateField):
            kwargs['data-type'] = 'date'
        elif isinstance(subfield, wtforms.DateTimeField):
            kwargs['data-type'] = 'datetime'
        elif isinstance(subfield, wtforms.IntegerField):
            kwargs['data-type'] = 'number'
        elif isinstance(subfield, wtforms.TextAreaField):
            kwargs['data-type'] = 'textarea'
        else:
            raise Exception('Unsupported field type: %s' % (type(subfield),))

        return HTMLString('<a %s>%s</a>' % (html_params(**kwargs), value))


class WebEditableForm(wtforms.Form):
    # min_entries=1 is required, because WebEditableWidget needs at least 1 entry
    acao_id = wtforms.FieldList(wtforms.IntegerField(), widget=WebEditableWidget(), min_entries=1)
    nome = wtforms.FieldList(wtforms.StringField(), widget=WebEditableWidget(), min_entries=1)
