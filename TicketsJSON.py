import json


def get_tickets_json():
    with open('tickets.json', 'r') as data:
        return json.load(data)


def dump_tickets_json(to_dump):
    with open('tickets.json', 'w') as data:
        json.dump(to_dump, data)
