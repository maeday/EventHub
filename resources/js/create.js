$(document).ready(function(){

	$(".datepicker").datepicker({ minDate:new Date() });
		
	$("#picker-1").click(function() {
    	$("#input-startdate").focus();
    });
    $("#picker-2").click(function() {
    	$("#input-enddate").focus();
    });
    
    $("#clockswitch-1").click(function() {
    	switch_clock($(this));
    });
    $("#clockswitch-2").click(function() {
    	switch_clock($(this));
    });
    
    $("#input-title").keyup(function() {
    	if ($(this).val() != "") {
			$("#ctrl-title").removeClass("error");
			$("#err-title").hide();
			return true;
		}
    });
    
    $("#input-description").keyup(function() {
    	if ($(this).val() != "") {
			$("#ctrl-description").removeClass("error");
			$("#err-description").hide();
			return true;
		}
    });
    
    $("#input-location").change(function() {
    	if ($(this).val() != -1) {
			$("#ctrl-location").removeClass("error");
			$("#err-location").hide();
			return true;
		}
    });
    
    $("#input-venue").keyup(function() {
    	if ($(this).val() != "") {
			$("#ctrl-venue").removeClass("error");
			$("#err-venue").hide();
			return true;
		}
    });
    
    $("#input-street").keyup(function() {
    	if ($(this).val() != "") {
			$("#ctrl-street").removeClass("error");
			$("#err-street").hide();
			return true;
		}
    });
    
    $("#input-startdate").blur(function() {
	    check_date($(this), $("#err-start"), $("#ctrl-start"));
    });
    $("#input-starttime").blur(function() {
	    check_time($(this), $("#err-start"), $("#ctrl-start"));
    });
    $("#input-enddate").blur(function() {
	    check_date($(this), $("#err-end"), $("#ctrl-end"));
    });
    $("#input-endtime").blur(function() {
	    check_time($(this), $("#err-end"), $("#ctrl-end"));
    });
    
    $("#input-startdate").change(function() {
	    $("#input-enddate").val($("#input-startdate").val());
    });
    
    $("#input-free").change(function() {
        disableCosts();
    });
    
    $("#publish").click(function() {
    	if (!check_all()) {
    		return false;
    	}
    	requestCreate();
    });
    	
});

