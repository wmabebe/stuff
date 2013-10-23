$(function(){

	$('#usermenulist li').mouseover(function(){
		$(this).addClass('activemenu')
	});
	$('#usermenulist li').mouseout(function(){
		$(this).removeClass('activemenu')
	});
	$("#usermenulist li a").click(function(){

		//$(this).popover('toggle');
		return false;
	});
	$('#accountbalance').click(function(){
		$('#requestloandiv').hide();
		$('#usereditprofilediv').hide();
		$('#userviewprofilediv').hide();
		$('#accountbalancediv').show();		
		return false;
	});
	$('#requestloan').click(function(){
		$('#accountbalancediv').hide();
		$('#usereditprofilediv').hide();
		$('#userviewprofilediv').hide();
		$('#requestloandiv').show();
		return false;
	});
	$('#loanrequestsubmit').click(function(){
      $('#memberloanrequestform').css('display','none');
      $('#memberguarantorrequestform').show();
      return false;
    });
    $('#editprofile').click(function(){
    	/*var li = $(this).closest('li');
    	$(li).addClass('activemenu');*/
    	$('#requestloandiv').hide();
    	$('#accountbalancediv').hide();
    	$('#userviewprofilediv').hide();
    	$('#usereditprofilediv').show();
    	return false;
    });

    $('#viewprofile').click(function(){
    	$('#requestloandiv').hide();
    	$('#accountbalancediv').hide();
    	$('#usereditprofilediv').hide();    	
    	$('#userviewprofilediv').show();
    	return false;
    });
    $('#userchangeun').click(function(){    	
    	$('#changepwdiv').hide();
    	$('#changeundiv').show();
    });
    $('#userchangepw').click(function(){
    	$('#changeundiv').hide();
    	$('#changepwdiv').show();
    });
    $('#cancelchangeun').click(function(){
    	$('#changeundiv').hide();
    });
    $('#cancelchangepw').click(function(){
    	$('#changepwdiv').hide();
    });
});