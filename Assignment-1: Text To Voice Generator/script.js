let synth = window.speechSynthesis;
let voices = [];

function populateVoiceList() {
    voices = synth.getVoices();
    let voiceSelect = document.getElementById("voice-select");
    voiceSelect.innerHTML = "";

    voices.forEach((voice, index) => {
        let option = document.createElement("option");
        option.textContent = `${voice.name} (${voice.lang})`;
        option.value = index;
        voiceSelect.appendChild(option);
    });
}

// Load voices
populateVoiceList();
if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = populateVoiceList;
}

function speakText() {
    let textInput = document.getElementById("text-input").value;
    let selectedVoice = document.getElementById("voice-select").value;
    let rate = document.getElementById("rate").value;
    let pitch = document.getElementById("pitch").value;

    if (textInput === "") {
        alert("Please enter text to speak.");
        return;
    }

    let utterance = new SpeechSynthesisUtterance(textInput);
    utterance.voice = voices[selectedVoice];
    utterance.rate = rate;
    utterance.pitch = pitch;

    synth.speak(utterance);
}

function stopSpeaking() {
    synth.cancel();
}

function downloadAudio() {
    alert("Downloading feature is under development. Try recording your screen with audio for now.");
}