function requestCreate() {
	var input_title = $("#input-title").val();
	var input_desc = $("#input-description").val();
	var input_poster = $("#user-id").val();
	var input_startdate = $("#input-startdate").val();
	var input_starttime = $("#input-starttime").val();
	var input_enddate = $("#input-enddate").val();
	var input_endtime = $("#input-endtime").val();
	var input_venue = $("#input-venue").val();
	var input_street = $("#input-street").val();
	var input_city = $("#input-city").val();
	var input_state = $("#input-state").val().toUpperCase();
	var input_zip = $("#input-zip").val();
	var input_url = $("#input-url").val();
	var input_image =  document.getElementById('input-photo').files[0];
	var input_cost_min = $("#input-cost-min").val();
	var input_cost_max = $("#input-cost-max").val();
	var input_free_checked = $("#input-free").is(':checked');
	var input_location = $("#input-location").val();
	var input_categories = $(".c-cat:checked").map(function() {
		return $(this).val();
	}).get();
	var input_categories_string = input_categories.join();
	
	if(input_categories_string==""){
		alert("Please choose at least 1 category.");
		return;
	}
	var start_clock = "am";
	if ($("#clockswitch-1").html() == "&nbsp;PM&nbsp;") { // if start clock is PM
		start_clock = "pm";
	}
	
	var end_clock = "am";
	if ($("#clockswitch-2").html() == "&nbsp;PM&nbsp;") { // if end clock is PM
		end_clock = "pm";
	}
	
	// Stringifies time variables. ex) "11/04/2012 04:15 pm"
	var start_str = input_startdate + " " + input_starttime + " " + start_clock;
	var end_str = input_enddate + " " + input_endtime + " " + end_clock;
	
	// Pass in 0, 1 values to controller for 'free'
	// If free, pass in non-blank dummy values for min and max cost
	if(input_free_checked) {
	    input_free_value = 1;
	    input_cost_min = "0";
	    input_cost_max = "0";
	} else {
	    input_free_value = 0;
	}
		
	var fd = new FormData();
	fd.append( 'image', input_image );
	fd.append( 'title', input_title );
	fd.append( 'poster', input_poster );
	fd.append( 'description', input_desc );
	fd.append( 'start', start_str );
	fd.append( 'end', end_str );
	fd.append( 'venue', input_venue );
	fd.append( 'street', input_street );
	fd.append( 'city', input_city );
	fd.append( 'state', input_state );
	fd.append( 'zip', input_zip );
	fd.append( 'url', input_url );
	fd.append( 'cost-min', input_cost_min );
	fd.append( 'cost-max', input_cost_max );
	fd.append( 'free', input_free_value );
	fd.append( 'location', input_location );
	fd.append( 'categories', input_categories_string );
	
	var request = $.ajax({
		url: "create_event",
		type: "POST",
		data: fd,
		processData: false,
	    contentType: false,
	    cache: false
	});
	
	// Regex that is used to determine if we get the event id (for page redirect)
        var isInt = /^\d+$/;
	
	request.done(function(msg) {
		// Basically check to see if we created the event or got an error.
		if (String(msg).search(isInt) != -1){
			$("#createEvent").modal('hide');
			window.location = "/event/" + String(msg);
		} else if(msg == "exists") {
			// If the event existed, we can ask the user if they want to overwrite
			// as it is better than denying them after entering info. 
			var choice = confirm("Event with similar name has already been created. Overwrite previous event details with entered information?");

			if (choice){
				// Overwrite so just call edit event function

				// TODO: Call edit event function in JS file or using Ajax request.
				// For now, just alert that we edited event and close event editing window.
				alert("Edited event!");
				$("#createEvent").modal('hide');
			}
		} else {
			// Error so just inform user of error.
			alert("Error: Could not create event");
		}
	});
	
	request.fail(function(jqXHR, textStatus) {
		alert("Ajax request failed: " + textStatus);
	});
}

// Checks for errors in the form.
function check_all() {
	return check_title() && check_times_comprehensive() && check_summary() && check_location() && check_venue() && check_street() && check_city() && check_state() && check_costs() && check_url();
}

function check_title() {
	if ($("#input-title").val() == "") {
		$("#ctrl-title").addClass("error");
		$("#err-title").text("You forgot the title!");
		$("#err-title").show();
		$("#input-title").focus();
		return false;
	} else {
		$("#ctrl-title").removeClass("error");
		$("#err-title").hide();
		return true;
	}
}

function check_times_comprehensive() {
	return check_date($("#input-startdate"), $("#err-start"), $("#ctrl-start")) && check_time($("#input-starttime"), $("#err-start"), $("#ctrl-start")) && check_date($("#input-enddate"), $("#err-end"), $("#ctrl-end")) 
		&& check_time($("#input-endtime"), $("#err-end"), $("#ctrl-end")) && check_time_logic();
}

function check_summary() {
	if ($("#input-description").val() == "") {
		$("#ctrl-description").addClass("error");
		$("#err-description").text("Please summarize the event.");
		$("#err-description").show();
		$("#input-description").focus();
		return false;
	} else {
		$("#ctrl-description").removeClass("error");
		$("#err-description").hide();
		return true;
	}
}

function check_location() {
	if ($("#input-location").val() == -1) {
		$("#ctrl-location").addClass("error");
		$("#err-location").text("Please select a neighborhood.");
		$("#err-location").show();
		$("#input-location").focus();
	    return false;
	} else {
		$("#ctrl-location").removeClass("error");
		$("#err-location").hide();
		return true;
	}
}

function check_date(input, err, ctrl) {
	var str = input.val();
	var errorMsg = validate_date(str);
	
	err.text(errorMsg);
	
	if (errorMsg != "") {
		ctrl.addClass("error");
		err.show();
		input.focus();
		return false;
	}
	
	err.hide();
	ctrl.removeClass("error");
	return true;
}

