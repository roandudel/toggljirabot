# Toggle Jira Bot

## Docker

```
docker run -d \
           --name tgj \
           -e TELEGRAM_API_TOKEN=${TELEGRAM_API_TOKEN} \
           -e TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID} \
           -e TOGGL_API_TOKEN=${TOGGL_API_TOKEN} \
           -e TOGGL_WORKSPACE_ID=${TOGGL_WORKSPACE_ID} \
           togglejirabot
```