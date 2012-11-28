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
	
	$('.close').click(function(event){
		delete_event(event.target.value);
	});
    
	$("#login-error").fadeIn("slow"); 
	
    // triggers infinite scroll
    $(window).scroll(function() {
        var wintop = $(window).scrollTop(), docheight = $(document).height(), winheight = $(window).height();
        var scrolltrigger = 0.95;

        if ((wintop/(docheight-winheight)) > scrolltrigger) {
			if (!waitingForScroll && last_index < max_res) {
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
    
    prevSearched = true;
	eventSearch(true);
});

function countChecked(identifier) {
    return $(identifier+":checked").length;
}


function editProfile(){
	var firstName = $.trim(document.getElementById("first-name").value);
	var lastName = $.trim(document.getElementById("last-name").value);
	var oldPassword = document.getElementById("old-password").value;
	var newPassword1 = document.getElementById("new-password-1").value;
	var newPassword2 = document.getElementById("new-password-2").value;
	var userEmail = $.trim(document.getElementById("user-email").value);
	var useFbPic = document.getElementById("fbPic").checked;
	var userPic = document.getElementById('uploadPic').files[0]
	if(newPassword1.length>0){
		if(newPassword1.length<6){
		 alert("Password should be at least 6 characters!");
		 return;
		}
		if(newPassword1!=newPassword2){
			alert("Passwords do not match.");
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
		if (msg == "1") {
			document.location.href = '/mypage';
		} else if(msg == "2"){
			alert("Your username and/or password were incorrect.");
		}else if(msg == "3"){
			alert("Your account is inactive.");
		}else {
			alert("Failing ");
		}
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
	waitingForScroll = false;
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
