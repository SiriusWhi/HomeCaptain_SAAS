$(function(){
    if(getCookie('token')!==null){
	$("#id_user_token").text(getCookie('token'));
    }
    
    if(getCookie('token')===null && url('?code')!==undefined){

	$.ajax({
	    url: GOOGLE_CODE_TO_ACCESS_TOKEN_URL,
	    method: 'POST',
	    data: {code: url('?code')},
	    beforeSend: function(){
		$("#id_user_token").text("logging in...");
	    },
	    success: function(data){
		setCookie('token', data.key);
		window.location.href = "/";
	    },
	    complete: function(data){
		console.log(data);
	    }
	});
	
    }

    $("#id_logout_btn").click(function(){
	$.ajax({
	    url: '/api/auth/logout/',
	    headers: {
		'X-CSRFToken': getCookie('csrftoken'),
	    },
	    method: 'POST',
	    data: {},
	    success: function(){
		eraseCookie('token');
		window.location.href = '/';
	    }
	});
    });
    
    
});
