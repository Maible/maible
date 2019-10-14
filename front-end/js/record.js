//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;


var gumStream;				//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 						//MediaStreamAudioSourceNode we'll be recording
var rcrdng=false;

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");

//add events to
const record = document.getElementById('record');

document.addEventListener('keypress', listen);
recordButton.addEventListener('click', startRecording);
stopButton.addEventListener('click',stopRecording);
function listen(key){
	if(rcrdng == false && key.code == 'KeyK')
		startRecording();
	else if (rcrdng == true && key.code == 'KeyK')
		stopRecording();
}

function startRecording() {
	console.log("recordButton clicked");

    var constraints = { audio: true, video:false }

 	//	Disable the record button until we get a success or fail from getUserMedia()
	recordButton.disabled = true;
	stopButton.disabled = false;

	/* 	We're using the standard promise based getUserMedia()
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia */
	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
		// create an audio context after getUserMedia is called
		audioContext = new AudioContext();

		// assign to gumStream for later use
		gumStream = stream;

		// use the stream
		input = audioContext.createMediaStreamSource(stream);

		//Create the Recorder object and configure to record mono sound (1 channel)
		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		rec.record()
		console.log("Recording started");
		rcrdng = true;

	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
    	recordButton.disabled = false;
    	stopButton.disabled = true;
	});
}

function stopRecording() {
	console.log("stopButton clicked");

	//disable the stop button, enable the record too allow for new recordings
	stopButton.disabled = true;
	recordButton.disabled = false;

	//tell the recorder to stop the recording
	rec.stop();
	rcrdng = false;

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
	var url = URL.createObjectURL(blob);
	var filename = "order";						//name of .wav file to use during upload and download (without extendion)

	//save to disk link
	var link = document.createElement('a');
	link.href = url;
	link.download = filename+".wav";	//download forces the browser to donwload the file using the  filename

	//upload link
	var upload = document.createElement('a');
	upload.href="#";
	upload.addEventListener("click", function(event){
			  var xhr=new XMLHttpRequest();
			  xhr.onload=function(e) {
			      if(this.readyState === 4) {
			          console.log("Server returned: ",e.target.responseText);
			      }
			  };
			  var fd=new FormData();
			  fd.append("audio_data",blob, filename);
			  xhr.open("POST","upload.php",true);
			  xhr.send(fd);
	})
}
