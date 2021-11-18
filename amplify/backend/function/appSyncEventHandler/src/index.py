import json

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths

logger = Logger()
tracer = Tracer()


@logger.inject_lambda_context(correlation_id_path=correlation_paths.APPSYNC_RESOLVER)
@tracer.capture_lambda_handler
def handler(event, context):
    print("received event:")
    print(event)

    return [{"locationID": "1", "enabled": True, "name": "Brew House"}]
