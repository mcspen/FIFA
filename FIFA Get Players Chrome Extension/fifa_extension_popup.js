// FIFA Extension Popup JS
// The logic part of the popup.

window.onload = function() {
	document.getElementById("start_button").onclick = function() {
		chrome.extension.sendMessage({
			type: "start-getPlayersList"
		});
	}
}