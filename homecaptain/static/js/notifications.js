function start(token){
    
    var notificationSocket = new WebSocket(
	SCHEME + '://' + window.location.host +
	    '/ws/?token=' + token);

    notificationSocket.onmessage = function(e) {
	var data = JSON.parse(e.data);
	console.log(e.data);
	var separator = "--------------------------------------------------------------"
	
	var message = 'Type: ' + data['type'] + '\n';
	if(data['type']!=='conversation'){
	    message += 'Message: ' + data['message'] + '\n';
	    message += 'Is Read? ' + data['is_read'] + '\n';
	    message += 'Timestamp: ' + data['created'] + '\n';
	    message += 'UID: ' + data['uid'] + '\n';
	    message += 'entity_type: ' + data['entity_type'] + '\n';
	    message += 'status: ' + data['status'] + '\n';
	    message += separator;
	} else {
	    message += JSON.stringify(data['conversation']);
	}
	document.querySelector('#notification-log').value += (message + '\n');
    };

    notificationSocket.onclose = function(e) {
	console.error('Notification socket closed unexpectedly');
    };

    document.querySelector('#notification-message-input').focus();
    document.querySelector('#notification-message-input').onkeyup = function(e) {
	if (e.keyCode === 13) {  // enter, return
	    document.querySelector('#notification-message-submit').click();
	}
    };

    document.querySelector('#notification-message-submit').onclick = function(e) {
	var messageInputDom = document.querySelector('#notification-message-input');
	var message = messageInputDom.value;
	notificationSocket.send(JSON.stringify(message));

	messageInputDom.value = '';
    };
}

var token = prompt("Please enter token", "");
start(token);
