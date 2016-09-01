// FIFA Extension Popup JS
window.onload = function() {
	document.getElementById("start_button").onclick = function() {
		chrome.extension.sendMessage({
			type: "get-player-list"
		});
	}
}