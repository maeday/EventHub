// TODO: A lot of refactoring needs to be done.

// Global variables (this is probably bad style)
var prevSearched = false;
var prevSearchKeywords = "";
var pickle_str = "";
var last_index = 0;
var max_res = 0;
var increment = 5;
var waitingForScroll = false;

$(document).ready(function(){

	// Initialize the "Last Search" area to nothing (just started)
	$("#lastSearch").text("");

	$('.cat').change(function(event){
		if ($(this).is(':checked'))
		{
			$('#cat-all').removeAttr("disabled");
			$('#cat-all').attr("checked", false);
		} else {
			if (countChecked('.cat') == 0) {
				$('#cat-all').attr("disabled", true);
				$('#cat-all').attr("checked", true);
			}
		}
		eventSearch(false);
	});

	$('.loc').change(function(event){
		if ($(this).is(':checked'))
		{
			$('#loc-all').removeAttr("disabled");
			$('#loc-all').attr("checked", false);
		} else {
			if (countChecked('.loc') == 0) {
				$('#loc-all').attr("disabled", true);
				$('#loc-all').attr("checked", true);
			}
		}
		eventSearch(false);
	});
	
	$('#cat-all').click(function(){
		if ($(this).is(':checked'))
		{
			$(this).attr("disabled", true);
			$('.cat').attr("checked", false);	
		}
		eventSearch(false);
	});
	
	$('#loc-all').click(function(){
		if ($(this).is(':checked'))
		{
			$(this).attr("disabled", true);
			$('.loc').attr("checked", false);
		}
		eventSearch(false);
	});

	// Function to initiate filtered searches of events (initiate from left sidebar)
	$('#inputText').keypress(function(event) {
		// Determine the button that was pressed in the input text area
		var keycode = (event.keyCode ? event.keyCode : event.which);

		if(keycode == 13) { // Check for the 'Enter' keycode
			prevSearched = true;
			eventSearch(true);
		}

	});
	
	$('.delete-close').click(function() {
		$("#confirm_delete").val($(this).val());
	});
	
	$('#confirm_delete').click(function() {
		delete_event($(this).val());
	});
    
    //$("#login-error").fadeIn("slow"); 
    $("div.alert").each( function(index) {
        $(this).fadeIn("slow");
    });
	
    // triggers infinite scroll
    $(window).scroll(function() {
		if (waitingForScroll) {
			return;
		}
        var wintop = $(window).scrollTop(), docheight = $(document).height(), winheight = $(window).height();
        var scrolltrigger = 0.95;

        if ((wintop/(docheight-winheight)) > scrolltrigger) {
			if (last_index < max_res) {
				waitingForScroll = true;
				infinite_scroll();
			}
			
        }
    });
    
    $("#editProfile_btn").click(function() {
    	editProfile();
    });
    
    $("#search-btn").click(function() {
	    eventSearch(true); 
    });
    
    $('.edit-event-btn').click(function() {
    	$("#confirm_edits").val($(this).val());
    	populate_fields($(this).val());
    });
    
    $("#confirm_edits").click(function(event) {
    	if (!edit_check_all()) {
    		return false;
    	}
    	$(this).addClass("disabled");
    	$(this).attr("disabled", true);
    	$("#editEventLoader").show();
    	editEvent($("#confirm_edits").val());
    });
    
    $("#edit-remove-image").change(function() {
    	edit_disableImage();
    });
    
// BEGINNING OF CREATE.JS DOCUMENT READY
//
//

	$(".edit-datepicker").datepicker({ minDate:new Date() });
		
	$("#edit-picker-1").click(function() {
    	$("#edit-input-startdate").focus();
    });
    $("#edit-picker-2").click(function() {
    	$("#edit-input-enddate").focus();
    });
    
    $("#edit-clockswitch-1").click(function() {
    	edit_switch_clock($(this));
    });
    $("#edit-clockswitch-2").click(function() {
    	edit_switch_clock($(this));
    });
    
    $("#edit-input-title").keyup(function() {
    	if ($(this).val() != "") {
			$("#edit-ctrl-title").removeClass("error");
			$("#edit-err-title").hide();
			return true;
		}
    });
    
    $("#edit-input-description").keyup(function() {
    	if ($(this).val() != "") {
			$("#edit-ctrl-description").removeClass("error");
			$("#edit-err-description").hide();
			return true;
		}
    });
    
    $("#edit-input-location").change(function() {
    	if ($(this).val() != -1) {
			$("#edit-ctrl-location").removeClass("error");
			$("#edit-err-location").hide();
			return true;
		}
    }); 
    
    $("#edit-input-venue").keyup(function() {
    	if ($(this).val() != "") {
			$("#edit-ctrl-venue").removeClass("error");
			$("#edit-err-venue").hide();
			return true;
		}
    });
    
    $("#edit-input-street").keyup(function() {
    	if ($(this).val() != "") {
			$("#edit-ctrl-street").removeClass("error");
			$("#edit-err-street").hide();
			return true;
		}
    });
    
    $('.edit-c-cat').change(function(event){
		if ($(this).is(':checked')) {
			$("#edit-ctrl-categories").removeClass("error");
			$("#edit-err-categories").hide();
		}
	});
    
    $("#edit-input-startdate").blur(function() {
	    edit_check_date($(this), $("#edit-err-start"), $("#edit-ctrl-start"));
    });
    $("#edit-input-starttime").blur(function() {
	    edit_check_time($(this), $("#edit-err-start"), $("#edit-ctrl-start"));
    });
    $("#edit-input-enddate").blur(function() {
	    edit_check_date($(this), $("#edit-err-end"), $("#edit-ctrl-end"));
    });
    $("#edit-input-endtime").blur(function() {
	    edit_check_time($(this), $("#edit-err-end"), $("#edit-ctrl-end"));
    });
    
    $("#edit-input-startdate").change(function() {
	    $("#edit-input-enddate").val($("#edit-input-startdate").val());
    });
    
    $("#edit-input-free").change(function() {
        edit_disableCosts();
    });
    
    $("#follow").click(function() {
      if ($(this).hasClass('btn-primary')) {
        followEvent($("#event-id").html());
        $(this).removeClass('btn-primary');
        $(this).addClass('btn-inverse');
        $(this).html('Unfollow');
      } else {
        unfollowEvent($("#event-id").html());
        $(this).removeClass('btn-inverse');
        $(this).addClass('btn-primary');
        $(this).html('Follow');
      }
    });
    
    prevSearched = true;
});

