from marshmallow import EXCLUDE, Schema, fields, post_load


class TimeEntry:
    def __init__(self, id, pid, description, duration):
        self.id = id
        self.pid = pid
        self.description = description
        self.duration = duration

    def __repr__(self):
        return f"TimeEntry: {self.id} {self.description}"

    def has_description(self):
        return self.description != ''


class TimeEntrySchema(Schema):
    id = fields.Integer(required=True)
    pid = fields.Integer(required=False, missing=None)
    description = fields.Str(required=False, missing=None)
    duration = fields.Integer(required=True)

    @post_load
    def make_timeentry(self, data, **kwargs):
        return TimeEntry(**data)


class TimeEntries:
    def __init__(self):
        self.timeentries = list()

    def __iter__(self):
        for time_entry in self.timeentries:
            yield time_entry

    def from_json(self, json):
        schema = TimeEntrySchema(many=True)
        result = schema.load(json, unknown=EXCLUDE)

        self.timeentries = result

        return self
