import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN', 1)
TELEGRAM_CHAT_ID = int(os.getenv('TELEGRAM_CHAT_ID', 1))

TOGGL_BASE_URL = os.getenv('TOGGL_BASE_URL', 'https://api.track.toggl.com/api')
TOGGL_API_TOKEN = os.getenv('TOGGL_API_TOKEN', 1)
TOGGL_WORKSPACE_ID = os.getenv('TOGGL_WORKSPACE_ID', 1)

JIRA_BASE_URL = os.getenv('JIRA_BASE_URL', 'https://jira.test.de')
