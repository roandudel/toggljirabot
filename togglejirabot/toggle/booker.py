from typing import List

from togglejirabot.settings import JIRA_BASE_URL
from togglejirabot.toggle.project import Projects
from togglejirabot.toggle.timeentry import TimeEntries, TimeEntry
from togglejirabot.toggle.togglereport import MessageBuilder

from .checks import extract_ticket, has_ticket_in_text
from .messages import MESSAGE_TEMPLATE_BOOKER


def booker(projects: Projects, timeentries: List[TimeEntry]):
    bookers_dict = {}

    # TODO: REFACTOR THIS!
    for t in timeentries:
        # We only process tickets with projects
        if t.pid in projects:
            project = projects.projects_dict[t.pid]
            if has_ticket_in_text(project.name):
                ticket = extract_ticket(project.name)
                if ticket not in bookers_dict:
                    bookers_dict[ticket] = {'duration': t.duration, 'entries': [t.description]}
                else:
                    bookers_dict[ticket]['duration'] += t.duration
                    if t.description not in bookers_dict[ticket]['entries']:
                        bookers_dict[ticket]['entries'].append(t.description)
            else:
                ticket = extract_ticket(t.description)
                if ticket not in bookers_dict:
                    bookers_dict[ticket] = {'duration': t.duration, 'entries': [t.description]}
                else:
                    if t.description in bookers_dict[ticket]['entries']:
                        bookers_dict[ticket]['duration'] += t.duration
                    else:
                        bookers_dict[ticket]['entries'].append(t.description)
                        bookers_dict[ticket]['duration'] += t.duration

    return bookers_dict


def booker_in_hours(bookers_dict: dict) -> dict:
    for k, v in bookers_dict.items():
        bookers_dict[k]['duration_in_hours'] = bookers_dict[k]['duration'] / 3600
    return bookers_dict


def booker_rounded(bookers_dict: dict, resolution: float) -> dict:
    for k, v in bookers_dict.items():
        bookers_dict[k]['duration_in_hours_rounded'] = round(
            bookers_dict[k]['duration_in_hours'] / resolution) * resolution

    return bookers_dict


#    message = "<a href=\"https://jira.disy.net\">PRO-1: T</a>"

class ToggleReportBookerReport:
    def __init__(self):
        pass

    def as_url(self, ticket):

        return f"<a href=\"{JIRA_BASE_URL}/secure/CreateWorklog!default.jspa?key={ticket}\">{ticket}</a>"

    def prepare_message(self, projects: Projects, timeentries: TimeEntries, work_time_goal) -> str:
        bookers_dict = booker(projects, timeentries)
        bookers_dict_hours = booker_in_hours(bookers_dict)
        bookers_dict_rounded = booker_rounded(bookers_dict_hours, 0.25)

        mb = MessageBuilder(MESSAGE_TEMPLATE_BOOKER)
        mb.add_newline()

        for k, v in bookers_dict_rounded.items():
            message = f"{self.as_url(k)}: {bookers_dict_rounded[k]['duration_in_hours_rounded']}h"
            mb.add_header(message)
            for e in bookers_dict_rounded[k]['entries']:
                mb.add_item(e)

            mb.add_newline()

        return mb.message()
