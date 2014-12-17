from django.shortcuts import render, get_object_or_404
from pull_requests.models import PR, Run
from django.conf import settings


def index(request):
    prs = PR.objects.all().order_by('-number')
    return render(request, 'index.html', {'prs': prs, 'artifact_ip': settings.ARTIFACT_IP})


def pr_detail(request, pr_number):
    pr = get_object_or_404(PR, pk=pr_number)
    return render(request, 'pr_detail.html', {'pr': pr, 'artifact_ip': settings.ARTIFACT_IP})


def run_detail(request, run_number):
    run = get_object_or_404(Run, pk=run_number)
    return render(request, 'run_detail.html', {'run': run, 'artifact_ip': settings.ARTIFACT_IP})


def retest(request, pr_number):
    run = Run.objects.all().filter(pr__number=pr_number).order_by('-datestamp')[0]
    run.retest = True
    run.save()
    return index(request)
