from togglejirabot.toggle.checks import timeentries_without_assigned_project
from togglejirabot.toggle.timeentry import TimeEntry
from togglejirabot.toggle.togglereport import MessageBuilder


def test_message_builder():
    timeentries = [TimeEntry(1, None, 'Integrate cool feature', 1800),
                   TimeEntry(2, None, 'Second', 1600),
                   TimeEntry(3, 1, 'Integrate cool feature', 1600),
                   ]

    timeentries_list = timeentries_without_assigned_project(timeentries)

    mb = MessageBuilder(header='Timeentries without Project')
    for t in timeentries_list:
        mb.add_item(text=t.description)
    message = mb.message()

    assert message == '''Timeentries without Project
• Integrate cool feature
• Second'''
