import pytest

from clearbit_info import additional_data


def test_clearbit_info():
    email = 'marko.mutavdzic@factoryww.com'
    user_data = additional_data(email)

    assert user_data == {'company_name': 'Factory World Wide',
                         'company_sector': 'Information Technology',
                         'user_location': None,
                         'user_title': None}


def test_clearbit_info_web_mail():
    email = 'markodmutavdzic@gmail.com'
    with pytest.raises(TypeError):
        additional_data(email)