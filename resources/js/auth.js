$(document).ready(function(){
    
	// Not sure what this really does
    /*$("#input03").blur(function() {
    	check_password_2($(this), $("#err-repassword"), $("#ctrl-repassword"));
    })*/;
    
    $("#register").click(function() {
    	if (!check_password()) {
    		return false;
    	}
    });
    
	$("#login-error").fadeIn("slow");
	$("#register-error").fadeIn("slow");
});

/*
function check_password_2(input, err, ctrl) {
	var str = input.val();
	var errorMsg = validate_password(str);
	
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

function validate_password(str) {
	var pwd1 = $("#input02").val();
	var errorMsg = "";
	
	if (pwd1 != pwd2) {
		errorMsg = "Passwords do not match!";
	}
	
	return errorMsg;
}
*/

function check_password() {
	var pwd1 = $("#input02").val();
	var pwd2 = $("#input03").val();
	if (pwd1 != pwd2) {
		$("#ctrl-password2").addClass("error");
		$("#err-password2").text("Passwords do not match!");
		$("#err-password2").show();
		$("#input03").focus();
		return false;
	}
	return true;
}