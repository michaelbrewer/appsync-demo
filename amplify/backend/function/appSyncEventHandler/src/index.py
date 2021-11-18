import json


def handler(event, context):
    print("received event:")
    print(event)

    return [{"locationID": "1", "enabled": True, "name": "Brew House"}]
