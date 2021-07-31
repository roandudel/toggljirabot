from typing import List

from togglejirabot.toggle.project import Projects
from togglejirabot.toggle.timeentry import TimeEntry

from .regexp import JIRA_TICKET_RE


def timeentries_without_assigned_project(timeentries: List[TimeEntry]) -> List[TimeEntry]:
    entries = []
    for time_entry in timeentries:
        if time_entry.pid is None:
            entries.append(time_entry)

    return entries


def timeentries_without_description(timeentries: List[TimeEntry]) -> List[TimeEntry]:
    entries = []

    for time_entry in timeentries:
        if not time_entry.has_description():
            entries.append(time_entry)

    return entries


def compute_worktime(timeentries: List[TimeEntry], hours=True) -> int:
    """ Compute work time in seconds."""
    worked_time = sum(te.duration for te in timeentries)
    if hours:
        return worked_time / 60.0 / 60.0
    return worked_time


def is_worktime_goal_achieved(work_time: float, worktime_goal: int) -> bool:
    """ Check if planned worktime is achieved
    :param worktime_goal: Work time goal in hours
    """
    if work_time < worktime_goal:
        return False
    return True


def has_ticket_in_text(text):
    if JIRA_TICKET_RE.search(text):
        return True
    return False


def extract_ticket(text):
    ticket = JIRA_TICKET_RE.search(text)
    if ticket:
        return ticket.group(0)
    return text


def timeentries_without_ticket(timentries: List[TimeEntry]) -> List[TimeEntry]:
    entries = []

    for time_entry in timentries:
        if not has_ticket_in_text(time_entry.description):
            entries.append(time_entry)

    return entries


def timeentries_should_have_ticket_in_description(projects: Projects, timeentries: List[TimeEntry]):
    entries = []

    for time_entry in timeentries:
        if time_entry.pid in projects:
            project = projects.projects_dict[time_entry.pid]
            if has_ticket_in_text(project.name):
                pass
            else:
                if not has_ticket_in_text(time_entry.description):
                    time_entry.description += f" -> {project.name}"
                    entries.append(time_entry)
        else:
            if not has_ticket_in_text(time_entry.description):
                entries.append(time_entry)

    return entries
