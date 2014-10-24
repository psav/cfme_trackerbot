from django.core.management.base import BaseCommand
from grapher.models import Build
from datetime import datetime
import os.path


def build_graph(stream_instance, import_dir):
    stream = stream_instance.name
    file_name = os.path.join(import_dir, '{}.tsc'.format(stream))
    with open(file_name) as f:
        data = f.readlines()

    fields = []
    for i in data[0].strip("\n").split("\t"):
        fields.append({'name': i, 'values': []})

    def func(elem, field):
        if "#" in elem:
            field['values'].append(elem)
        else:
            field['values'].append(int(elem))

    def get_values(field):
        for a in fields:
            if a['name'] == field:
                return a['values']

    for line in data[1:]:
        elems = line.strip("\n").split("\t")
        b = Build(number=elems[0].strip('#'), fails=elems[1], skips=elems[2],
                  passes=elems[3], datestamp=datetime.now(), stream=stream_instance)
        b.save()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('import_dir', type=str)

    def handle(self, *args, **options):
        from provider_templates.models import Group
        for stream in Group.objects.filter(stream=True):
            build_graph(stream, args[0])
