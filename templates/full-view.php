<?php
include 'header.php';
?>
      <div class="row-fluid">
      	<div class="span3"><br>
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header side-title-custom">Categories</li>
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
              	  <input type="checkbox" value="" checked="checked">
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
              
              <li class="nav-header side-title-custom">Locations</li>
              <label class="checkbox">
              	  <input type="checkbox" value="">
				  Ballard
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="">
				  Bellevue and Eastside
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="">
				  Capitol Hill
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="">
				  Columbia City
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="" checked="checked">
				  Downtown Seattle
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="">
				  Fremont
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="">
				  Georgetown
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="">
				  International District
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="">
				  Lake Union Area
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="">
				  Madison Park
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="">
				  Pioneer Square
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="">
				  Queen Anne
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="">
				  Southeast Seattle
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="">
				  Southside Seattle
			  </label>
			  <label class="checkbox">
              	  <input type="checkbox" value="" checked="checked">
				  University District
			  </label>
               <label class="checkbox">
              	  <input type="checkbox" value="">
				  West Seattle
			  </label>
            </ul>
		    <div class="input-prepend" style="padding: 10px 0 0 10px;">
		      <span class="add-on"><i class="icon-search"></i></span>
		      <input class="span10" id="inputIcon" type="text" placeholder="Search for events">
		    </div>
          </div><!--/.well -->
        </div><!--/span-->
        
        <div class="span9">
          <div class="row-fluid">
            <div class="span12">
              <h2>Upcoming Events &nbsp;<small>Sports / Downtown</small><button class="btn btn-medium btn-primary pull-right" type="button" data-toggle="modal" data-target="#myModal" style="margin-top:8px;" onclick="pop_create_event()">Create Event</button></h2>
              