function countChecked(identifier) {
    return $(identifier+":checked").length;
}


function editProfile() {
	var firstName = $.trim(document.getElementById("first-name").value);
	var lastName = $.trim(document.getElementById("last-name").value);
	var oldPassword = document.getElementById("old-password").value;
	var newPassword1 = document.getElementById("new-password-1").value;
	var newPassword2 = document.getElementById("new-password-2").value;
	var userEmail = $.trim(document.getElementById("user-email").innerHTML);
	var useFbPic = document.getElementById("fbPic").checked;
	var userPic = document.getElementById("uploadPic").files[0];
	
	// Show loader and disable "Save" button
	$("#editProfLoader").show();
	$("#editProfile_btn").addClass("disabled");
	$("#editProfile_btn").attr("disabled", true);
	
	$("#ctrl-old-password").removeClass("error");
	$("#err-old-password").hide();
	$("#ctrl-new-password-1").removeClass("error");
	$("#err-new-password-1").hide();
	$("#ctrl-new-password-2").removeClass("error");
	$("#err-new-password-2").hide();
	
	if(newPassword1.length>0){
//		if(newPassword1.length<6){
//		 //alert("Password should be at least 6 characters!");
//		 $("#ctrl-new-password-1").addClass("error");
//		 $("#err-new-password-1").text("Password should be at least 6 characters!");
//		 $("#err-new-password-1").show();
//		 $("#new-password-1").focus();
//		 return;
//		}
		if(newPassword1!=newPassword2){
			//alert("Passwords do not match.");
			$("#ctrl-new-password-2").addClass("error");
			$("#err-new-password-2").text("Passwords do not match.");
			$("#err-new-password-2").show();
			$("#new-password-2").focus();
			return;
		}
	}
	var fd = new FormData();
	fd.append( 'firstName', firstName );
	fd.append( 'lastName', lastName );
	fd.append( 'oldPassword', oldPassword );
	fd.append( 'newPassword', newPassword1 );
	fd.append( 'userEmail', userEmail );
	fd.append( 'useFbPic', useFbPic );
	fd.append( 'userPic', userPic );
	var request = $.ajax({
		url: "edit_profile",
		type: "POST",
		data: fd,
		processData: false,
    contentType: false,
    cache: false 
	});
	
	request.done(function(msg) {
		if (msg == "1" || msg == "3") {
			document.location.href = '/mypage';
		} else if(msg == "2"){
			//alert("Your current password is incorrect.");
			
			$("#ctrl-old-password").addClass("error");
			$("#err-old-password").text("Your current password is incorrect.");
			$("#err-old-password").show();
			$("#old-password").focus();
		} else {
			alert("Error: User Profile editing failed.");
		}
		
		// Reset state
		$("#editProfLoader").hide();
		$("#editProfile_btn").removeClass("disabled");
		$("#editProfile_btn").removeAttr("disabled");
	});
	
	request.fail(function(jqXHR, textStatus) {
		alert("Ajax request failed: " + textStatus);
	});
}

