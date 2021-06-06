from marshmallow import EXCLUDE, Schema, fields, post_load


class Project:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Project: {self.id} {self.name}"


class ProjectSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True)

    @post_load
    def make_project(self, data, **kwargs):
        return Project(**data)


class Projects:
    def __init__(self):
        self.projects_dict = dict()

    def __contains__(self, item):
        if item in self.projects_dict:
            return True
        else:
            return False

    def from_json(self, json):
        schema = ProjectSchema(many=True)
        result = schema.load(json, unknown=EXCLUDE)

        for project in result:
            self.projects_dict[project.id] = project

        return self
