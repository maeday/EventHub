$(document).ready(function(){

	$(".datepicker").datepicker({ minDate: new Date() });
	
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
    
});

function pop_create_event() {
	$("#input01").focus();
}
function pop_edit_event() {
	$("#input01").focus();
}

function switch_clock(btn) {
	if (btn.html() == "&nbsp;AM&nbsp;") {
		btn.html("&nbsp;PM&nbsp;");
	} else {
		btn.html("&nbsp;AM&nbsp;");
	}
}