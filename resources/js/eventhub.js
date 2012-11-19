$(document).ready(function(){

	// Initialize the "Last Search" area to nothing (just started)
	$("#lastSearch").text("");

	$('.cat').change(function(event){
		eventSearch(false);
	});

	$('.loc').change(function(event){
		eventSearch(false);
	});

	// Function to initiate filtered searches of events (initiate from left sidebar)
	$('#inputText').keypress(function(event) {
		// Determine the button that was pressed in the input text area
		var keycode = (event.keyCode ? event.keyCode : event.which);

		if(keycode == 13) { // Check for the 'Enter' keycode
			eventSearch(true);
		}

	});
    
	$("#login-error").fadeIn("slow"); 
	
    // triggers infinite scroll
    $(window).scroll(function() {
        var wintop = $(window).scrollTop(), docheight = $(document).height(), winheight = $(window).height();
        var scrolltrigger = 0.95;

        if ((wintop/(docheight-winheight)) > scrolltrigger) {
			infinite_scroll();
        }
    });
    
    $("#editProfile_btn").click(function() {
    	editProfile();
    });

});

function editProfile(){
	var firstName = $.trim(document.getElementById("first-name").value);
	var lastName = $.trim(document.getElementById("last-name").value);
	var oldPassword = $.trim(document.getElementById("old-password").value);
	var newPassword1 = $.trim(document.getElementById("new-password-1").value);
	var newPassword2 = $.trim(document.getElementById("new-password-2").value);
	var userEmail = $.trim(document.getElementById("user-email").value);
	var useFbPic = document.getElementById("fbPic").checked;
	var userPic = document.getElementById('uploadPic').files[0]
	//var input_image =  document.getElementById('input-photo').files[0];
	/*if(newPassword1.length<6){
	 alert("password too short");
	 return;
	}
	if(newPassword1!=newPassword2){
		alert("passwords do not match.");
		return;
	}*/
	
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
	
	$.get("eventlist", function(data){
		if (data != "") {
			$("#refresher").append(data);
		} else {
			$('#contentLoader').empty();
		}
		$('#contentLoader').hide();
	});
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
	} 

	// Now prepare the extracted data to send in the POST request to the event controller.
	var fd = new FormData();
	fd.append('categories', category_values);
	fd.append('locations', location_values);
	fd.append('keywords', keyword_values);

	// Now send the POST request.
/*
	// TODO: Make the search_event function (!!!) in events/views.py that
	// can extract the data that is stored as 'categories', 'locations', and 'keywords',
	// use the search functions, and then return the data.
	var request = $.ajax({
		url: "search_event",
		type: "POST",
		data: fd,
		processData: false,
		contentType: false,
		cache: false 
	});
*/
	// TODO: Determine the values that are returned from the event controller function
	//       search_event (for example, see create_event return values)

	// Now just update the values at the top of the main page (next to the Upcoming Events)
	if(useKeyword && keyword_values.length != 0){
		$("#lastSearch").text(category_values.toString() + " / " + location_values.toString() + " / " + keyword_values.toString() );
	} else {
		$("#lastSearch").text(category_values.toString() + " / " + location_values.toString() );		
	}
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
