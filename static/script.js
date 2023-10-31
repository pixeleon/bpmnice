const validFileExtensions = ['bpmn'];

const resultsTextArea = document.getElementById('results');

function validateFile(fileName) {
    if (!fileName) {
        return "No file selected!";
    }

    const fileExtension = fileName.split('.').pop().toLowerCase();
    return validFileExtensions.includes(fileExtension) ? null : "Invalid file extension!";
}

function setResultsText(color, text) {
    resultsTextArea.style.color = color;
    resultsTextArea.value = text;
}

function submitForm(event) {
    event.preventDefault();

    const form = document.getElementById('fileUploadForm');
    const textArea = document.getElementById('results');
    const fileInput = document.getElementById('fileInput');

    const fileName = fileInput.value;

    let validation = validateFile(fileName);
    if (validation != null) {
        textArea.value = validation + " Please upload a valid .bpmn file";
        return;
    }

    const formData = new FormData(form);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(data => {
            textArea.value = data;
        })
        .catch(error => {
            textArea.value = 'Error: ' + error;
        });
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('fileUploadForm');
    form.addEventListener('submit', submitForm);
});

document.getElementById('clearFileInput').addEventListener('click', function() {
    document.getElementById('fileUploadForm').reset();
});