function infinite_scroll() {
	$('#contentLoader').show();
	if (pickle_str != "") {
		// Get next [increment] events from filter result
		var next_index = last_index+increment;
		if (next_index > max_res) {
			next_index = max_res;
		}
		$.post("getevents", {pickle_str: pickle_str, last_index: last_index, next_index: next_index}, function(data){
			if (data != "" && data.length > 40) {
				last_index += increment;
				$("#refresher").append(data);
			} else {
				$('#contentLoader').empty();
			}
			$('#contentLoader').hide();
			
			// This needs to go here since post request is asynchronous
			waitingForScroll = false;
		});
	} else {
		// Default behavior (load everything). Should never reach here.
		$.get("eventlist", function(data){
			if (data != "") {
				$("#refresher").append(data);
			} else {
				$('#contentLoader').empty();
			}
			$('#contentLoader').hide();
		});
	}
}

function followEvent(eventId) {
  $.get("/follow/"+eventId);
}

function unfollowEvent(eventId) {
  $.get("/unfollow/"+eventId);
}

// Function that will extract the locations, the categories, and the keywords that will
// be used to filter the events displayed on the front page.
function eventSearch(useKeyword) {
	// Create arrays for the locations, the neighborhoods, and the keywords (as we will
	// be passing them to the functions directly).
	var category_values = $('.cat:checked').map(function() {
		return $(this).val();
	}).get();

	var location_values = $('.loc:checked').map(function() {
		return $(this).val();
	}).get();

	var keyword_values = new Array();

	// Last checks with the keyword values (make sure empty string is not given)
	if(useKeyword){
		keyword_values = $('#inputText').val().split(" ");
		keyword_values = keyword_values.filter(String);
		prevSearchKeywords = keyword_values;
	} else if (prevSearched) {
		keyword_values = prevSearchKeywords;
	}

	// Now prepare the extracted data to send in the POST request to the event controller.
	var fd = new FormData();
	var keyword_string = keyword_values.join();
	var locations_string = location_values.join();
	var categories_string = category_values.join();
	fd.append('categories', categories_string);
	fd.append('locations', locations_string);
	fd.append('keywords', keyword_string);

	// Now send the POST request.

	// TODO: Make the search_event function (!!!) in events/views.py that
	// can extract the data that is stored as 'categories', 'locations', and 'keywords',
	// use the search functions, and then return the data.
	var request = $.ajax({
		//url: "filterlist",
		url: "testfilter",
		type: "POST",
		data: fd,
		processData: false,
		contentType: false,
		cache: false
	});

	// TODO: Determine the values that are returned from the event controller function
	//       search_event (for example, see create_event return values)
	
	request.success(function(msg) {
		if (msg) {
			$("#refresher").hide();
			
			// Reply should be "[# results],[cache key]"
			var parts = msg.split(',', 2);
			
			max_res = parts[0];
			pickle_str = parts[1];
			
			last_index = 0;
			
			// Now just update the values at the top of the main page (next to the Upcoming Events)
			if((useKeyword || prevSearched) && keyword_values.length != 0){
				$("#search-title").html(max_res + " events found &nbsp;<small>\"" + keyword_values.toString() + "\"</small>");
			} else {
				$("#search-title").html("Upcoming Events");		
			}
			
			// Get first [increment] events from filter result
			var next_index = last_index+increment;
			if (next_index > max_res) {
				next_index = max_res;
			}
			$.post("getevents", {pickle_str: pickle_str, last_index: last_index, next_index: next_index}, function(data){
				if (data != "") {
//					$("#refresher").append(data);
					$("#refresher").html(data);
					last_index += increment;
				} else {
//					$('#contentLoader').empty();
				}
//				$('#contentLoader').hide();
			});
			
			//$("#refresher").html(msg);
			$("#refresher").fadeIn(2000);
			//filterEventList();
		} else {
			alert("Could not filter");
		}
	});
	
	request.fail(function(jqXHR, textStatus) {
		alert("Ajax request failed: " + textStatus);
		filterEventList();
	});

	// Scroll to top of page
	window.scrollTo(0,0);
}

