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
        $('#loanextensiondiv').hide();
        $('#loanrenewaldiv').hide();
		$('#accountbalancediv').show();		
		return false;
	});
	$('#requestloan').click(function(){
		$('#accountbalancediv').hide();
		$('#usereditprofilediv').hide();
		$('#userviewprofilediv').hide();
        $('#loanextensiondiv').hide();
        $('#loanrenewaldiv').hide();
		$('#requestloandiv').show();
		return false;
	});
	$('#loanrequestsubmit').click(function(){
        $('#usermessageboard').show();
        $('#loanrequestalert').show();
      //$('#memberloanrequestform').css('display','none');
      //$('#memberguarantorrequestform').show();
      return false;
    });
    $('#editprofile').click(function(){
    	/*var li = $(this).closest('li');
    	$(li).addClass('activemenu');*/
    	$('#requestloandiv').hide();
    	$('#accountbalancediv').hide();
    	$('#userviewprofilediv').hide();
        $('#loanextensiondiv').hide();
        $('#loanrenewaldiv').hide();
    	$('#usereditprofilediv').show();
    	return false;
    });

    $('#viewprofile').click(function(){
    	$('#requestloandiv').hide();
    	$('#accountbalancediv').hide();
    	$('#usereditprofilediv').hide();   
        $('#loanextensiondiv').hide();
        $('#loanrenewaldiv').hide(); 	
    	$('#userviewprofilediv').show();
    	return false;
    });
    $('#reportleave').click(function(){        
        $('#changepwdiv').hide();
        $('#changeundiv').hide();
        $('#reportleavediv').show();        
    });
    $('#userchangeun').click(function(){    	
        $('#reportleavediv').hide();         
    	$('#changepwdiv').hide();
    	$('#changeundiv').show();
    });
    $('#reportleavecancel').click(function(){
       $('#reportleavediv').hide();         
    });
    $('#userchangepw').click(function(){
        $('#reportleavediv').hide();         
    	$('#changeundiv').hide();
    	$('#changepwdiv').show();
    });
    $('#cancelchangeun').click(function(){
    	$('#changeundiv').hide();
		return false;
    });
    $('#cancelchangepw').click(function(){
    	$('#changepwdiv').hide();
		return false;
    });
    $('#loanextension').click(function(){
        $('#requestloandiv').hide();
        $('#accountbalancediv').hide();
        $('#usereditprofilediv').hide();   
        $('#userviewprofilediv').hide();  
        $('#loanrenewaldiv').hide();
        $('#loanextensiondiv').show();
    });    
    $('#loanrenewal').click(function(){
        $('#requestloandiv').hide();
        $('#accountbalancediv').hide();
        $('#usereditprofilediv').hide();   
        $('#userviewprofilediv').hide();  
        $('#loanextensiondiv').hide();
        $('#loanrenewaldiv').show();
    });
    $('#usernotification').mouseover(function(){
        $('#usernotificationdiv').show();
    });
    $('#usernotificationdiv').hover(function(){
        $('#usernotificationdiv').show();
    },
    function(){
        $('#usernotificationdiv').hide();
    });
    $('#usernotificationdiv').click(function(){
        $(this).hide();
    })

    $('#notifications').mouseover(function(){
        $('#notificationdiv').show();
    });
    $('#notificationdiv').hover(function(){
        $('#notificationdiv').show();
    },
    function(){
        $('#notificationdiv').hide();
    });

    $('#mem-2').click(function(){
        $('#requestdetails').modal();
    });

});
