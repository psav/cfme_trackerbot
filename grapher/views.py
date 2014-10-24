from django.http import HttpResponse, HttpResponseNotFound
from grapher.models import Build
import pygal
from pygal.style import DefaultStyle
from collections import defaultdict


def show_graph(request, stream_name):
    builds = Build.objects.filter(stream=stream_name).order_by('number')

    if not builds:
        return HttpResponseNotFound('No stream by that name')

    fields = ['number', 'fails', 'skips', 'passes']

    data = defaultdict(list)

    for build in builds:
        for field in fields:
            if field == 'number':
                # The run number is an int, but needs to be a str for the xlabel
                data[field].append(str(getattr(build, field)))
            else:
                data[field].append(getattr(build, field))

    style = DefaultStyle
    style.colors = ('#dc322f', '#b58900', '#2aa198')

    stackedbar_chart = pygal.StackedLine(fill=True, x_label_rotation=90, style=style)
    stackedbar_chart.title = stream_name
    stackedbar_chart.show_dots = False
    stackedbar_chart.x_labels = data['number']
    stackedbar_chart.show_minor_x_labels = False
    stackedbar_chart.x_labels_major_count = 20
    stackedbar_chart.x_title = "Run number"
    for a in fields:
        if a != 'number':
            stackedbar_chart.add(str(a), data[a])
    da = stackedbar_chart.render()

    response = HttpResponse(da, mimetype="image/svg+xml")
    return response
