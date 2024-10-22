import phonenumbers
import pycountry
from api_clientes.clients.regions.definitions.values import Countries


def convert_br_to_e164(phone: str, country: Countries = Countries.Brazil) -> str:
    country_info = pycountry.countries.get(name=country.name)
    parsed = phonenumbers.parse(phone, country_info.alpha_2)
    return f"+{parsed.country_code}{parsed.national_number}"
