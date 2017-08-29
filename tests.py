from app import get_form


def test_get_form():
    tests = [{
        'data': {'phone_number': '+79991234567', 'email': 'example@email.com'},
        'assert': {'form_name': 'registration_form'}
    }, {
        'data': {'email': 'johndoe@email.com', 'created': '18.10.2007'},
        'assert': {'form_name': 'order_form'}
    }, {
        'data': {'email_address': 'hello@email.com', 'password': 'uncommon_password'},
        'assert': {'form_name': 'login_form'}
    }, {
        'data': {'unexpected_field_1': 'email@email.com', 'unexpected_field_2': '1900/12/11'},
        'assert': {'unexpected_field_1': 'email', 'unexpected_field_2': 'date'}
    }]
    for test in tests:
        result = get_form(test['data'])
        assert result == test['assert']
