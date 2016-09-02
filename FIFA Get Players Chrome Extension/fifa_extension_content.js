// FIFA Extension Content JS
// The logic interacting with webpages.
// Sends messages to the background JS.

// Listens for the start message, retrieves all player info, and returns that info to background.js
chrome.extension.onMessage.addListener(function(request, sender, sendResponse) {
	window.alert("CONTENT PAGE!");
    if (request.greeting == "get-player-info") {
		sendResponse({farewell: "made it to the content page!"});
	}
});
