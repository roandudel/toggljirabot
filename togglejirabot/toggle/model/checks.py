from togglejirabot.settings import MESSAGE_TEMPLATE_TIME_WORKED


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


def check_worktime(projects, timeentries, worktime_goal):
    work_time_message = ""
    work_time = 0

    for t in timeentries:
        if t.duration > 0:
            work_time += t.duration

    work_time_in_hours = work_time / 60.0 / 60.0

    if work_time_in_hours > worktime_goal:
        work_time_message += f"✅ Du hast dein Ziel von {worktime_goal} Stunden erreicht! \n"
    else:
        work_time_message += f"❌ Du hast dein Ziel von {worktime_goal} Stunden nicht erreicht! \n"

    return f"{MESSAGE_TEMPLATE_TIME_WORKED} {work_time_in_hours} \n{work_time_message}"