<div id="myModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
              <h3 id="myModalLabel">Create an event</h3>
            </div>
            <div class="modal-body">
            
              	<div class="form-horizontal">
              	
                    <div class="control-group">
                        <label class="control-label-custom" for="input01">Event Title</label>
                        <div class="controls-custom">
                            <input type="text" class="span10" id="input01" name="title"> <span class="help-inline"></span>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        <label class="control-label-custom" for="input02">Start</label>
                        <div class="controls-custom controls-row">
                            <div class="input-append">
                                <input type="text" class="input-small datepicker" id="input02" name="startdate" style="text-align:center;" autocomplete="off" value="<?php echo date('m/d/Y'); ?>"><span id="picker-1" class="add-on btn"><i class="icon-calendar"></i></span>
                            </div>&nbsp;&nbsp;&nbsp;&nbsp;
                            <div class="input-append">
                            	<input type="text" class="input-mini" id="starttime" name="starttime" style="text-align:center;" autocomplete="off" value="12:00"><span id="clockswitch-1" class="add-on btn" type="button">&nbsp;PM&nbsp;</span>
                            </div>
                            <span class="help-inline"></span>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        <label class="control-label-custom" for="input03">Finish</label>
                        <div class="controls-custom controls-row">
                            <div class="input-append">
                                <input type="text" class="input-small datepicker" id="input03" name="enddate" style="text-align:center;" autocomplete="off" value="<?php echo date('m/d/Y'); ?>"><span id="picker-2" class="add-on btn"><i class="icon-calendar"></i></span>
                            </div>&nbsp;&nbsp;&nbsp;&nbsp;
                            <div class="input-append">
                            	<input type="text" class="input-mini" id="endtime" name="endtime" style="text-align:center;" autocomplete="off" value="4:00"><span id="clockswitch-2" class="add-on btn" type="button">&nbsp;PM&nbsp;</span>
                            </div>
                            <span class="help-inline"></span>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        <label class="control-label-custom" for="input04">Description</label>
                        <div class="controls-custom">
                            <textarea class="span10" id="input04" rows="5" name="description"></textarea>
                            <span class="help-inline"></span>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        <label class="control-label-custom" for="input05">Location</label>
                        <div class="controls-custom">
                            <select>
                              <option>Select a location</option>
							  <option>Downtown</option>
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
                                <span class="add-on">$</span><input type="text" class="input-small" id="input06" name="cost" placeholder="0.00">
                            </div>
                        </div>
                    </div>
                    
                    <div class="control-group">
                        <label class="control-label-custom" for="input07">Web URL</label>
                        <div class="controls-custom">
                            <div class="input-prepend">
                                <span class="add-on"><i class="icon-globe"></i></span><input type="text" class="input-xlarge" id="input07" name="url" placeholder="http://example.com">
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
			              	  <input type="checkbox" value="">
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
              <button class="btn btn-primary">Publish Event</button>
            </div>
          </div>
              
              <p>
              	<table class="table table-striped">
                    <tbody>
                     
                      <!--show more of this event-->
                    <tr>
                        <td>
                            <div class="event-title" style="padding-top:0;padding-bottom:0;">
                                <h3>Washington vs. USC Football Game </h3>
                            </div>
                            <p style="padding-top:5px;">
                                <strong>Saturday, October 13, 2012</strong><br>
                                4:00 PM - 7:30 PM
                            </p>
                              <p>Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p>
                              <p>
                                 <strong>CenturyLink Field</strong><br>
                                  800 Occidental Avenue South, Seattle, WA<br>
                                  <a href="http://www.centurylinkfield.com/">http://www.centurylinkfield.com/</a>
                              </p>
                              <p>
                                      <strong>Cost/Fees</strong><br>
                                      $20 for UW students; $50 for general public
                              </p>
                              <small><a href="index.php">&raquo; show less</a></small>
                        </td>     
                        <td width="240" height="500" style="padding:50 50">
                            <img src="photos/football.png" class="img-polaroid" >        
                        </td>
                      </tr>
                      <!--list of events-->
                      <tr>
                        <td width="240">
                                    <img src="photos/football.png" class="img-polaroid" style="width:230px;height:150px;">
                                    <p style="padding-top:5px;">
                                          <strong>Saturday, October 13, 2012</strong><br>
                                          4:00 PM - 7:30 PM
                                    </p>
                        </td>
                        <td>
                                <div class="event-title" style="padding-top:0;padding-bottom:0;">
                                          <h3>Washington vs. USC Football Game <small><a href="#">&raquo; more</a></small></h3>
                                </div>
                                  <p>Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p>
                                  <p>
                                          <strong>CenturyLink Field</strong><br>
                                          800 Occidental Avenue South, Seattle, WA<br>
                                          <a href="http://www.centurylinkfield.com/">http://www.centurylinkfield.com/</a>
                                  </p>
                                  <p>
                                          <strong>Cost/Fees</strong><br>
                                          $20 for UW students; $50 for general public
                                  </p>
                        </td>
                      </tr>
                      <tr>
                        <td width="240">
                                    <img src="photos/football.png" class="img-polaroid" style="width:230px;height:150px;">
                                    <p style="padding-top:5px;">
                                          <strong>Saturday, October 13, 2012</strong><br>
                                          4:00 PM - 7:30 PM
                                    </p>
                        </td>
                        <td>
                                <div class="event-title" style="padding-top:0;padding-bottom:0;">
                                          <h3>Washington vs. USC Football Game <small><a href="#">&raquo; more</a></small></h3>
                                </div>
                                  <p>Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p>
                                  <p>
                                          <strong>CenturyLink Field</strong><br>
                                          800 Occidental Avenue South, Seattle, WA<br>
                                          <a href="http://www.centurylinkfield.com/">http://www.centurylinkfield.com/</a>
                                  </p>
                                  <p>
                                          <strong>Cost/Fees</strong><br>
                                          $20 for UW students; $50 for general public
                                  </p>
                        </td>
                      </tr>
                      <tr>
                        <td width="240">
                                    <img src="photos/football.png" class="img-polaroid" style="width:230px;height:150px;">
                                    <p style="padding-top:5px;">
                                          <strong>Saturday, October 13, 2012</strong><br>
                                          4:00 PM - 7:30 PM
                                    </p>
                        </td>
                        <td>
                                <div class="event-title" style="padding-top:0;padding-bottom:0;">
                                          <h3>Washington vs. USC Football Game <small><a href="#">&raquo; more</a></small></h3>
                                </div>
                                  <p>Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p>
                                  <p>
                                          <strong>CenturyLink Field</strong><br>
                                          800 Occidental Avenue South, Seattle, WA<br>
                                          <a href="http://www.centurylinkfield.com/">http://www.centurylinkfield.com/</a>
                                  </p>
                                  <p>
                                          <strong>Cost/Fees</strong><br>
                                          $20 for UW students; $50 for general public
                                  </p>
                        </td>
                      </tr>
                      <tr>
                        <td width="240">
                                    <img src="photos/football.png" class="img-polaroid" style="width:230px;height:150px;">
                                    <p style="padding-top:5px;">
                                          <strong>Saturday, October 13, 2012</strong><br>
                                          4:00 PM - 7:30 PM
                                    </p>
                        </td>
                        <td>
                                <div class="event-title" style="padding-top:0;padding-bottom:0;">
                                          <h3>Washington vs. USC Football Game <small><a href="#">&raquo; more</a></small></h3>
                                </div>
                                  <p>Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p>
                                  <p>
                                          <strong>CenturyLink Field</strong><br>
                                          800 Occidental Avenue South, Seattle, WA<br>
                                          <a href="http://www.centurylinkfield.com/">http://www.centurylinkfield.com/</a>
                                  </p>
                                  <p>
                                          <strong>Cost/Fees</strong><br>
                                          $20 for UW students; $50 for general public
                                  </p>
                        </td>
                      </tr>				    
                    </tbody>
                </table>
              </p>
            </div><!--/span-->
            
            <ul class="pager">
				<li class="previous">
					<a href="#">&larr; Previous</a>
				</li>
				<li class="next">
					<a href="#">Next &rarr;</a>
				</li>
			</ul>
          </div><!--/row-->
        </div><!--/span-->

<?php
include 'footer.php';
?>