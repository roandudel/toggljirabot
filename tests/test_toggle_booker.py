from togglejirabot.toggle.booker import *
from togglejirabot.toggle.booker import ToggleReportBookerReport
from togglejirabot.toggle.project import Project

PROJECTS = Projects().from_projects_list([Project(1, 'Orga - ORG-1'),
                                          Project(2, 'Neues Project')])

TIMEENTRIES = [TimeEntry(1, 1, 'Dies gemacht', 3600),
               TimeEntry(2, 1, 'Jenes gemacht', 3600),
               TimeEntry(3, 2, 'PRO-2: Was ganz anderes gemacht', 3600),
               TimeEntry(4, 2, 'PRO-2: Was ganz anderes gemacht', 3600),
               TimeEntry(5, 2, 'NEW-3: Feature', 3300),
               TimeEntry(5, 2, 'NEW-4: Feature', 1500)
               ]


def test_toggle_booker():
    bookers_dict = booker(PROJECTS, TIMEENTRIES)
    assert bookers_dict['PRO-2']['duration'] == 7200


def test_toggle_booker_hours():
    bookers_dict = booker(PROJECTS, TIMEENTRIES)
    bookers_dict_hours = booker_in_hours(bookers_dict)

    assert bookers_dict_hours['PRO-2']['duration_in_hours'] == 2.0


def test_toggle_booker_rounded():
    bookers_dict = booker(PROJECTS, TIMEENTRIES)
    bookers_dict_hours = booker_in_hours(bookers_dict)
    bookers_dict_rounded = booker_rounded(bookers_dict_hours, 0.25)

    assert bookers_dict_rounded['NEW-3']['duration_in_hours_rounded'] == 1.0
    assert bookers_dict_rounded['NEW-4']['duration_in_hours_rounded'] == 0.5


def test_toggle_booker_report():
    trbr = ToggleReportBookerReport()
    timeentries = TimeEntries()
    timeentries.timeentries = TIMEENTRIES
    message = trbr.prepare_message(PROJECTS, timeentries, 1)

    print(message)


def test_project_without_ticket_with_multiple_entries():
    trbr = ToggleReportBookerReport()
    timeentries = TimeEntries()

    projects = Projects().from_projects_list([Project(1, 'Team A')])
    timeentries.timeentries = [TimeEntry(1, 1, 'PR-1: Feature A', 3600),
                               TimeEntry(2, 1, 'PR-1: Feature B', 3600)]

    message = trbr.prepare_message(projects, timeentries, 1)
    print(message)
