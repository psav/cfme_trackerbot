#!/usr/bin/env python
from datetime import datetime
import os
import requests
from utils.conf import docker

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from pull_requests.models import PR, Run, Task
from provider_templates.models import Group
from django.core.exceptions import ObjectDoesNotExist
print PR.objects.all()
docker['gh_token']
token = docker['gh_token']
owner = "RedHatQE"
repo = "cfme_tests"


def perform_request(url):
    out = {}
    if token:
        headers = {'Authorization': 'token {}'.format(token)}
        r = requests.get("https://api.github.com/repos/{}/{}/{}".format(owner,
                                                                        repo, url), headers=headers)
        out = r.json()
    return out


def create_run(db_pr, pr):
    new_run = Run(pr=db_pr,
                  result="pending",
                  datestamp=datetime.now(),
                  commit=pr['head']['sha'])
    new_run.save()
    for stream in Group.objects.all():
        template = stream.latest_template
        if template:
            new_task = Task(run=new_run,
                            output="",
                            result="pending",
                            template=template)
            new_task.save()


def check_prs():
    json = perform_request('pulls'.format(owner, repo))
    for pr in json:
        check_pr(pr)


# For simulation only
def run_tasks():
    for task in Task.objects.all().filter(result="pending"):
        task.result = "passed"
        task.save()


def check_runs():
    for run in Run.objects.all().exclude(result="passed").exclude(result="failed"):
        results = [task.result for task in Task.objects.all().filter(run=run)]
        if not "pending" in results:
            all_passed = all([result == "passed" for result in results])
            print all_passed, results
            if all_passed:
                run.result = "passed"
            else:
                run.result = "failed"
        run.save()
        pr = run.pr
        pr.state = run.result
        pr.save()


def check_pr(pr):
    print pr['number']
    labels = []
    raw_labels = perform_request("issues/{}/labels".format(pr['number']))

    for label in raw_labels:
        labels.append(label['name'])

    commit = pr['head']['sha']
    try:
        db_pr = PR.objects.get(number=pr['number'])
        if db_pr.current_commit_head != commit and \
           "WIP" not in labels:
                try:
                    Run.objects.get(pr=db_pr, commit=commit)
                except ObjectDoesNotExist:
                    create_run(db_pr, pr)
        elif "WIP" in labels:
            db_pr.state = "wip"
        #db_pr.current_commit_head = commit
        db_pr.save()
    except ObjectDoesNotExist:
        new_pr = PR(number=pr['number'],
                    description=pr['body'],
                    current_commit_head=commit,
                    state="untested")
        new_pr.save()
        if "WIP" not in labels:
            create_run(new_pr, pr)
        elif "WIP" in labels:
            new_pr.state = "wip"
        new_pr.save()

check_prs()
run_tasks()
check_runs()
