from epic_events.controllers.click_app import app

import sentry_sdk
import os
from dotenv import load_dotenv


load_dotenv()

sentry_sdk.init(
        dsn=os.getenv("SENTRY_KEY"),
        enable_tracing=True,
        shutdown_timeout=5,
        debug=False
    )

if __name__ == '__main__':
    application = app()
