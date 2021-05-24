function show_bar(bar, only=false) {
	let bar_id = bar.bar_name + bar.suffix
	// console.log(bar);
	if($('#' + bar_id).length) {
		change_bar(bar_id, bar, only);
	} else {
		create_bar(bar_id, bar, only);
	}
}

function change_bar(bar_id, bar, only) {
	if($('#' + bar_id + '-desc').text() != bar.desc)
		$('#' + bar_id + '-desc').text(bar.desc);
	let progress_bar = document.getElementById(bar_id + '-progress');
	update_progress(progress_bar, bar.n, bar.initial, bar.total, bar.percentage, bar.colour);
	let rate = document.getElementById(bar_id + '-speed');
	update_rate(rate, bar_id, bar.rate, bar.primary_unit, bar.secondary_unit);
	if($('#' + bar_id + '-position').text() != bar.n)
		$('#' + bar_id + '-position').text(bar.n);
	if($('#' + bar_id + '-total').text() != bar.total)
		$('#' + bar_id + '-total').text(bar.total);
	if($('#' + bar_id + '-elapsed').text() != bar.elapsed_str)
		$('#' + bar_id + '-elapsed').text(bar.elapsed_str);
	if($('#' + bar_id + '-remain').text() != bar.remaining_str)
		$('#' + bar_id + '-remain').text(bar.remaining_str);
	if($('#' + bar_id + '-eta').text() != bar.eta)
		$('#' + bar_id + '-eta').text(bar.eta);
	if(only && bar.finished) {
		$('#' + bar_id + '-eta-li').remove();
		create_finished($('#' + bar_id + '-ulist'), bar_id, bar.end_time_str);
	} else if(only) {
		create_eta($('#' + bar_id + '-ulist'), bar_id, bar.eta);
		$('#' + bar_id + '-end-li').remove();
		$('#' + bar_id + '-end-msg-li').remove();
	}
}

function create_bar(bar_id, bar, only = false) {
	// The card
	let col = document.createElement('div');
	col.setAttribute('id', bar_id);
	col.setAttribute('class', 'col');
	let card = document.createElement('div');
	card.setAttribute('class', 'card mb-4 rounded-3 shadow-sm');
	col.append(card);
	if(!only) {
		// The card header
		let header_card = document.createElement('div');
		header_card.setAttribute('class', 'card-header py-3');
		card.append(header_card);
		let header = document.createElement('h4');
		header.setAttribute('id', bar_id + '-title');
		header.setAttribute('class', 'my-0 fw-normal');
		header.textContent = bar_id;
		header_card.append(header);
	}
	// The card body
	let body = document.createElement('div');
	body.setAttribute('class', 'card-body');
	card.append(body);
	// The bar description
	let desc = document.createElement('p');
	desc.setAttribute('id', bar_id + '-desc');
	desc.textContent = bar.desc;
	body.append(desc);
	// The bar progress
	let progress_div = document.createElement('div');
	progress_div.setAttribute('class', 'progress');
	progress_div.style.height = '30px';
	body.append(progress_div);
	let progress_bar = document.createElement('div');
	progress_bar.setAttribute('id', bar_id + '-progress');
	progress_bar.setAttribute('class', 'progress-bar progress-bar-striped');
	progress_bar.setAttribute('role', 'progressbar');
	progress_bar.setAttribute('role', 'progressbar');
	update_progress(progress_bar, bar.n, bar.initial, bar.total, bar.percentage, bar.colour);
	progress_div.append(progress_bar);
	// The speed info
	let speed = document.createElement('h2');
	create_rate(speed, bar_id, bar.rate, bar.primary_unit, bar.secondary_unit);
	body.append(speed);
	// The position, elapsed and remain information
	let ulist = document.createElement('ul');
	ulist.setAttribute('id', bar_id + '-ulist');
	ulist.setAttribute('class', 'list-unstyled mt-3 mb-4');
	body.append(ulist);
	let position = document.createElement('li');
	position.innerHTML = '<b>Position:</b> <span id="' + bar_id + '-position">' + bar.n + '</span>/<span id="' + bar_id + '-total">' + bar.total + '</span>';
	ulist.append(position);
	let elapsed = document.createElement('li');
	elapsed.innerHTML = '<b>Elapsed:</b> <span id="' + bar_id + '-elapsed">' + bar.elapsed_str + '</span>';
	ulist.append(elapsed);
	let remain = document.createElement('li');
	remain.innerHTML = '<b>Remain:</b> <span id="' + bar_id + '-remain">' + bar.remaining_str + '</span>';
	ulist.append(remain);
	if(only) {
		let start = document.createElement('li');
		start.innerHTML = '<b>Started:</b> <span id="' + bar_id + '-start">' + bar.start_time_str + '</span>';
		ulist.append(start);
		if(bar.finished) {
			create_finished(ulist, bar_id, bar.end_time_str);
		} else {
			create_eta(ulist, bar_id, bar.eta);
		}
	}
	// The buttons
	if(!only) {
		// The button to a specific bar progress
		let see_btn = document.createElement('a');
		see_btn.setAttribute('type', 'button');
		see_btn.setAttribute('class', 'w-100 btn btn-lg btn-outline-success');
		see_btn.setAttribute('href', $SCRIPT_ROOT + '/bar/' + bar_id);
		see_btn.textContent = 'Details';
		body.append(see_btn);
		// The close button
		let close_btn = document.createElement('a');
		close_btn.setAttribute('onclick', 'remove_bar("' + bar_id + '")');
		close_btn.setAttribute('type', 'button');
		close_btn.setAttribute('class', 'btn p-0 position-absolute top-0 right-4');
		close_btn.innerHTML = '<span>&times;</span>';
		body.append(close_btn);
	}
	$('#meters').prepend(col);
}