function check_time(input, err, ctrl) {
	var str = input.val();
	var errorMsg = validate_time(str);
	
	err.text(errorMsg);
	
	if (errorMsg != "") {
		ctrl.addClass("error");
		err.show();
		input.focus();
		return false;
	}
	
	err.hide();
	ctrl.removeClass("error");
	return true;
}

// Validates date format with Regex. Returns error message or empty string if no error.
function validate_date(str) {
	var allowBlank = false;
	var minYear = (new Date()).getFullYear() - 10; // current year
	var maxYear = minYear + 20;
	
	var errorMsg = "";
	
	re = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/;
	
	if (str != '') {
		if (regs = str.match(re)) {
			if (regs[1] < 1 || regs[1] > 12) {
				errorMsg = "Invalid month format: " + regs[1];
			} else if (regs[2] < 1 || regs[2] > 31) {
				errorMsg = "Invalid day format: " + regs[2];
			} else if (regs[3] < minYear || regs[3] > maxYear) {
				errorMsg = "Invalid year format: Date out of acceptable range";			}
		} else {
			errorMsg = "Invalid date format: " + str;
		}
	} else if (!allowBlank) {
		errorMsg = "You forgot the date!"
	}
	
	return errorMsg;
}

// Validates time format with Regex. Returns error message or empty string if no error.
function validate_time(str) {
	var errorMsg = "";
	
	re = /^(\d{1,2}):(\d{2})(:00)?$/;
	
	if (str != '') {
		if (regs = str.match(re)) {
			if (regs[1] < 1 || regs[1] > 12) {
				errorMsg = "Invalid hour format: " + regs[1];
			}
			if (!errorMsg && regs[2] > 59) {
				errorMsg = "Invalid minute format: " + regs[2];
			}
		} else {
			errorMsg = "Invalid time format: " + str;
		}
	}
	
	return errorMsg;
}

function check_time_logic() {
	// get start date
	re = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/;
	var str = $("#input-startdate").val();
	regs = str.match(re);
	var start_month = parseInt(regs[1], 10);
	var start_day = parseInt(regs[2], 10);
	var start_year = regs[3];
	
	// get end date
	str = $("#input-enddate").val();
	regs = str.match(re);
	var end_month = parseInt(regs[1], 10);
	var end_day = parseInt(regs[2], 10);
	var end_year = regs[3];
	
	// get start time
	re = re = /^(\d{1,2}):(\d{2})(:00)?$/;
	str = $("#input-starttime").val();
	regs = str.match(re);
	var start_hour = parseInt(regs[1], 10);
	var start_minute = parseInt(regs[2], 10);
	if ($("#clockswitch-1").html() == "&nbsp;PM&nbsp;" && start_hour != 12)
		start_hour += 12;
	if ($("#clockswitch-1").html() == "&nbsp;AM&nbsp;" && start_hour == 12)
		start_hour -= 12;
	
	// get end time
	str = $("#input-endtime").val();
	regs = str.match(re);
	var end_hour = parseInt(regs[1], 10);
	var end_minute = parseInt(regs[2], 10);
	if ($("#clockswitch-2").html() == "&nbsp;PM&nbsp;" && end_hour != 12)
		end_hour += 12;
	if ($("#clockswitch-2").html() == "&nbsp;AM&nbsp;" && end_hour == 12)
		end_hour -= 12;
	
	var start_date = new Date(start_year, start_month - 1, start_day, start_hour, start_minute, 0, 0);
	var end_date = new Date(end_year, end_month - 1, end_day, end_hour, end_minute, 0, 0);
	// side note ^ : months are zero-based
	var today = new Date();
	today.setHours(0);
	today.setMinutes(0);
	today.setSeconds(0);
	today.setMilliseconds(0);
	
	var errorMsg = "";
	
	if (start_date < today) {
		errorMsg = "Cannot use past date";
		$("#err-start").text(errorMsg);
		$("#err-start").show();
		$("#ctrl-start").addClass("error");
		//$("#input-startdate").focus();
		return false;
	} else if (end_date < start_date) {
		errorMsg = "Cannot finish before start";
		$("#err-end").text(errorMsg);
		$("#err-end").show();
		$("#ctrl-end").addClass("error");
		$("#input-endtime").focus();
		return false;
	} else {
		$("#err-start").hide();
		$("#ctrl-start").removeClass("error");
		$("#err-end").hide();
		$("#ctrl-end").removeClass("error");
		return true;
	}
}

