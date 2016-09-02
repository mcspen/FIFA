// FIFA Extension Background JS
// The logic running continuously for the extension.
// Sends messages to the content JS.

// Global variable for player info
var playerInfo = "Player List Not Retrieved... Please try again."

// Starts when extension is installed or upgraded
chrome.runtime.onInstalled.addListener(function() {
  // Replace all rules with a new rule
  chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
    chrome.declarativeContent.onPageChanged.addRules([
      {
        // Fires when a page's URL contains a the FIFA web-app URL.
        conditions: [
          new chrome.declarativeContent.PageStateMatcher({
            pageUrl: { urlContains: 'https://www.easports.com/fifa/ultimate-team/web-app'},
		  }),
		  new chrome.declarativeContent.PageStateMatcher({
            pageUrl: { urlContains: 'google'},
		  })
        ],
        // And shows the extension's page action.
        actions: [ new chrome.declarativeContent.ShowPageAction() ]
      }
    ]);
  });
});

// Listening for the popup message (and other one-time requests)
chrome.extension.onMessage.addListener(function(request, sender, sendResponse) {
	switch(request.type) {
		case "start-getPlayersList":
			getPlayersList();
		break;
	}
	return true;
});

// Listening for long-lived connections
/*chrome.extension.onConnect.addListener(function (port) {
	port.onMessage.addListener(function (message) {
		switch(port.name) {
			case "start-getPlayersList":
				getPlayersList();
			break;
		}
	});
});*/

// Function for getting the list of players
function getPlayersList() {
	window.alert("1")
	// Send message to content script to get player info
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
		chrome.tabs.sendMessage(tabs[0].id, {greeting: "get-player-info"}, function(response) {
			//playerInfo = response.farewell;
		});
	});
	window.alert("2")
	// Give user player info in prompt box
	window.prompt("Copy player info and save to blah file...", playerInfo);
}
