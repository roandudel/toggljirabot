import logging

import pendulum
import togglwrapper

from togglejirabot.settings import (TOGGL_API_TOKEN, TOGGL_BASE_URL,
                                    TOGGL_WORKSPACE_ID)
from togglejirabot.toggle.checks import (
    compute_worktime, is_worktime_goal_achieved,
    timeentries_should_have_ticket_in_description,
    timeentries_without_assigned_project, timeentries_without_description)
from togglejirabot.toggle.messages import (
    MESSAGE_TEMPLATE_DAILY_REPORT, MESSAGE_TEMPLATE_GOAL_ACHIEVED,
    MESSAGE_TEMPLATE_GOAL_NOT_ACHIEVED, MESSAGE_TEMPLATE_NO_DESCRIPTION,
    MESSAGE_TEMPLATE_NO_PROJECT_ASSIGNED, MESSAGE_TEMPLATE_TIME_WORKED,
    MESSAGE_TEMPLATE_TIMEENTRY_SHOULD_HAVE_TICKET)
from togglejirabot.toggle.project import Projects
from togglejirabot.toggle.timeentry import TimeEntries


class ToggleDataFetcher:
    def __init__(self):
        self.toggl = togglwrapper.Toggl(api_token=TOGGL_API_TOKEN, base_url=TOGGL_BASE_URL)

    def fetch(self, start_date, end_date) -> (Projects, TimeEntries):
        projects_as_json = self.toggl.Workspaces.get_projects(TOGGL_WORKSPACE_ID)
        timeentries_as_json = self.toggl.TimeEntries.get(start_date=start_date, end_date=end_date)

        logging.debug(projects_as_json)
        logging.debug(timeentries_as_json)

        projects = Projects().from_json(json=projects_as_json)
        timeentries = TimeEntries().from_json(json=timeentries_as_json)

        return projects, timeentries


class ToggleDataFakeFetcher:
    def __init__(self, project_json, timeentries_json):
        self.project_json = project_json
        self.timeentries_json = timeentries_json

    def fetch(self, start_date, end_date) -> (Projects, TimeEntries):
        return Projects().from_json(json=self.project_json), TimeEntries().from_json(json=self.timeentries_json)


class ToggleReportMessagePreparer:
    def __init__(self):
        pass

    def prepare_message(self, projects: Projects, timeentries: TimeEntries, work_time_goal) -> str:
        mb = MessageBuilder(header=MESSAGE_TEMPLATE_DAILY_REPORT)
        work_time = compute_worktime(timeentries)
        mb.add_newline()

        mb.add_header(MESSAGE_TEMPLATE_TIME_WORKED + ' ' + str(work_time))

        if is_worktime_goal_achieved(work_time=work_time, worktime_goal=work_time_goal):
            mb.add_header(MESSAGE_TEMPLATE_GOAL_ACHIEVED.format(work_time_goal))
        else:
            mb.add_header(MESSAGE_TEMPLATE_GOAL_NOT_ACHIEVED.format(work_time_goal))

        mb.add_newline()
        mb.add_header(MESSAGE_TEMPLATE_NO_DESCRIPTION)

        twd = timeentries_without_description(timeentries)
        for t in twd:
            mb.add_item(t)

        mb.add_newline()
        mb.add_header(MESSAGE_TEMPLATE_NO_PROJECT_ASSIGNED)
        twap = timeentries_without_assigned_project(timeentries)
        for t in twap:
            mb.add_item(t.description)

        mb.add_newline()
        mb.add_header(MESSAGE_TEMPLATE_TIMEENTRY_SHOULD_HAVE_TICKET)

        tshtid = timeentries_should_have_ticket_in_description(projects, timeentries)
        for t in tshtid:
            mb.add_item(t.description)

        return mb.message()


class ToggleReport:
    def __init__(self, fetcher=ToggleDataFetcher(), message_preparer=ToggleReportMessagePreparer()):
        self.fetcher = fetcher
        self.preparer = message_preparer

    def _fetch_data(self, start, end):
        logging.debug(f"{start} {end}")
        return self.fetcher.fetch(start_date=start, end_date=end)

    def compute_date_period_corners(self, time, period):
        return time.start_of(period).to_atom_string(), time.end_of(period).to_atom_string()

    # TODO: Refactor today initialization?
    def today(self):
        today = pendulum.now("Europe/Berlin")
        return self.report_for_given_period('day', 8, today)

    def week(self):
        today = pendulum.now("Europe/Berlin")
        return self.report_for_given_period('week', 40, today)

    def last_week(self):
        today = pendulum.now("Europe/Berlin").subtract(days=7)
        return self.report_for_given_period('week', 40, today)

    def prepare_message(self, projects: Projects, timeentries: TimeEntries, work_time_goal) -> str:
        return self.preparer.prepare_message(projects, timeentries, work_time_goal)

    def report_for_given_period(self, period: str, work_time_goal: int, today):
        begin, end = self.compute_date_period_corners(today, period)
        projects, timeentries = self._fetch_data(begin, end)

        message = self.prepare_message(projects, timeentries, work_time_goal=work_time_goal)

        return message


class MessageBuilder:
    def __init__(self, header=""):
        self._message = header

    def add_header(self, text):
        self._message += f"\n{text}"

    def add_item(self, text):
        self._message += f"\n• {text}"

    def add_newline(self):
        self._message += "\n"

    def message(self):
        return self._message
