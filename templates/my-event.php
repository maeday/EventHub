<?php
include 'header.php';
?>
      <div class="row-fluid">
      	<div class="span12"><br>
            <div class="tabbable tabs-left">
                <ul class="nav nav-tabs">
                    <li class="active"><a href="#tab1" data-toggle="tab">Recently Hosted</a></li>
                    <li><a href="#tab2" data-toggle="tab">Recently Attended</a></li>
                    <li><a href="#tab3" data-toggle="tab">My Profile</a></li>
                    
                </ul>
                <div class="tab-content">
                    <div class="tab-pane active" id="tab1">
                         <div class="span9">
                            <div class="row-fluid">
                                 <div class="span12">
                                 <h2>Recently Hosted &nbsp;</h2>

                                    <table class="table table-striped">
                                      <tbody>
                                        <tr>
                                          <td width="240">
                                            <img src="photos/football.png" class="img-polaroid" style="width:230px;height:150px;">
                                               <p style="padding-top:5px;">
                                                  <strong>Saturday, October 13, 2012</strong><br>
                                                  4:00 PM - 7:30 PM
                                               </p>
                                          </td>
                                          <td >
                                            <div class="event-title" style="padding-top:0;padding-bottom:0;">
                                                <h3>Washington vs. USC Football Game</h3>
                                            </div>
                                            <p>Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula. [...]</p>
                                                <p>
                                                   <strong>CenturyLink Field</strong><br>
                                                   800 Occidental Avenue South, Seattle, WA<br>
                                                   <a href="http://www.centurylinkfield.com/">http://www.centurylinkfield.com/</a>
                                                </p>
                                            <p>
                                                <strong>Cost/Fees</strong><br>
                                                $20 for UW students; $50 for general public
                                                <button class="btn btn-medium btn-primary pull-right" type="button" data-toggle="modal" data-target="#myModal" style="margin-top:8px;" onclick="pop_edit_event()" >Edit Event</button>
                                            </p>
                                          </td>
                                        </tr>				    	    
                                      </tbody>
                                    </table>
                                 </div><!--/span-->
                            </div><!--/row-->
                        </div><!--/span-->
                    </div>
                        <div class="tab-pane" id="tab2">
                            <p>Something nice goes here...</p>
                        </div>
                    <div class="tab-pane" id="tab3">
                        <p>Profilestuff...</p>
                        <button class="btn btn-medium btn-primary" type="button" data-toggle="modal" data-target="#myModal" style="margin-top:8px;" onclick="pop_edit_profile()">Edit Profile</button>			
                    </div>
                </div>
            </div>
        </div><!--/span-->
        
                     
<div id="myModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
              <h3 id="myModalLabel">Edit event</h3>
            </div>
            <div class="modal-body">
            
              	<div class="form-horizontal">
              	
                    <div class="control-group">
                        <label class="control-label-custom" for="input01" >Event Title</label>
                        <div class="controls-custom">
                            <input type="text" class="span10" id="input01" name="title" value="Washington vs. USC Football Game"> <span class="help-inline"></span>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        <label class="control-label-custom" for="input02">Start</label>
                        <div class="controls-custom controls-row">
                            <div class="input-append">
                                <input type="text" class="input-small datepicker" id="input02" name="startdate" style="text-align:center;" autocomplete="off" value="10/13/2012"><span id="picker-1" class="add-on btn"><i class="icon-calendar"></i></span>
                            </div>&nbsp;&nbsp;&nbsp;&nbsp;
                            <div class="input-append">
                            	<input type="text" class="input-mini" id="starttime" name="starttime" style="text-align:center;" autocomplete="off" value="4:00"><span id="clockswitch-1" class="add-on btn" type="button">&nbsp;PM&nbsp;</span>
                            </div>
                            <span class="help-inline"></span>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        <label class="control-label-custom" for="input03">Finish</label>
                        <div class="controls-custom controls-row">
                            <div class="input-append">
                                <input type="text" class="input-small datepicker" id="input03" name="enddate" style="text-align:center;" autocomplete="off" value="10/13/2012" ?>"><span id="picker-2" class="add-on btn"><i class="icon-calendar"></i></span>
                            </div>&nbsp;&nbsp;&nbsp;&nbsp;
                            <div class="input-append">
                            	<input type="text" class="input-mini" id="endtime" name="endtime" style="text-align:center;" autocomplete="off" value="7:30"><span id="clockswitch-2" class="add-on btn" type="button">&nbsp;PM&nbsp;</span>
                            </div>
                            <span class="help-inline"></span>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        <label class="control-label-custom" for="input04">Description</label>
                        <div class="controls-custom">
                            <textarea class="span10" id="input04" rows="5" name="description">Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.
                                  </textarea>
                            <span class="help-inline"></span>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        <label class="control-label-custom" for="input05">Location</label>
                        <div class="controls-custom">
                            <select>
                                <option>Downtown</option>
                                <option>Select a location</option>
				<option>University District</option>
				<option>Ballard</option>
				<option>Green Lake</option>
				<option>Northgate</option>
			    </select>
                            <span class="help-inline"></span>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        <label class="control-label-custom" for="input06">Cost</label>
                        <div class="controls-custom">
                            <div class="input-prepend">
                                <span class="add-on">$</span><input type="text" value="$20 for UW students; $50 for general public" class="input-small" id="input06" name="cost" placeholder="0.00">
                            </div>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        <label class="control-label-custom" for="input07">Web URL</label>
                        <div class="controls-custom">
                            <div class="input-prepend">
                                <span class="add-on"><i class="icon-globe"></i></span><input type="text" class="input-xlarge" id="input07" name="url" value="http://www.centurylinkfield.com/">
                            </div>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        <label class="control-label-custom" for="input08">Categories</label>
                        <div class="controls-custom controls-row">
			               <label class="checkbox">
			              	  <input type="checkbox" value="">
							  Music
						  </label>
						   <label class="checkbox">
			              	  <input type="checkbox" value="">
							  Arts
						  </label>
						   <label class="checkbox">
			              	  <input type="checkbox" value="" checked="checked">
							  Sports & Activities
						  </label>
						   <label class="checkbox">
			              	  <input type="checkbox" value="">
							  Festivals & Fairs
						  </label>
						   <label class="checkbox">
			              	  <input type="checkbox" value="">
							  Food
						  </label>
						   <label class="checkbox">
			              	  <input type="checkbox" value="">
							  Film
						  </label>
						   <label class="checkbox">
			              	  <input type="checkbox" value="">
							  Lectures
						  </label>
						   <label class="checkbox">
			              	  <input type="checkbox" value="">
							  Fashion
						  </label>
						   <label class="checkbox">
			              	  <input type="checkbox" value="">
							  Nightlife
						  </label>
						   <label class="checkbox">
			              	  <input type="checkbox" value="">
							  Kids & Family
						  </label>
						   <label class="checkbox">
			              	  <input type="checkbox" value="">
							  Charities
						  </label>
                        </div>
                    </div>
                    
              	</div>
              
            </div>
            <div class="modal-footer">
              <button class="btn" data-dismiss="modal">Cancel</button>
              <button class="btn btn-primary" >Edit Event</button>
            </div>
          </div>


<?php
include 'footer.php';
?>