chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	console.log(sender.tab ? "from a content script:" + sender.tab.url : "from the extension");
	// if (request.msgtype == "hello")
	// sendResponse({farewell: "goodbye"});
	console.log(" this should be seen on the Pandora page only");
	var btn = null;
	switch(request.msgtype) {
	case "pandoraDislike":
		btn = document.getElementsByClassName("thumbDownButton")[0].firstChild;
		//<div class="disabled" style="opacity: 0.01; display: none;"></div>

		break;
	case "pandoraLike":
		btn = document.getElementsByClassName("thumbUpButton")[0].firstChild;
		break;
	case "pandoraSkip":
		btn = document.getElementsByClassName("skipButton")[0].firstChild;
		break;
	}
	btn.click();
});
