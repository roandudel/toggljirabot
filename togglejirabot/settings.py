import os

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
TELEGRAM_CHAT_ID = int(os.getenv('TELEGRAM_CHAT_ID'))

TOGGL_API_TOKEN = os.getenv('TOGGL_API_TOKEN')
TOGGL_WORKSPACE_ID = os.getenv('TOGGL_WORKSPACE_ID')

MESSAGE_TEMPLATE_DAILY_REPORT = '<b>🔥 Daily Report\n</b>'
MESSAGE_TEMPLATE_NO_PROJECT_ASSIGNED = '\n ⚡ Projekt nicht angegeben: \n'
MESSAGE_TEMPLATE_NO_DESCRIPTION = '\n 🥺 Keine Beschreibung: \n'
MESSAGE_TEMPLATE_TIME_WORKED = '\n ⏲️ Arbeitszeit:'