function switch_clock(btn) {
	if (btn.html() == "&nbsp;AM&nbsp;") {
		btn.html("&nbsp;PM&nbsp;");
	} else {
		btn.html("&nbsp;AM&nbsp;");
	}
}

function check_venue() {
	if ($("#input-venue").val() == "") {
		$("#ctrl-venue").addClass("error");
		$("#err-venue").text("Please specify the name of the place.");
		$("#err-venue").show();
		$("#input-venue").focus();
		return false;
	} else {
		$("#ctrl-venue").removeClass("error");
		$("#err-venue").hide();
		return true;
	}
}

function check_street() {
	if ($("#input-street").val() == "") {
		$("#ctrl-street").addClass("error");
		$("#err-street").text("Please enter street address.");
		$("#err-street").show();
		$("#input-street").focus();
		return false;
	} else {
		$("#ctrl-street").removeClass("error");
		$("#err-street").hide();
		return true;
	}
}

function check_city() {
	if ($("#input-city").val() == "") {
		$("#ctrl-city").addClass("error");
		$("#err-city").text("Please enter city.");
		$("#err-city").show();
		$("#input-city").focus();
		return false;
	} else {
		$("#ctrl-city").removeClass("error");
		$("#err-city").hide();
		return true;
	}
}

function check_state() {
	if ($("#input-state").val() == "") {
		$("#ctrl-city").addClass("error");
		$("#err-city").text("Please enter state.");
		$("#err-city").show();
		$("#input-state").focus();
		return false;
	} else {
		$("#ctrl-city").removeClass("error");
		$("#err-city").hide();
		return true;
	}
}

function check_zip() {
	if ($("#input-zip").val() == "") {
		$("#ctrl-city").addClass("error");
		$("#err-city").text("Please enter zip code.");
		$("#err-city").show();
		$("#input-zip").focus();
		return false;
	} else {
		$("#ctrl-city").removeClass("error");
		$("#err-city").hide();
		return true;
	}
}

function check_url() {
	if ($("#input-url").val() == "") {
		$("#ctrl-url").addClass("error");
		$("#err-url").text("Please enter a URL address.");
		$("#err-url").show();
		$("#input-url").focus();
		return false;
	} else {
		$("#ctrl-url").removeClass("error");
		$("#err-url").hide();
		return true;
	}
}

function check_costs() {
    if(($("#input-cost-min").val()=="" || $("#input-cost-max").val()=="") && !$("#input-free").is(':checked')) {
        $("#ctrl-cost").addClass("error");
		$("#err-cost").text("Please specify how much the event costs.");
		$("#err-cost").show();
		$("#input-cost-min").focus();
		return false;
	} else if((isNaN($("#input-cost-min").val()) || isNaN($("#input-cost-max").val())) ||
	          ($("#input-cost-min").val() < 0 || $("#input-cost-max").val() < 0)) {
	    $("#ctrl-cost").addClass("error");
		$("#err-cost").text("Negative numbers cannot be used.");
		$("#err-cost").show();
		$("#input-cost-min").focus();
		return false;
    } else if($("#input-cost-min").val() * 1.0 > $("#input-cost-max").val() * 1.0) {
        $("#ctrl-cost").addClass("error");
		$("#err-cost").text("Minimum cost cannot be larger than maximum.");
		$("#err-cost").show();
		$("#input-cost-min").focus();
		return false;
    } else {
        $("#ctrl-cost").removeClass("error");
		$("#err-cost").hide();
		return true;
    }
}

function disableCosts() {
    if($("#input-free").is(':checked')) {
        $("#input-cost-min").val("");
        $("#input-cost-min").prop('disabled', true);
        $("#input-cost-max").val("");
        $("#input-cost-max").prop('disabled', true);
    } else {
        $("#input-cost-min").prop('disabled', false);
        $("#input-cost-max").prop('disabled', false);
    }
}