function refreshEventList() {
	$.get("eventlist", function(data) {
		$("#refresher").hide();
		$("#refresher").html(data);
		$("#refresher").fadeIn(2000);
	});
}

function disablefield() { 
    if (document.getElementById('fbPic').checked == 1){ 
        document.getElementById('uploadPic').disabled='disabled'; 
        document.getElementById('uploadPic').value='disabled';
    } else { 
        document.getElementById('uploadPic').disabled=''; 
        document.getElementById('uploadPic').value='Allowed'; 
    } 
}

function delete_event(id) {
	var fd = new FormData();
	fd.append( 'id', id );

	var request = $.ajax({
		url: "delete_event",
		type: "POST",
		data: fd,
		processData: false,
		contentType: false,
		cache: false
	});

	request.done(function(msg) {
		if (msg == "1") {
			location.reload();
		} else {
			alert("Could not delete event");
		}
	});
	
	request.fail(function(jqXHR, textStatus) {
		alert("Ajax request failed: " + textStatus);
	});
}

function editEvent(id) {
	var input_id = id;
	var input_title = $("#edit-input-title").val();
	var input_desc = $("#edit-input-description").val();
	var input_poster = $("#edit-user-id").val();
	var input_startdate = $("#edit-input-startdate").val();
	var input_starttime = $("#edit-input-starttime").val();
	var input_enddate = $("#edit-input-enddate").val();
	var input_endtime = $("#edit-input-endtime").val();
	var input_venue = $("#edit-input-venue").val();
	var input_street = $("#edit-input-street").val();
	var input_city = $("#edit-input-city").val();
	var input_state = $("#edit-input-state").val().toUpperCase();
	var input_zip = $("#edit-input-zip").val();
	var input_url = $("#edit-input-url").val();
	var input_image =  document.getElementById('edit-input-photo').files[0];
	var input_cost_min = $("#edit-input-cost-min").val();
	var input_cost_max = $("#edit-input-cost-max").val();
	var input_free_checked = $("#edit-input-free").is(':checked');
	var input_remove_checked = $("#edit-remove-image").is(':checked');
	var input_location = $("#edit-input-location").val();
	var input_categories = $(".edit-c-cat:checked").map(function() {
		return $(this).val();
	}).get();
	var input_categories_string = input_categories.join();
	
	var start_clock = "am";
	if ($("#edit-clockswitch-1").html() == "&nbsp;PM&nbsp;") { // if start clock is PM
		start_clock = "pm";
	}
	
	var end_clock = "am";
	if ($("#edit-clockswitch-2").html() == "&nbsp;PM&nbsp;") { // if end clock is PM
		end_clock = "pm";
	}
	
	// Stringifies time variables. ex) "11/04/2012 04:15 pm"
	var start_str = input_startdate + " " + input_starttime + " " + start_clock;
	var end_str = input_enddate + " " + input_endtime + " " + end_clock;
	
	var input_free_value;
	// Pass in 0, 1 values to controller for 'free'
	// If free, pass in non-blank dummy values for min and max cost
	if(input_free_checked) {
	    input_free_value = 1;
	    input_cost_min = "0";
	    input_cost_max = "0";
	} else {
	    input_free_value = 0;
	}
	
	var input_remove_value;
	// Pass in 0, 1 values to controller for remove image
	// If free, pass in blank dummy value for image url
	if(input_remove_checked) {
	    input_remove_value = 1;
	} else {
	    input_remove_value = 0;
	}
		
	var fd = new FormData();
	fd.append( 'id', input_id );
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
	fd.append( 'remove', input_remove_value );
	fd.append( 'location', input_location );
	fd.append( 'categories', input_categories_string );
	
	var request = $.ajax({
		url: "edit_event",
		type: "POST",
		data: fd,
		processData: false,
	    contentType: false,
	    cache: false
	});
	
	request.done(function(msg) {
		if (msg == "1") {
			$("#editEvent").modal('hide');
			location.reload();
		} else {
			alert("Could not edit event");
		}
		
		// Reset state
		$("#editEventLoader").hide();
		$("#confirm_edits").removeClass("disabled");
    	$("#confirm_edits").removeAttr("disabled");
	});
	
	request.fail(function(jqXHR, textStatus) {
		alert("Ajax request failed: " + textStatus);
	});
}

