function getAnswer() {

	var conversationHistory = document.getElementById("conversation-history");
	var questionInput = document.getElementById("question");

	question = questionInput.value;

	if (question.length == 0) {
		return;
	}

	conversationHistory.value += "    Me: " + question + "\n";

	if (window.XMLHttpRequest) {
		// code for IE7+, Firefox, Chrome, Opera, Safari
		request = new XMLHttpRequest();
	} else {
		// code for IE6, IE5
		request = new ActiveXObject("Microsoft.XMLHTTP");
	}

	request.onreadystatechange = function() {
		if ((this.readyState == 4) && (this.status == 200)) {
			conversationHistory.value += "    Jarvis: " + this.responseText + "\n";
			questionInput.value = "";
		}
	}

	request.open("GET", "http://localhost:8080/get_answer?question=" + question, true);
	request.send();
}