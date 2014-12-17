// TODO: We should make this way better.
// http://stackoverflow.com/questions/9625366/generate-html-page-with-js-from-json

function hubber_build_url(resource_name, query_params) {
    // Pretty naive, it's on the caller to make sure resource_name is a string and query_params is a mapping
    query_params = query_params || {}; // if this is undef/falsy, make it an object so param doesn't explode
    query_params.format = "json";
    return base_url + "api/" + resource_name + "/?" + $.param(query_params);
}

function hubber_trackerbot_fail(jqxhr, text_status, error) {
    $("#templates").html(
        '<div class="alert alert-danger"><span class="pficon pficon-error-octagon"></span><span class="pficon pficon-error-exclamation"></span><strong>Trackerbot isn\'t talking today.</strong> ' + text_status + '</div>'
    )
}

function hubber_build_graphs() {
    url = hubber_build_url("group", {
        limit: 3
    })
    $.getJSON(url, function(data) {
        num_obj = Object.keys(data['objects']).length
        offset = 12 / num_obj
        width = 1000 / num_obj
        $.each(data['objects'],
            function(key, val) {
                $("<div>", {
                    "class": "col-md-" + offset,
                }).append(
                    $("<div>", {
                        "class": "panel panel-default"
                    }).append(
                        $("<div>", {
                            "class": "panel-heading"
                        }).append(
                            $("<strong>", {
                                "class": "panel-title"
                            }).text("Jenkins - " + val['name'])
                        ),
                        $("<div>", {
                            "class": "panel-body",
                            "id": val['name'],
                            "style": "width:" + width + "px;height:150px;"
                        }),
                        $("<div>", {
                            "id": val['name'] + "-data",
                        })
                    )
                ).appendTo("#jenkins_graphs")
                hubber_jenkins_data(val['name']);
            });
    });
}

function hubber_jenkins_data(job_name) {
    url = hubber_build_url("build", {
        stream__name: job_name,
        order_by: "-datestamp"
    })

    $.getJSON(url, function(data) {
        var nums = [];
        $.each(data['objects'], function(key, val) {
            percen = (val['passes'] / (val['passes'] + val['fails'])) * 100
            nums.push([val['number'], percen])
        });
        $.plot("#" + job_name, [nums], {
            yaxis: {
                min: 0,
                max: 100,
            }
        });
    });

    url = hubber_build_url("build", {
        stream__name: job_name,
        order_by: "-datestamp",
        limit: 5
    })

    $.getJSON(url, function(data) {
        var items = [];
        $.each(data['objects'], function(key, val) {
            percen = (val['passes'] / (val['passes'] + val['fails'])) * 100
            link = '<a href="' + jenkins_url + job_name + '/' + val['number'] + '/">' + val['number'] + '</a>'
            items.push('<li id="' + val['number'] + '">[' + link + '] : <em>' + percen.toFixed(2) + '%</em></li>');
        });
        $("<ul/>", {
            "class": "my-new-list",
            html: items.join("")
        }).appendTo("#" + job_name + "-data");
    });
}

function hubber_latest_templates() {
    url = hubber_build_url("group")

    $.getJSON(url, function(data) {
        var items = [];
        $.each(data['objects'], function(key, val) {
            providers = val['latest_template_providers'].join(", ")
            stream = val['name']
            template_name = val['latest_template']
            items.push('<li id="' + template_name + '"><strong>' + stream + '</strong>: ' + template_name + ' on <em>(' + providers + ')</em></li>');
        });
        $("#templates").html(
            $("<ul/>", {
                "class": "my-new-list",
                html: items.join("")
            })
        );
    }).fail(hubber_trackerbot_fail);
}

