<?php
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
      <h2>Log in to EventHub</h2>
    </div>
  </div>
</div>

<div class="login coat">
<form method="post">
  <div class="row-fluid">
    <div class="login-upper-pad">
      <label for="user_login">Email Address</label>
      <input class="span12" id="user_login" size="30" type="text" name="email" >
      <label for="user_password">Password</label>
      <input class="span12" id="user_password" size="30" type="password" name="password">
      <p class="help-block">
        <a href="#">Forgot your password?</a>
      </p>
    </div>
  </div>
  <div class="form-actions">
    <div class="row-fluid">
      <div class="span12">
        <button class="btn btn-primary btn-large" type="submit" name="login" style="float:left;margin-left:15px;">Log in</button>
        <label class="checkbox" for="user_remember_me" style="float:right;padding-top:8px;margin-right:20px;">
        <input id="user_remember_me" type="checkbox" value="1">
        Remember me
        </label>
      </div>
    </div>
  </div>
</form>
</div>

<br>

<?php
include 'footer.php';
?>