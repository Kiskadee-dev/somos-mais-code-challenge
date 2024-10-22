from enum import Enum


class EndpointRepo(Enum):
    users_json = "https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json"
    users_csv = "https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv"
