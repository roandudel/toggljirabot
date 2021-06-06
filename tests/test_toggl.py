import togglwrapper

from togglejirabot.settings import TOGGL_API_TOKEN
from togglejirabot.toggle.model.timeentry import TimeEntries


def test_timeentry():
    toggl = togglwrapper.Toggl(TOGGL_API_TOKEN)

    timeentries_in_workspace_today = toggl.TimeEntries.get(start_date='2021-06-01T15:00:00+02:00',
                                                           end_date='2021-06-02T15:00:00+02:00')
    timeentries = TimeEntries().from_json(json=timeentries_in_workspace_today)

    for t in timeentries:
        print(t.duration)

    assert True
