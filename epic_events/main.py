from epic_events.controllers.click_app import app

import sentry_sdk
import os
from dotenv import load_dotenv


load_dotenv()

"""
sentry_sdk.init(
    dsn=os.getenv("SENTRY_KEY"),
    traces_sample_rate=1.0,
    attach_stacktrace=True,
    enable_tracing=True
)
"""

if __name__ == '__main__':
    application = app()






