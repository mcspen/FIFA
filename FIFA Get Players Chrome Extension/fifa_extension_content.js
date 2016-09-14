// FIFA Extension Content JS
// The logic interacting with webpages.
// Sends messages to the background JS.

// Random unique name, to be used to minimize conflicts:
var EVENT_FROM_PAGE = '__rw_chrome_ext_' + new Date().getTime();
var EVENT_REPLY = '__rw_chrome_ext_reply_' + new Date().getTime();


// Listens for the start message, retrieves all player info, and returns that info to background.js
chrome.extension.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.type == "get-player-info") {
		
		// Get player info here
		var players = "Got Players!!!!!";
		
		
		
		
		
		var s = document.createElement('script');
		s.textContent = '(' + function(send_event_name, reply_event_name) {
			// NOTE: This function is serialized and runs in the page's context
			// Begin of the page's functionality
			window.hello = function(string) {
				sendMessage({
					type: 'sayhello',
					data: string
				}, function(response) {
					alert('Background said: ' + response);
				});
			};

			// End of your logic, begin of messaging implementation:
			function sendMessage(message, callback) {
				var transporter = document.createElement('dummy');
				// Handles reply:
				transporter.addEventListener(reply_event_name, function(event) {
					var result = this.getAttribute('result');
					if (this.parentNode) this.parentNode.removeChild(this);
					// After having cleaned up, send callback if needed:
					if (typeof callback == 'function') {
						result = JSON.parse(result);
						callback(result);
					}
				});
				// Functionality to notify content script
				var event = document.createEvent('Events');
				event.initEvent(send_event_name, true, false);
				transporter.setAttribute('data', JSON.stringify(message));
				(document.body||document.documentElement).appendChild(transporter);
				transporter.dispatchEvent(event);
			}
		} + ')(' + JSON.stringify(/*string*/EVENT_FROM_PAGE) + ', ' +
				   JSON.stringify(/*string*/EVENT_REPLY) + ');';
		document.documentElement.appendChild(s);
		s.parentNode.removeChild(s);
		
		
		
		
		
		
		//var xhr = new XMLHttpRequest();
		//xhr.open("GET", "https://utas.external.s2.fut.ea.com/ut/game/fifa16/club?count=97&level=10&type=1&start=0", true);
		//xhr.onreadystatechange = function() {
		  //if (xhr.readyState == 4) {
			// test test test
			//window.alert(xhr.responseText);
		  //}
		//}
		//xhr.send();
		
		//var actualCode = '$(".ng-scope").ajaxSuccess(function(event, xhr, ajaxOptions) {alert("xhr.reponseText")});';
		//var actualCode = '$(document).ajaxSuccess(function(event, xhr, ajaxOptions) {alert("xhr.reponseText")});';
		//var actualCode = "if(jQuery){alert('True');} else{alert('False');}";

		
		
		/*var actualCode =
			`alert("hello");
			(function() {
				alert("1");
				var XHR = XMLHttpRequest.prototype;
				// Remember references to original methods
				var open = XHR.open;
				var send = XHR.send;
				alert("2");
				alert(open);
				alert(send);

				// Overwrite native methods
				// Collect data: 
				alert("3");
				XHR.open = function(method, url) {
					this._method = method;
					this._url = url;
					return open.apply(this, arguments);
					alert("4");
				};

				// Implement "ajaxSuccess" functionality
				alert("5");
				XHR.send = function(postData) {
					this.addEventListener('load', function() {
						this._method // method
						this._url // url
						this.responseText // response body
						postData // request body
						alert("6");
						alert(postData);
					});
					alert("7");
					return send.apply(this, arguments);
				};
			})();`*/


		
		/*var script = document.createElement('script');
		script.textContent = actualCode;
		(document.head||document.documentElement).appendChild(script);
		script.remove();*/
		
		
		
		
		// Send response here
		chrome.runtime.sendMessage({type: "finish-getPlayersList", playerInfo: players}, function(response) {});
	}
});



// Handle messages from/to page:
document.addEventListener(EVENT_FROM_PAGE, function(e) {
    var transporter = e.target;
    if (transporter) {
        var request = JSON.parse(transporter.getAttribute('data'));
        // Example of handling: Send message to background and await reply
		alert("Handled message from page?")
        chrome.runtime.sendMessage({
            type: 'page',
            request: request
        }, function(data) {
            // Received message from background, pass to page
            var event = document.createEvent('Events');
            event.initEvent(EVENT_REPLY, false, false);
            transporter.setAttribute('result', JSON.stringify(data));
            transporter.dispatchEvent(event);
        });
    }
});



/*var actualCode = `jQuery.ajaxSuccess(function(event, xhr, ajaxOptions) {ajaxOptions.type})`;
var script = document.createElement('script');
script.textContent = actualCode;
(document.head||document.documentElement).appendChild(script);
script.remove();*/
