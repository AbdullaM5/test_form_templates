import re

from apistar import Route
from apistar import http
from apistar.frameworks.wsgi import WSGIApp
from tinydb import TinyDB


def get_type(value: str) -> str:
    date_regexp = re.compile(r'^(\d{2})[.](\d{2})[.](\d{4})|(\d{4})[/](\d{2})[/](\d{2})$')
    if date_regexp.match(value):
        return 'date'

    phone_number_regexp = re.compile(r'(^(\+7)\d{10}$)')
    if phone_number_regexp.match(value):
        return 'phone_number'

    email_regexp = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
    if email_regexp.match(value):
        return 'email'

    return 'text'


def get_mapping(data):
    return [{'name': k, 'type': get_type(v)} for k, v in data.items()]


def get_intersection_len(form, data) -> int:
    mapping = get_mapping(data)
    fields = set(frozenset(i.items()) for i in form['fields'])
    mapping = set(frozenset(i.items()) for i in mapping)
    return len(fields.intersection(mapping))


def get_form(data: http.RequestData):
    db = TinyDB('db.json')
    forms = db.all()
    for form in forms:
        form.update({'intersection': get_intersection_len(form=form, data=data)})
    forms = list(filter(lambda x: x['intersection'] > 0, forms))
    forms = sorted(forms, key=lambda x: x['intersection'], reverse=True)
    if len(forms) > 0:
        return {'form_name': forms[0]['name']}
    else:
        result = {}
        [result.update({k: get_type(v)}) for k, v in data.items()]
        return result


app = WSGIApp(
    routes=[Route('/get_form', 'POST', get_form)]
)

if __name__ == '__main__':
    app.main()
