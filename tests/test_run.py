from typing import List

from toggl import api, utils


def time_entries(toggl_config) -> List[api.TimeEntry]:
    return api.TimeEntry.objects.all(config=toggl_config)


# return api.TimeEntry.objects.current(config=toggl_config)


def test_one():
    toggl_config = utils.Config.factory(None)
    toggl_config.api_token = '57df23d7ddacd09464d1a92485910244'
    list_of_all_entries = time_entries(toggl_config)

    print(list_of_all_entries.project)

    for entry in list_of_all_entries:
        e_dict = entry.to_dict()
        print(f"{entry.project} {e_dict['description']}")

    assert True