function create_finished(ulist, bar_id, end_time_str) {
	if(!$('#' + bar_id + '-end-msg').length) {
		let end = document.createElement('li');
		end.setAttribute('id', bar_id + '-end-li');
		end.innerHTML = '<b>Finished:</b> <span id="' + bar_id + '-end">' + end_time_str + '</span>';
		ulist.append(end);
		let finished = document.createElement('li');
		finished.setAttribute('id', bar_id + '-end-msg-li');
		finished.innerHTML = '<h2 id="' + bar_id + '-end-msg">Finished</h2>';
		ulist.append(finished);
	}
}

function create_eta(ulist, bar_id, eta_value) {
	if(!$('#' + bar_id + '-eta').length) {
		let eta = document.createElement('li');
		eta.setAttribute('id', bar_id + '-eta-li');
		eta.innerHTML = '<b>ETA:</b> <span id="' + bar_id +'-eta">' + eta_value + '</span>';
		ulist.append(eta);
	}
}

function update_progress(progress_bar, n, initial, total, percentage, colour) {
	percentage = Math.round(percentage);
	if(progress_bar.getAttribute("aria-valuenow") != n)
		progress_bar.setAttribute('aria-valuenow', n);
	if(progress_bar.getAttribute("aria-valuemin") != initial)
		progress_bar.setAttribute('aria-valuemin', initial);
	if(progress_bar.getAttribute("aria-valuemax") != total)
		progress_bar.setAttribute('aria-valuemax', total);
	if(progress_bar.style.width != percentage + '%')
		progress_bar.style.width = percentage + '%';
	if(progress_bar.textContent != percentage + '%')
		progress_bar.textContent = percentage + '%';
	if(colour && progress_bar.style.backgroundColor != colour) {
		progress_bar.style.backgroundColor = colour;
	}
}

function create_rate(elem, bar_name, rate_value, primary_unit_value, secondary_unit_value) {
	elem.setAttribute('id', bar_name + '-speed');
	elem.setAttribute('class', 'card-title pricing-card-title');
	elem.textContent = Math.round(rate_value * 100) / 100;
	let primary_unit = document.createElement('span');
	primary_unit.setAttribute('id', bar_name + '-primary-unit');
	primary_unit.textContent = primary_unit_value
	elem.append(primary_unit);
	let secondary_unit = document.createElement('small');
	secondary_unit.setAttribute('id', bar_name + '-secondary-unit');
	secondary_unit.setAttribute('class', 'text-muted fw-light');
	secondary_unit.textContent = '/' + secondary_unit_value;
	elem.append(secondary_unit);
}

function update_rate(elem, bar_name, rate_value, primary_unit, secondary_unit) {
	rate = Math.round(rate_value * 100) / 100;
	if(elem.childNodes[0].textContent != rate)
		elem.childNodes[0].textContent = rate;
	if(elem.childNodes[1].textContent != primary_unit)
		elem.childNodes[1].textContent = primary_unit;
	if(elem.childNodes[2].textContent != '/' + secondary_unit)
		elem.childNodes[2].textContent = '/' + secondary_unit;
}

function show_bars(bars) {
	// Update or create the bars
    bars.forEach(e => show_bar(e));
    // Remove the completed bars
	let cards = $('#meters').children();
	for(let i=0; i < cards.length; i++) {
		if(!exist_bar(cards[i].getAttribute('id'), bars)) {
			cards[i].remove();
		}
	}
}

function exist_bar(id, bars) {
	for(i=0; i < bars.length; i++) {
		let bar_id = bars[i].bar_name + bars[i].suffix;
		if(id === bar_id) {
		 	return true
		}
	}
	return false;
}

function update_bars() {
    $.ajax({
    	url: $SCRIPT_ROOT + "/tqdm",
    	success: function(data){
    		hide_error();
    		show_bars(data.bars);
    		hide_loading();
    	},
    	error: function(jqXHR, textStatus, errorThrown) {
    		hide_loading();
    		show_error(jqXHR.responseText);
    	}
    });
}

function update_bar(bar_id, only = false) {
    $.ajax({
    	url: $SCRIPT_ROOT + "/tqdm/" + bar_id,
    	success: function(data) {
    		hide_error();
    		show_bar(data, only);
    		hide_loading();
    	},
    	error: function(jqXHR, textStatus, errorThrown){
    		hide_loading();
    		show_error(jqXHR.responseText);
    	}
    });
}

function remove_bar(bar_id) {
	$.ajax({
    	url: $SCRIPT_ROOT + "/remove/" + bar_id,
    	success: function(data) {
    		hide_error();
			$("#" + bar_id).remove();
    	},
    	error: function(jqXHR, textStatus, errorThrown) {
    		show_error(jqXHR.responseText);
    	}
    });
}

function show_error(msg) {
	let error = $('#error-msg');
	error.text(msg);
	error_section = $('#error-section');
	error_section.removeClass('d-none');
	error_section.addClass('d-block');
}

function hide_error() {
	error_section = $('#error-section');
	error_section.removeClass('d-block');
	error_section.addClass('d-none');
}

function hide_loading() {
	$('#loading-section').addClass('d-none');
}