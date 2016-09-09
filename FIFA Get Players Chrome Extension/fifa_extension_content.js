// FIFA Extension Content JS
// The logic interacting with webpages.
// Sends messages to the background JS.

// Listens for the start message, retrieves all player info, and returns that info to background.js
chrome.extension.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.type == "get-player-info") {
		
		// Get player info here
		var players = "Got Players!!!!!";
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
		var actualCode = '$(document).ajaxSuccess(function(event, xhr, ajaxOptions) {alert("xhr.reponseText")});';
		//var actualCode = "if(jQuery){alert('True');} else{alert('False');}";
		var script = document.createElement('script');
		script.textContent = actualCode;
		(document.head||document.documentElement).appendChild(script);
		script.remove();
		
		// Send response here
		chrome.runtime.sendMessage({type: "finish-getPlayersList", playerInfo: players}, function(response) {});
	}
});

/*var actualCode = `jQuery.ajaxSuccess(function(event, xhr, ajaxOptions) {ajaxOptions.type})`;
var script = document.createElement('script');
script.textContent = actualCode;
(document.head||document.documentElement).appendChild(script);
script.remove();*/
