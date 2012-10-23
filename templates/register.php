<?php
//session_start();

define('FACEBOOK_APP_ID', '419055718161688');
define('FACEBOOK_SECRET', 'b8269e74fc5d9968a19b43b4bafa8635');

function parse_signed_request($signed_request, $secret) {
  list($encoded_sig, $payload) = explode('.', $signed_request, 2); 

  // decode the data
  $sig = base64_url_decode($encoded_sig);
  $data = json_decode(base64_url_decode($payload), true);

  if (strtoupper($data['algorithm']) !== 'HMAC-SHA256') {
    error_log('Unknown algorithm. Expected HMAC-SHA256');
    return null;
  }

  // check sig
  $expected_sig = hash_hmac('sha256', $payload, $secret, $raw = true);
  if ($sig !== $expected_sig) {
    error_log('Bad Signed JSON signature!');
    return null;
  }

  return $data;
}

function base64_url_decode($input) {
    return base64_decode(strtr($input, '-_', '+/'));
}

if (isset($_POST['formsubmitted'])) {
  // DON'T DO ANYTHING
  echo "nothing happens";
  return false;
  
  // Function to sanitize values received from the form. Prevents SQL injection.
  function clean($str) {
    $str = @trim($str);
    if(get_magic_quotes_gpc()) {
      $str = stripslashes($str);
    }
    return mysql_real_escape_string($str);
  }

  $firstname = clean($_POST['firstname']);
  $lastname = clean($_POST['lastname']);
  $nickname = $_POST['nickname'];
  if (!empty($nickname)) { $nickname = clean($nickname); }
  $password = clean($_POST['password']);
  $gender = $_POST['gender'];
  $birthday = date_format(DateTime::createFromFormat('n/j/Y', $_POST['birthday']), 'Y-m-d');
  $email = clean($_POST['email']);
  $phone = clean($_POST['phone']);
  $location = clean($_POST['location']);
  $fbid = $_POST['fbid'];
  
} else if ($_REQUEST['signed_request']) {
  $response = parse_signed_request($_REQUEST['signed_request'], 
                                   FACEBOOK_SECRET);
  
  // registration variables
  $firstname = $response['registration']['first_name'];
  $lastname = $response['registration']['last_name'];
  if ($response['registration']['name']) {
    $fullname = explode(" ", $response['registration']['name']);
    $firstname = $fullname[0];
    $lastname = $fullname[(count($fullname) - 1)];
  }
  $gender = 0;
  if ($response['registration']['gender'] == 'female') {
    $gender = 1;
  }
  $birthday = $response['registration']['birthday'];
  $email = $response['registration']['email'];
  $phone = $response['registration']['phone'];
  $hometown = $response['registration']['location']['name'];
  $fbid = -1;
  if ($response['user_id']) {
    $fbid = $response['user_id'];
  }
  
  include 'header.php';
  ?>

<style type="text/css">
  body {
    background: url(img/bg.jpg) repeat 0 0 #efefef;
  }
</style>

<div class="row-fluid">
  <div class="span12">
    <div class="registration-title">
      <h2>You're almost there!</h2>
    </div>
  </div>
</div>

<div class="register coat">
  <form class="form-horizontal" method="post">
  <div class="row-fluid">
      <div class="register-upper-pad">
          
          <div class="control-group">
            <label class="control-label" for="input01">Email Address</label>
            <div class="controls">
              <input type="text" class="input-large" id="input01" value="<?php echo $email; ?>" name="email">
              <p class="help-block">This is the email address you will use to log in.</p>
            </div>
          </div>
          
          <div class="control-group">
            <label class="control-label" for="input02">Create Password</label>
            <div class="controls">
              <input type="password" class="input-medium" id="input02" name="password">
            </div>
          </div>
          
          <div class="control-group">
            <label class="control-label" for="input03">Confirm Password</label>
            <div class="controls">
              <input type="password" class="input-medium" id="input03" name="repassword">
            </div>
          </div>
          
          <br>
          
          <div class="control-group">
			<label class="control-label" for="input04">First Name</label>
			<div class="controls controls-row">
				<input type="text" class="input-small" id="input04" value="<?php echo $firstname; ?>" name="firstname"> &nbsp;&nbsp; Preferred Name &nbsp;&nbsp; <input type="text" class="input-small" id="input05"  placeholder="Optional" name="nickname">
			</div>
          </div>
          
          <div class="control-group">
            <label class="control-label" for="input06">Last Name</label>
            <div class="controls">
              <input type="text" class="input-small" id="input06" value="<?php echo $lastname; ?>" name="lastname">
            </div>
          </div>
          
          <input type="hidden" name="gender" value="<?php echo $gender; ?>">
          <input type="hidden" name="birthday" value="<?php echo $birthday; ?>">
          <input type="hidden" name="phone" value="<?php echo $phone; ?>">
          <input type="hidden" name="location" value="<?php echo $location; ?>">
          <input type="hidden" name="fbid" value="<?php echo $fbid; ?>">
          
    </div>
  </div>
  
  <div class="form-actions">
    <div class="row">
      <div class="span3 offset1">
        <button type="submit" class="btn btn-large btn-success" name="formsubmitted">Create Account</button>
      </div>
    </div>
  </div>
  
  </form>
  
</div>

<div class="row-fluid">
	<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
	<hr class="footer-diag">
	<h3 style="text-align:center;color:blue;">DEV USE: front-end return array</h3>
	<pre><?php print_r($response); ?></pre>
</div>


<br>

<?php
} else {
  include 'header.php';
?>

<style type="text/css">
  body {
    background: url(img/bg.jpg) repeat 0 0 #efefef;
  }
</style>

<div id="fb-root"></div>
<script src="https://connect.facebook.net/en_US/all.js#appId=419055718161688&xfbml=1"></script>

<div class="row-fluid">
  <div class="span12">
    <div class="registration-title">
      <h2>Create an account</h2>
    </div>
  </div>
</div>

<div class="row-fluid align-center">
  <div class="span12">
    <fb:registration
        redirect-uri="http://chungskie.com/eventhub/development/register.php"
        fields="[
        {'name':'name','view':'prefilled'},
        {'name':'first_name','view':'not_prefilled'},
        {'name':'last_name','view':'not_prefilled'},
        {'name':'gender'},
        {'name':'birthday'},
        {'name':'email'},
        {'name':'phone','description':'Phone Number','type':'text'},
        {'name':'location','description':'Location','type':'typeahead', 'categories':['city','country','state_province']}
        ]"
        width="940">
    </fb:registration>
  </div>
</div>

<br>
  
<?php
}

include 'footer.php';
?>