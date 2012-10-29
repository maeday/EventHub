$(document).ready(function(){

	$(".datepicker").datepicker({ minDate:new Date() });
		
	$("#picker-1").click(function() {
    	$("#input02").focus();
    });
    $("#picker-2").click(function() {
    	$("#input03").focus();
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
    
    $("#input04").keyup(function() {
    	if ($(this).val() != "") {
			$(".control-group:eq(3)").removeClass("error");
			$(".help-block:eq(0)").text("");
			return true;
		}
    });
    
    $("#input05").keyup(function() {
    	if ($(this).val() != "") {
			$(".control-group:eq(4)").removeClass("error");
			$(".help-block:eq(1)").text("");
			return true;
		}
    });
    
    $("#publish").click(function() {
    	if (!check_all()) {
    		return false;
    	}
    	requestCreate();
    });
    
	$("#login-error").fadeIn("slow"); 
    	
});

function requestCreate() {
	var input_title = $("#input-title").val();
	var input_desc = $("#input-description").val();
	
	var request = $.ajax({
		url: "create_event",
		type: "POST",
		data: {
			title : input_title,
			description: input_desc
		}
	});
	
	request.done(function(msg) {
		if (msg == "1") {
			$("#myModal").modal('hide');
			refreshEventList();
		} else {
			alert("Could not create event");
		}
	});
	
	request.fail(function(jqXHR, textStatus) {
		alert("Ajax request failed: " + textStatus);
	});
	
	// post call testing (ignore)
	/*
	var request = $.post("create_event", { title : input_title, description : input_desc }, function(data) {
		// do something
	})
	.success(function(data) {
		if (data == "1") {
			$("#myModal").modal('hide');
			refreshEventList();
		} else {
			alert("Could not create event");
		}
	})
	.error(function() {
		alert("Post request failed");
	})
	.complete(function() {
		// do something
	});
	*/
}

function refreshEventList() {
	$.get("eventlist", function(data) {
		$("#refresher").hide();
		$("#refresher").html(data);
		$("#refresher").fadeIn(2000);
	});
}

function pop_create_event() {
	$("#input-title").focus();
}
function pop_edit_event() {
	$("#input-title").focus();
}

// Checks for errors in the form.
function check_all() {
	return check_title() && check_times_comprehensive() && check_summary() && check_location();
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

function check_location() {
	// TO DO
	return true;
}