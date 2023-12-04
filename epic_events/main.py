import logging

from epic_events.controllers.click_app import app

import sentry_sdk
import os
from dotenv import load_dotenv

load_dotenv()

functions_to_trace = [
    {"new_user_created": "epic_events.controllers.user_controller.user.create_user"},
    {"user_modified": "epic_events.controllers.user_controller.user.modify_user"},
    {"new_contract_and_signed": "epic_events.controllers.user_controller.contract.create_contract"},
    {"contract_modification_signed": "epic_events.controllers.user_controller.user.modify_contract"},
]

sentry_sdk.init(
    dsn=os.getenv("SENTRY_KEY"),
    enable_tracing=True,
    shutdown_timeout=5,
    debug=False
)

logging.getLogger("sentry_sdk").setLevel(logging.WARNING)

if __name__ == '__main__':
    try:
        app()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        # raise e


