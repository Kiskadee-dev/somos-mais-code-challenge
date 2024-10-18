from client.phone_conversion import convert_br_to_e164


def test_convert_phone():
    phone = "(86) 8370-9831"
    converted = convert_br_to_e164(phone)
    assert converted == "+558683709831"
