// document.addEventListener("DOMContentLoaded", function() {
//     const recordButton = document.getElementById('record-btn');
//     const responseList = document.getElementById('response-list');
//     let mediaRecorder;
//     let isRecording = false;
//     let audioChunks = [];

//     recordButton.addEventListener('click', function() {
//         if (!isRecording) {
//             startRecording();
//         } else {
//             stopRecording();
//         }
//     });

//     function startRecording() {
//         navigator.mediaDevices.getUserMedia({ audio: true })
//             .then((stream) => {
//                 mediaRecorder = new MediaRecorder(stream);
//                 mediaRecorder.start();
//                 recordButton.textContent = 'Stop Recording';
//                 isRecording = true;

//                 audioChunks = [];

//                 mediaRecorder.addEventListener("dataavailable", event => {
//                     audioChunks.push(event.data);
//                 });

//                 mediaRecorder.addEventListener("stop", () => {
//                     const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
//                     convertAndSendToServer(audioBlob);
//                 });
//             })
//             .catch(error => console.error('Error accessing media devices.', error));
//     }

//     function stopRecording() {
//         mediaRecorder.stop();
//         recordButton.textContent = 'Start Recording';
//         isRecording = false;
//     }

//     function convertAndSendToServer(audioBlob) {
//         const reader = new FileReader();
//         reader.onload = function(event) {
//             const arrayBuffer = event.target.result;
//             const wav = lamejs.WavHeader.readHeader(new DataView(arrayBuffer));
//             const samples = new Int16Array(arrayBuffer, wav.dataOffset, wav.dataLen / 2); 

//             const mp3Encoder = new lamejs.Mp3Encoder(1, wav.sampleRate, 128);
//             const mp3Buffer = [];
//             let remaining = samples.length;
//             const maxSamples = 1152;

//             for (let i = 0; remaining >= maxSamples; i += maxSamples) {
//                 const monoChunk = samples.subarray(i, i + maxSamples);
//                 const mp3buf = mp3Encoder.encodeBuffer(monoChunk);
//                 if (mp3buf.length > 0) {
//                     mp3Buffer.push(new Int8Array(mp3buf));
//                 }
//                 remaining -= maxSamples;
//             }

//             const d = mp3Encoder.flush();
//             if (d.length > 0) {
//                 mp3Buffer.push(new Int8Array(d));
//             }

//             const mp3Blob = new Blob(mp3Buffer, { type: 'audio/mpeg-3' });
//             sendDataToServer(mp3Blob);
//         };

//         reader.readAsArrayBuffer(audioBlob);
//     }

//     function sendDataToServer(audioBlob) {
//         const formData = new FormData();
//         formData.append('file', audioBlob, 'audio.mp3');

//         fetch('/ask', {
//             method: 'POST',
//             body: formData
//         })
//         .then(response => response.json())
//         .then(data => {
//             const li = document.createElement('li');
//             li.textContent = data.response;
//             responseList.appendChild(li);
//         })
//         .catch((error) => {
//             console.error('Error:', error);
//         });
//     }
// });







document.addEventListener("DOMContentLoaded", function() {
    const recordButton = document.getElementById('record-btn');
    const submitButton = document.getElementById('start-convo');
    const responseList = document.getElementById('response-list');
    let mediaRecorder;
    let isRecording = false;

    recordButton.addEventListener('click', function() {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    });

    function startRecording() {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then((stream) => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                recordButton.textContent = 'Stop Recording';
                isRecording = true;

                const audioChunks = [];

                mediaRecorder.addEventListener("dataavailable", event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener("stop", () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    // uncomment to use wav format instead
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audio = new Audio(audioUrl);
                    // audio.play();
                    sendDataToServer(audioBlob);
                    // convertAndSendToServer(audioBlob);
                });
            })
            .catch(error => console.error('Error accessing media devices.', error));
    }

    function stopRecording() {
        console.log('recording stopped');
        mediaRecorder.stop();
        recordButton.textContent = 'Start Recording';
        isRecording = false;
    }

    // submitButton.addEventListener('submit', function(event) {
    //     event.preventDefault();
    //     const company = document.getElementById('company').value;
    //     const jobfield = document.getElementById('job-field').value;
    //     const jobrole = document.getElementById('job-role').value;
    //     if (!jobfield || !jobrole) return;
        
    //     fetch('/updateparams', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({ field: jobfield, name: jobrole, company: company })
    //     })
    //     .then(response => response.json())
    //     .then(data => {})
    //     .catch((error) => {
    //         console.error('Error:', error);
    //     });
    // });

    function sendDataToServer(audioBlob) {
        const formData = new FormData();
        formData.append('file', audioBlob, 'audio.wav');

        fetch('/ask', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.user_input) {
                const li = document.createElement('li');
                li.textContent = data.user_input;
                if (data.status != 0){
                    li.style.cssText = 'color: red';
                }
                responseList.appendChild(li);
            }
            if (data.response) {
                const li = document.createElement('li');
                li.textContent = data.response;
                responseList.appendChild(li);
            }
            // if (data.audio_filename){
            const audioPlayer = document.getElementById('reply-audio');
            audioPlayer.src = `${data.audio_filename}`;
            audioPlayer.play();
            audioPlayer.style.display = 'block';
            // }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});

// document.addEventListener("DOMContentLoaded", function() {
//     const form = document.getElementById('question-form');
//     const responseList = document.getElementById('response-list');
//     const recordButton = document.getElementById('record-btn');
//     let mediaRecorder;
//     let isRecording = false;

//     form.addEventListener('submit', function(event) {
//         event.preventDefault();

//         const question = document.getElementById('question').value;
//         if (!question) return;
        
//         fetch('/ask', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ question: question })
//         })
//         .then(response => response.json())
//         .then(data => {
//             console.log(data);
//             const li = document.createElement('li');
//             li.textContent = data.response;
//             responseList.appendChild(li);
//         })
//         .catch((error) => {
//             console.error('Error:', error);
//         });

//         // Clear input
//         document.getElementById('question').value = '';
//     });

//     recordButton.addEventListener('click', function() {
//         if (!isRecording) {
//             startRecording();
//         } else {
//             stopRecording();
//         }
//     });

//     function startRecording() {
//         navigator.mediaDevices.getUserMedia({ audio: true })
//             .then((stream) => {
//                 mediaRecorder = new MediaRecorder(stream);
//                 mediaRecorder.start();
//                 recordButton.textContent = 'Stop Recording';
//                 isRecording = true;

//                 const audioChunks = [];

//                 mediaRecorder.addEventListener("dataavailable", event => {
//                     audioChunks.push(event.data);
//                 });

//                 mediaRecorder.addEventListener("stop", () => {
//                     const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
//                     sendDataToServer(audioBlob);

//                     const audioUrl = URL.createObjectURL(audioBlob);
//                     const audio = new Audio(audioUrl);
//                     audio.play();
//                 });
//             })
//             .catch(error => console.error('Error accessing media devices.', error));
//     }

//     function stopRecording() {
//         mediaRecorder.stop();
//         recordButton.textContent = 'Start Recording';
//         isRecording = false;
//     }

// });