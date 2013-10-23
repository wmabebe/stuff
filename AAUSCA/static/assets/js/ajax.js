
$(function(){
	
	//$('#loanrequestsubmit').attr('disabled','disabled');
	
	$('#loanAmount').change(function () {
		var RequestData = $('#memberloanrequestform').serialize();
		$.post('/member_loan_request/', RequestData, function (data) {
			if (data.errors)
			{
				var errorReport = '<div class="alert alert-error">'+ data.errors +'</div>';
				$('#memberloanrequestform').show();				
				$('#loanrequestmsg').html(errorReport);
				$('#loanrequestsubmit').attr('disabled','disabled');							
			}
			else if (data.date)
			{
				var successReport = '<div class="alert alert-success">'+ data.date +'</div>';
				$('#memberloanrequestform').show();
				$('#loanrequestmsg').html(successReport);
				$('#loanrequestsubmit').attr('disabled',false);
			}			
		});
	});
});

/*

$(document).ready(function(){
     $('input[type="submit"]').attr('disabled','disabled');
     $('input[type="text"]').change(function(){
            if($(this).val != ''){
               $('input[type="submit"]').removeAttr('disabled');
            }
     });
 });
	
	$('#memberloanrequestform').submit(function(){

		var RequestData = $(this).serialize();
		$.post('/member_loan_request/',RequestData,serverResult).error(function(){alert('Problemo')});
		function serverResult(data,status){
			//if(status == 'success'){
				alert(status);
				$('#loanrequestmsg').html(data);
			//}
		}
		return false;
	});
}); 

/*
$(document).ready(function() {
		$("#memberloanrequestform").submit(function() {
			var amount = $("#loanAmount").val();
			var reason = $("#loanReason").val();
			$.ajax({
					url : "/member_loan_request/",
					type : "POST",
					dataType: "json",
					data : {
						xhr : 'xhr',
					loanAmount : amount,
					loanReason : reason
					//csrfmiddlewaretoken: '{{ csrf_token }}'
				},
				success : function(json) {
					alert(xhr.status + ": " + xhr.responseText);
					$('#loanrequestmsg').append( 'Server Response: ' + json.server_response);
				},
				error : function(xhr,errmsg,err) {
					alert(xhr.status + ": " + xhr.responseText);
				}
			});
		return false;
	});
});
*/