function hubber_retest_templates() {
    // In addition to the basic latest templates view, get all the providers and template we know about for bulk and individual retesting
    var providers = $.getJSON(hubber_build_url('provider'), {
        limit: 1000
    }, function(data) {
        var retest_providers_container = $("<div>");
        $.each(data['objects'], function(key, val) {
            var provider_key = val['key']
            var retest_a = $("<a class='btn btn-danger center-block' href='#' class='text-info'>")
                // In this, and other retest anchors, add a click handler so we can get the view output in a nice modal
            retest_a.click({
                provider_key: provider_key,
                template_name: 'all'
            }, hubber_retest_click_handler)
            retest_providers_container.append($("<p>").append(retest_a.append(provider_key)))
        });
        $("#retest-providers").html(retest_providers_container);
    }).fail(hubber_trackerbot_fail);
    templates = $.getJSON(hubber_build_url('template'), {
        limit: 1000
    }, function(data) {
        retest_templates_container = $("<div>");
        $("#retest-templates").html(retest_templates_container);
        var template_columns = 3
        for (var i = 0; i < template_columns; i++) {
            // TODO: Base column width on template_columns
            retest_templates_container.append("<div id='retest_templates_column_" + i + "' class='col-md-4' style='padding-right: 3em;'>")
        }
        var counter = 0;
        $.each(data['objects'], function(key, val) {
            var template_name = val['name']
            var template_panel = $("<div class='panel panel-default'>");
            template_panel.append($("<div class='panel-heading'>").append("<h3 class='panel-title'>" + template_name + "</h3>"))
            var template_providers = $("<table class='table table-hover'>")
            template_panel.append(template_providers)
            $.each(val['providers'], function(index, provider_key) {
                if ($.inArray(provider_key, val['usable_providers']) != -1) {
                    var template_provider_row = $("<tr class='success'>")
                    var glyph = $("<td class='pficon pficon-ok' title='Usable'>")
                    var retest_a = $("<a href='#' class='text-success'>Retest</a>")
                    var mark_a = $("<a href='#' class='text-success'>Mark Unusable</a>")
                    var mark = 'unusable'
                } else {
                    var template_provider_row = $("<tr class='danger'>")
                    var glyph = $("<td class='pficon pficon-close text-danger' title='Unusable'>")
                    var retest_a = $("<a href='#' class='text-danger'>Retest</a>")
                    var mark_a = $("<a href='#' class='text-success'>Mark Usable</a>")
                    var mark = 'usable'
                }
                retest_a.click({
                    provider_key: provider_key,
                    template_name: template_name
                }, hubber_retest_click_handler)
                mark_a.click({
                    usable: mark,
                    provider_key: provider_key,
                    template_name: template_name
                }, hubber_mark_click_handler)
                template_provider_row.append(glyph)
                template_provider_row.append($("<td>").append(provider_key))
                template_provider_row.append($("<td>").append(retest_a))
                template_provider_row.append($("<td>").append(mark_a))
                template_providers.append(template_provider_row)
            })
            var retest_a = $("<a href='#' class='text-info'>Retest on all providers</a>")
            retest_a.click({
                provider_key: "all",
                template_name: template_name
            }, hubber_retest_click_handler)
            var all_providers_row = $("<tr class='info'>")
            all_providers_row.append($("<td class='pficon pficon-refresh text-info'/>"))
            all_providers_row.append($("<td colspan=3>").append(retest_a))
            template_providers.append(all_providers_row)
            $("#retest_templates_column_" + counter++ % template_columns).append($("<div class='row'>").append(template_panel))
        });
    }).fail(hubber_trackerbot_fail);
}

function hubber_retest_click_handler(event) {
    // TODO: We have some z-order issues with .modal-backdrop, so hackery is employed here that should replaced with good code
    // The hackery is that we need the modal dialog to exist before we can set its z-index (backdrop is at 1040),
    // so we show the modal before getting its contents, allowing that GET request to serve as a delay for the modal to appear
    // allowing us to set the z-order. Ideally, of course, the modal would "just work".
    var retest_url = base_url + "template/retest/" + event.data.provider_key + "/" + event.data.template_name
    $("#templateUpdateResponse .modal-body").html('<div class="spinner spinner-xs spinner-inline"></div><strong>Loading...</strong>');
    $("#templateUpdateResponse").modal('show');
    $.get(retest_url, function(data) {
        $("#templateUpdateResponse .modal-body").html(data);
    });
    $(".modal-dialog").css("z-index", "1041");
}

function hubber_mark_click_handler(event) {
    // same z-order issue comment as in the retest click handler. Also, it would be easy to combine the two functions
    var mark_url = base_url + "template/mark/" + event.data.usable + "/" + event.data.provider_key + "/" + event.data.template_name
    $("#templateUpdateResponse .modal-body").html('<div class="spinner spinner-xs spinner-inline"></div><strong>Loading...</strong>');
    $("#templateUpdateResponse").modal('show');
    $.get(mark_url, function(data) {
        $("#templateUpdateResponse .modal-body").html(data);
    });
    $(".modal-dialog").css("z-index", "1041");
}

function hubber_sauce_jobs() {
    url = sauce_proxy + 'rest/v1/$user$/jobs?limit=5&full=true'

    $.getJSON(url, function(data) {
        var items = [];
        $.each(data, function(key, val) {
            errors = val['commands_not_successful']
            browser = val['build']
                //link = '<a href="' + jenkins_url + job_name + '/' + val['number'] + '/">' + val['number'] + '</a>'
            items.push('<tr><td>' + browser + '</td><td>' + errors + '</td></tr>');
        });
        $("#sauce_data").html(
            $("<table/>", {
                "class": "table table-bordered table-hover table-striped",
                html: items.join("")
            })
        );
    }).fail(hubber_trackerbot_fail)
}

function hubber_prt_results() {
    url = hubber_build_url("task", {
        order_by: "-datestamp",
        limit: 5
    })

    $.getJSON(url, function(data) {
        var items = [];
        $.each(data['objects'], function(key, val) {
            result = val['result']
            tid = val['tid']
            pr_number = val['pr_number']
            stream = val['stream']
            if (result == 'pending') {
                mclass = 'warning'
            } else if (result == 'failed') {
                mclass = 'danger'
            } else if (result == 'passed') {
                mclass = 'success'
            } else if (result == 'running') {
                mclass = 'info'
            } else {
                mclass = ''
            }
            //link = '<a href="' + jenkins_url + job_name + '/' + val['number'] + '/">' + val['number'] + '</a>'
            items.push('<tr class="' + mclass + '"><td><em>' + tid + '</em></td><td><strong>' + pr_number + '</strong></td><td>' + result + '</td><td>' + stream + '</td></tr>');
        });
        $("#prt_data").html(
            $("<table/>", {
                "class": "table table-bordered table-hover",
                html: items.join("")
            })
        )
    }).fail(hubber_trackerbot_fail);
}
