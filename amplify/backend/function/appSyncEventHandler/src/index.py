from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import AppSyncResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.data_classes.appsync import scalar_types_utils

logger = Logger()
tracer = Tracer()
app = AppSyncResolver()
LOCATIONS = [
    {
        "locationID": "foo",
        "enabled": True,
        "name": "Brew house",
        "description": "String",
        "creationTime": scalar_types_utils.aws_datetime(),  # type AWSDateTime
    },
    {
        "locationID": scalar_types_utils.make_id(),
        "name": "Another one",
        "enabled": False,
        "description": "String",
        "done": True,
        "creationTime": scalar_types_utils.aws_datetime(),
    },
]


@app.resolver(type_name="Query", field_name="getLocation")
def get_location(location_id: str = ""):
    logger.info(f"Fetching location by id: {location_id}")
    for location in LOCATIONS:
        if location["locationID"] == location_id:
            return location

    raise ValueError("Not found")


@app.resolver(type_name="Query", field_name="listLocations")
def list_locations():
    return LOCATIONS


@app.resolver(field_name="commonField")
def common_field():
    return scalar_types_utils.make_id()


@logger.inject_lambda_context(correlation_id_path=correlation_paths.APPSYNC_RESOLVER)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
