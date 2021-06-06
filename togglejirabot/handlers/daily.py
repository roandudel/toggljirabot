import togglwrapper
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from togglejirabot.decorators import security
from togglejirabot.settings import (MESSAGE_TEMPLATE_DAILY_REPORT,
                                    MESSAGE_TEMPLATE_NO_DESCRIPTION,
                                    MESSAGE_TEMPLATE_NO_PROJECT_ASSIGNED,
                                    MESSAGE_TEMPLATE_TIME_WORKED,
                                    TOGGL_API_TOKEN, TOGGL_WORKSPACE_ID)
from togglejirabot.toggle.model.project import Projects
from togglejirabot.toggle.model.timeentry import TimeEntries


def no_proj_assigned(timeentries, projects):
    message = ""
    for time_entry in timeentries:
        if time_entry.pid not in projects:
            message += f"• {time_entry.description} \n"

    return message


def no_description(timeentries, projects):
    message = ""

    for time_entry in timeentries:
        if not time_entry.description:
            if time_entry.pid in projects:
                message += f"• {projects.projects_dict[time_entry.pid].name} \n"
            else:
                message += "• Zeiteintrag ohne Beschreibung und Projekt \n"

    return message


@security
def command_daily(update: Update, context: CallbackContext):
    toggl = togglwrapper.Toggl(TOGGL_API_TOKEN)

    projects_in_workspace = toggl.Workspaces.get_projects(TOGGL_WORKSPACE_ID)
    projects = Projects().from_json(json=projects_in_workspace)

    timeentries_in_workspace = toggl.TimeEntries.get()
    timeentries = TimeEntries().from_json(json=timeentries_in_workspace)

    timeentries_in_workspace_today = toggl.TimeEntries.get(start_date='2021-06-01T15:00:00+02:00',
                                                           end_date='2021-06-02T15:00:00+02:00')
    timeentries_in_workspace_today_ = TimeEntries().from_json(json=timeentries_in_workspace_today)

    message_no_proj_assigned = no_proj_assigned(timeentries, projects)
    message_no_description = no_description(timeentries, projects)

    work_time = 0

    for t in timeentries_in_workspace_today_:
        if t.duration > 0:
            work_time += t.duration

    work_time_message = f"{work_time / 60.0 / 60.0}h \n"

    if work_time / 60.0 / 60.0 > 8:
        work_time_message += "✅ Du hast dein Ziel von 8 Stunden erreicht! \n"
    else:
        work_time_message += "❌ Du hast dein Ziel von 8 Stunden nicht erreicht! \n"

    message = MESSAGE_TEMPLATE_DAILY_REPORT + \
              MESSAGE_TEMPLATE_TIME_WORKED + \
              work_time_message + \
              MESSAGE_TEMPLATE_NO_PROJECT_ASSIGNED + \
              message_no_proj_assigned + \
              MESSAGE_TEMPLATE_NO_DESCRIPTION + \
              message_no_description

    update.effective_chat.send_message(message, parse_mode=ParseMode.HTML)