function jDecode(str) {
    return $("<div/>").html(str).text();
}

function parse_and_populate(json) {
	/*
	var input_image =  document.getElementById('edit-input-photo').files[0];
	*/
	$("#edit-input-title").val(json.name);
	
	var startDateTime = json.start.split(" ");
	var endDateTime = json.end.split(" ");

	$("#edit-input-startdate").val(startDateTime[0]);
	$("#edit-input-starttime").val(startDateTime[1]);
	$("#edit-clockswitch-1").html("&nbsp;" + startDateTime[2] + "&nbsp;");
	$("#edit-input-enddate").val(endDateTime[0]);
	$("#edit-input-endtime").val(endDateTime[1]);
	$("#edit-clockswitch-2").html("&nbsp;" + endDateTime[2] + "&nbsp;");
	
	$("#edit-input-description").val(json.desc);
	$("#edit-input-location").val(json.neighborhood);
	$("#edit-input-venue").val(json.venue);
	$("#edit-input-street").val(json.address);
	$("#edit-input-city").val(json.city);
	$("#edit-input-zip").val(json.zipcode);
	
	if (json.free == "1") {
		$('#edit-input-free').prop('checked', true);
		$("#edit-input-cost-max").prop('disabled', true);
		$("#edit-input-cost-min").prop('disabled', true);
		$("#edit-input-cost-max").val("");
		$("#edit-input-cost-min").val("");
	} else {
		$('#edit-input-free').prop('checked', false);
		$("#edit-input-cost-max").prop('disabled', false);
		$("#edit-input-cost-min").prop('disabled', false);
		$("#edit-input-cost-max").val(json.max);
		$("#edit-input-cost-min").val(json.min);
	}
	
	$("#edit-input-url").val(json.url);
	
	$(".edit-c-cat").prop('checked', false);
	for (i = 0; i < json.categories.length; i++) {
		cid = "#checkbox-" + json.categories[i];
		$(cid).prop('checked', true);
	}
	
	$("#edit-remove-image").prop('checked', false);
	$("#edit-input-photo").prop('disabled', false);
}

function populate_fields(event_id) {
		
	var request = $.ajax({
		url: "get_event_info",
		type: "POST",
		data: {id:event_id},
		dataType: "json",
	    cache: false
	});
	
	request.success(function(msg) {
		parse_and_populate(msg);
	});
	
	request.fail(function(jqXHR, textStatus) {
		alert("Ajax request failed: " + textStatus);
	});
}

// BEGINNING OF CREATE.JS FUNCTIONS
//
//

// Checks for errors in the form.
function edit_check_all() {
	return edit_check_title() && edit_check_times_comprehensive() && edit_check_summary() && edit_check_location() && edit_check_venue() && edit_check_street() && edit_check_city() && edit_check_state() && edit_check_costs() && edit_check_categories();
}

function edit_check_title() {
	if ($("#edit-input-title").val() == "") {
		$("#edit-ctrl-title").addClass("error");
		$("#edit-err-title").text("You forgot the title!");
		$("#edit-err-title").show();
		$("#edit-input-title").focus();
		return false;
	} else {
		$("#edit-ctrl-title").removeClass("error");
		$("#edit-err-title").hide();
		return true;
	}
}

function edit_check_times_comprehensive() {
	return edit_check_date($("#edit-input-startdate"), $("#edit-err-start"), $("#edit-ctrl-start")) && edit_check_time($("#edit-input-starttime"), $("#edit-err-start"), $("#edit-ctrl-start")) && edit_check_date($("#edit-input-enddate"), $("#edit-err-end"), $("#edit-ctrl-end")) 
		&& edit_check_time($("#edit-input-endtime"), $("#edit-err-end"), $("#edit-ctrl-end")) && edit_check_time_logic();
}

