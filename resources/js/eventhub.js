$(document).ready(function(){

	// Initialize the "Last Search" area to nothing (just started)
	$("#lastSearch").text("");

	// Function to initiate filtered searches of events (initiate from left sidebar)
	$('#inputText').keypress(function(event) {
		// Determine the button that was pressed in the input text area
		var keycode = (event.keyCode ? event.keyCode : event.which);

		if(keycode == 13) { // Check for the 'Enter' keycode
			eventSearch();
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

});

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
function eventSearch() {
	// Create arrays for the locations, the neighborhoods, and the keywords (as we will
	// be passing them to the functions directly).
	var category_values = $('.cat:checked').map(function() {
		return $(this).val();
	}).get();

	var location_values = $('.loc:checked').map(function() {
		return $(this).val();
	}).get();

	var keyword_values = $('#inputText').val().split(" ");

	// Last checks with the keyword values (make sure empty string is not given)
	keyword_values = keyword_values.filter(String);

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
	$("#lastSearch").text(category_values.toString() + " / " + location_values.toString() + " / " + keyword_values.toString() );
}

function refreshEventList() {
	$.get("eventlist", function(data) {
		$("#refresher").hide();
		$("#refresher").html(data);
		$("#refresher").fadeIn(2000);
	});
}
