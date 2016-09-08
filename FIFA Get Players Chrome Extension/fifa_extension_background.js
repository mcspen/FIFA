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
		
		case "finish-getPlayersList":
			playerInfo = request.playerInfo;
			outputPlayersList();
		break;
	}
	return true;
});

// Function for getting the list of players
function getPlayersList() {
	// Send message to content script to get player info
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
		chrome.tabs.sendMessage(tabs[0].id, {type: "get-player-info"}, function(response) {});
	});
}

// Function for getting the list of players
function outputPlayersList() {
	// Give user player info in prompt box
	window.prompt("Copy and save the follwing player information to players.txt file in the FIFA App folder.", playerInfo);
	console.log("Stuffffff");
	//var xhr = new XMLHttpRequest();
	//xhr.open("GET", "https://utas.external.s2.fut.ea.com/ut/game/fifa16/club?count=97&level=10&type=1&start=0", true);
	//xhr.onreadystatechange = function() {
	  //if (xhr.readyState == 4) {
		// test test test
		//window.alert(xhr.responseText);
	  //}
	//}
	//xhr.send();
}

//chrome.webRequest.onBeforeRequest.addListener(function(details){
  //console.log(details.responseHeaders);
  //window.alert("Background Headers received!");
//}, {urls: ["http://*/*", "https://*/*"]},["requestBody"]);
