import logging

import pendulum
import togglwrapper

from togglejirabot.settings import (MESSAGE_TEMPLATE_DAILY_REPORT,
                                    MESSAGE_TEMPLATE_NO_DESCRIPTION,
                                    MESSAGE_TEMPLATE_NO_PROJECT_ASSIGNED,
                                    TOGGL_API_TOKEN, TOGGL_WORKSPACE_ID)
from togglejirabot.toggle.model.checks import (check_worktime, no_description,
                                               no_proj_assigned)
from togglejirabot.toggle.model.project import Projects
from togglejirabot.toggle.model.timeentry import TimeEntries


class ToggleReport:
    def __init__(self):
        self.toggl = togglwrapper.Toggl(TOGGL_API_TOKEN)

    def _fetch_data(self, start, end, work_time_goal):
        logging.debug(f"{start} {end} {work_time_goal}")

        projects = Projects().from_json(json=self.toggl.Workspaces.get_projects(TOGGL_WORKSPACE_ID))

        timeentries_ = TimeEntries().from_json(json=self.toggl.TimeEntries.get(start_date=start,
                                                                               end_date=end))
        message_no_proj_assigned = no_proj_assigned(timeentries_, projects)
        message_no_description = no_description(timeentries_, projects)

        work_time_message = check_worktime(projects, timeentries_, worktime_goal=work_time_goal)

        message = MESSAGE_TEMPLATE_DAILY_REPORT + \
                  work_time_message + \
                  MESSAGE_TEMPLATE_NO_PROJECT_ASSIGNED + \
                  message_no_proj_assigned + \
                  MESSAGE_TEMPLATE_NO_DESCRIPTION + \
                  message_no_description

        return message

    def compute_date_period_corners(self, time, period):
        return (time.start_of(period).to_atom_string(), time.end_of('week').to_atom_string())

    def today(self):
        today = pendulum.now("Europe/Berlin")
        begin, end = self.compute_date_period_corners(today, 'day')
        message = self._fetch_data(begin, end, work_time_goal=8)

        return message

    def week(self):
        today = pendulum.now("Europe/Berlin")

        begin, end = self.compute_date_period_corners(today, 'week')
        message = self._fetch_data(begin, end, work_time_goal=40)

        return message
