function hubber_build_graphs(){
    url = base_url + 'api/group/?format=json&limit=3'
    $.getJSON(url, function( data ) {
	$.each(data['objects'],
	       function(key, val){
		   $( "<div>", {
		       "class": "col-md-4",
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
			       "style": "width:300px;height:150px;"
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

function hubber_jenkins_data(job_name){
    url = base_url + 'api/build/?format=json&stream__name='
    url += job_name
    url += '&order_by=-datestamp'

    $.getJSON(url, function( data ) {
	var nums = [];
	$.each(data['objects'], function(key, val){
	    percen = (val['passes'] / (val['passes'] + val['fails'])) * 100
	    nums.push([val['number'], percen])
	});
	$.plot("#"+job_name, [ nums ], {
	    yaxis: {
		min: 0,
		max: 100,
	    }
	});
    });

    url = base_url + 'api/build/?format=json&stream__name='
    url += job_name
    url += '&order_by=-datestamp&limit=5'

    $.getJSON(url, function( data ) {
	var items = [];
	$.each(data['objects'], function(key, val){
	    percen = (val['passes'] / (val['passes'] + val['fails'])) * 100
	    link = '<a href="' + jenkins_url + job_name + '/' + val['number'] + '/">' + val['number'] + '</a>'
	    items.push( '<li id="' + val['number'] + '">[' + link + '] : <em>' + percen.toFixed(2) + '%</em></li>' );
	});
	$( "<ul/>", {
	    "class": "my-new-list",
	    html: items.join( "" )
	}).appendTo( "#" + job_name + "-data");
    });
}

function hubber_latest_templates(){
    url = base_url + 'api/group/?format=json'

    $.getJSON(url, function( data ) {
	var items = [];
	$.each(data['objects'], function(key, val){
	    providers = val['latest_template_providers'].join(", ")
	    stream = val['name']
	    template_name = val['latest_template']
	    items.push( '<li id="' + template_name + '"><strong>' + stream + '</strong>: ' + template_name + ' on <em>(' + providers + ')</em></li>' );
	});
	$("#templates").html(
	    $( "<ul/>", {
		"class": "my-new-list",
		html: items.join( "" )
	    })
	);
    }).fail(function(jqxhr, text_status, error) {
	$("#templates").html(
	    '<div class="alert alert-danger"><span class="pficon pficon-error-octagon"></span><span class="pficon pficon-error-exclamation"></span><strong>Trackerbot isn\'t talking today.</strong> ' + text_status + '</div>'
	)
    })
}

function hubber_sauce_jobs(){
    url = base_url + 'sauce_proxy/rest/v1/$user$/jobs?limit=5&full=true'
    $.getJSON(url, function (data){
	var items = [];
	$.each(data, function(key, val){
	    errors = val['commands_not_successful']
	    browser = val['build']
	    //link = '<a href="' + jenkins_url + job_name + '/' + val['number'] + '/">' + val['number'] + '</a>'
	    items.push( '<tr><td>' + browser + '</td><td>' + errors + '</td></tr>' );
	});
	$("#sauce_data").html(
	    $( "<table/>", {
		"class": "table table-bordered table-hover table-striped",
		html: items.join( "" )
	    })
	);
    }).fail(function(jqxhr, text_status, error) {
	$("#sauce_data").html(
	    '<div class="alert alert-danger"><span class="pficon pficon-error-octagon"></span><span class="pficon pficon-error-exclamation"></span><strong>I guess Sauce is having a bad day.</strong> ' + text_status + '</div>'
	)
    })
}

function hubber_prt_results(){
   url = base_url + 'api/task/?format=json&order_by=-datestamp&limit=5'
    $.getJSON(url, function (data){
	var items = [];
	$.each(data['objects'], function(key, val){
	    result = val['result']
	    tid = val['tid']
	    pr_number = val['pr_number']
	    stream = val['stream']
	    if (result == 'pending') {
		mclass = 'warning'
	    }
	    else if (result == 'failed') {
		mclass = 'danger'
	    }
	    else if (result == 'passed') {
		mclass = 'success'
	    }
	    else if (result == 'running') {
		mclass = 'info'
	    }
	    else{
		mclass = ''
	    }
	    //link = '<a href="' + jenkins_url + job_name + '/' + val['number'] + '/">' + val['number'] + '</a>'
	    items.push( '<tr class="' + mclass + '"><td><em>' + tid + '</em></td><td><strong>' + pr_number + '</strong></td><td>' + result + '</td><td>' + stream + '</td></tr>' );
	});
	$("#prt_data").html(
	    $( "<table/>", {
		"class": "table table-bordered table-hover",
		html: items.join( "" )
	    })
	)
    }).fail(function(jqxhr, text_status, error) {
	$("#prt_data").html(
	    '<div class="alert alert-danger"><span class="pficon pficon-error-octagon"></span><span class="pficon pficon-error-exclamation"></span><strong>Trackerbot isn\'t talking today.</strong> ' + text_status + '</div>'
	)
    });
}