function edit_check_summary() {
	if ($("#edit-input-description").val() == "") {
		$("#edit-ctrl-description").addClass("error");
		$("#edit-err-description").text("Please summarize the event.");
		$("#edit-err-description").show();
		$("#edit-input-description").focus();
		return false;
	} else {
		$("#edit-ctrl-description").removeClass("error");
		$("#edit-err-description").hide();
		return true;
	}
}

function edit_check_date(input, err, ctrl) {
	var str = input.val();
	var errorMsg = edit_validate_date(str);
	
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

function edit_check_time(input, err, ctrl) {
	edit_normalize_time(input);
	
	var str = input.val();
	var errorMsg = edit_validate_time(str);
	
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

function edit_normalize_time(input, str) {
	var str = input.val();
	
	re = /^(\d{1,2})$/;
	
	if (str != '') {
		if (regs = str.match(re)) {
			input.val(str + ":00");
		}
	}
}

// Validates date format with Regex. Returns error message or empty string if no error.
function edit_validate_date(str) {
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
function edit_validate_time(str) {
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

function edit_check_time_logic() {
	// get start date
	re = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/;
	var str = $("#edit-input-startdate").val();
	regs = str.match(re);
	var start_month = parseInt(regs[1], 10);
	var start_day = parseInt(regs[2], 10);
	var start_year = regs[3];
	
	// get end date
	str = $("#edit-input-enddate").val();
	regs = str.match(re);
	var end_month = parseInt(regs[1], 10);
	var end_day = parseInt(regs[2], 10);
	var end_year = regs[3];
	
	// get start time
	re = re = /^(\d{1,2}):(\d{2})(:00)?$/;
	str = $("#edit-input-starttime").val();
	regs = str.match(re);
	var start_hour = parseInt(regs[1], 10);
	var start_minute = parseInt(regs[2], 10);
	if ($("#edit-clockswitch-1").html() == "&nbsp;PM&nbsp;" && start_hour != 12)
		start_hour += 12;
	if ($("#edit-clockswitch-1").html() == "&nbsp;AM&nbsp;" && start_hour == 12)
		start_hour -= 12;
	
	// get end time
	str = $("#edit-input-endtime").val();
	regs = str.match(re);
	var end_hour = parseInt(regs[1], 10);
	var end_minute = parseInt(regs[2], 10);
	if ($("#edit-clockswitch-2").html() == "&nbsp;PM&nbsp;" && end_hour != 12)
		end_hour += 12;
	if ($("#edit-clockswitch-2").html() == "&nbsp;AM&nbsp;" && end_hour == 12)
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
		$("#edit-err-start").text(errorMsg);
		$("#edit-err-start").show();
		$("#edit-ctrl-start").addClass("error");
		//$("#edit-input-startdate").focus();
		return false;
	} else if (end_date < start_date) {
		errorMsg = "Cannot finish before start";
		$("#edit-err-end").text(errorMsg);
		$("#edit-err-end").show();
		$("#edit-ctrl-end").addClass("error");
		$("#edit-input-endtime").focus();
		return false;
	} else {
		$("#edit-err-start").hide();
		$("#edit-ctrl-start").removeClass("error");
		$("#edit-err-end").hide();
		$("#edit-ctrl-end").removeClass("error");
		return true;
	}
}

function edit_switch_clock(btn) {
	if (btn.html() == "&nbsp;AM&nbsp;") {
		btn.html("&nbsp;PM&nbsp;");
	} else {
		btn.html("&nbsp;AM&nbsp;");
	}
}

function edit_check_venue() {
	if ($("#edit-input-venue").val() == "") {
		$("#edit-ctrl-venue").addClass("error");
		$("#edit-err-venue").text("Please specify the name of the place.");
		$("#edit-err-venue").show();
		$("#edit-input-venue").focus();
		return false;
	} else {
		$("#edit-ctrl-venue").removeClass("error");
		$("#edit-err-venue").hide();
		return true;
	}
}

function edit_check_street() {
	if ($("#edit-input-street").val() == "") {
		$("#edit-ctrl-street").addClass("error");
		$("#edit-err-street").text("Please enter street address.");
		$("#edit-err-street").show();
		$("#edit-input-street").focus();
		return false;
	} else {
		$("#edit-ctrl-street").removeClass("error");
		$("#edit-err-street").hide();
		return true;
	}
}

function edit_check_city() {
	if ($("#edit-input-city").val() == "") {
		$("#edit-ctrl-city").addClass("error");
		$("#edit-err-city").text("Please enter city.");
		$("#edit-err-city").show();
		$("#edit-input-city").focus();
		return false;
	} else {
		$("#edit-ctrl-city").removeClass("error");
		$("#edit-err-city").hide();
		return true;
	}
}

function edit_check_state() {
	if ($("#edit-input-state").val() == "") {
		$("#edit-ctrl-city").addClass("error");
		$("#edit-err-city").text("Please enter state.");
		$("#edit-err-city").show();
		$("#edit-input-state").focus();
		return false;
	} else {
		$("#edit-ctrl-city").removeClass("error");
		$("#edit-err-city").hide();
		return true;
	}
}

function edit_check_zip() {
	if ($("#edit-input-zip").val() == "") {
		$("#edit-ctrl-city").addClass("error");
		$("#edit-err-city").text("Please enter zip code.");
		$("#edit-err-city").show();
		$("#edit-input-zip").focus();
		return false;
	} else {
		$("#edit-ctrl-city").removeClass("error");
		$("#edit-err-city").hide();
		return true;
	}
}

function edit_check_url() {
	if ($("#edit-input-url").val() == "") {
		$("#edit-ctrl-url").addClass("error");
		$("#edit-err-url").text("Please enter a URL address.");
		$("#edit-err-url").show();
		$("#edit-input-url").focus();
		return false;
	} else {
		$("#edit-ctrl-url").removeClass("error");
		$("#edit-err-url").hide();
		return true;
	}
}

function edit_check_costs() {
    if(($("#edit-input-cost-min").val()=="" || $("#edit-input-cost-max").val()=="") && !$("#edit-input-free").is(':checked')) {
        $("#edit-ctrl-cost").addClass("error");
		$("#edit-err-cost").text("Please specify cost or check 'Free'.");
		$("#edit-err-cost").show();
		$("#edit-input-cost-min").focus();
		return false;
	} else if((isNaN($("#edit-input-cost-min").val()) || isNaN($("#edit-input-cost-max").val())) ||
	          ($("#edit-input-cost-min").val() < 0 || $("#edit-input-cost-max").val() < 0)) {
	    $("#edit-ctrl-cost").addClass("error");
		$("#edit-err-cost").text("Please provide positive numbers for min and max cost.");
		$("#edit-err-cost").show();
		$("#edit-input-cost-min").focus();
		return false;
    } else if($("#edit-input-cost-min").val() * 1.0 > $("#edit-input-cost-max").val() * 1.0) {
        $("#edit-ctrl-cost").addClass("error");
		$("#edit-err-cost").text("Min cost should be less than or equal to max cost.");
		$("#edit-err-cost").show();
		$("#edit-input-cost-min").focus();
		return false;
    } else {
        $("#edit-ctrl-cost").removeClass("error");
		$("#edit-err-cost").hide();
		return true;
    }
}

function edit_disableCosts() {
    if($("#edit-input-free").is(':checked')) {
        $("#edit-input-cost-min").val("");
        $("#edit-input-cost-min").prop('disabled', true);
        $("#edit-input-cost-max").val("");
        $("#edit-input-cost-max").prop('disabled', true);
    } else {
        $("#edit-input-cost-min").prop('disabled', false);
        $("#edit-input-cost-max").prop('disabled', false);
    }
}

function edit_disableImage() {
    if($("#edit-remove-image").is(':checked')) {
    	$("#edit-input-photo").val("");
        $("#edit-input-photo").prop('disabled', true);
    } else {
        $("#edit-input-photo").prop('disabled', false);
    }
}

function edit_check_location() {
	if ($("#edit-input-location").val() == -1) {
		$("#edit-ctrl-location").addClass("error");
		$("#edit-err-location").text("Please select a neighborhood.");
		$("#edit-err-location").show();
		$("#edit-input-location").focus();
	    return false;
	} else {
		$("#edit-ctrl-location").removeClass("error");
		$("#edit-err-location").hide();
		return true;
	}
}

function edit_check_categories() {
	if ($(".edit-c-cat:checked").map(function() { return $(this).val(); }).get() == "") {
		$("#edit-ctrl-categories").addClass("error");
		$("#edit-err-categories").text("Please select at least one category.");
		$("#edit-err-categories").show();
		return false;
	} else {
		$("#edit-ctrl-categories").removeClass("error");
		$("#edit-err-categories").hide();
		return true;
	}
}