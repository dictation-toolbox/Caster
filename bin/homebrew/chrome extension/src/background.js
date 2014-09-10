chrome.commands.onCommand.addListener(function(command) {
	console.log('Command:', command);

	var message = {};
	if (["pandoraDislike", "pandoraSkip", "pandoraLike"].indexOf(command) > -1) {
		message.site = "pandora";
	}

	message.msgtype = command;

	chrome.tabs.query({
		// url : "http://www.pandora.com"
	}, function(tabs) {
		for (var i = 0; i < tabs.length; i++) {
			if (tabs[i].url.indexOf("pandora") > -1) {
				chrome.tabs.sendMessage(tabs[i].id, message, null);
			}
		}
	});
});

