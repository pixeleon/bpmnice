const validFileExtensions = ['bpmn'];

const resultsTextArea = document.getElementById('results');

let gauge = null;

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

function resetResults(invalidTasks, totalTasks) {
    invalidTasks.textContent = '0';
    totalTasks.textContent = '0'
    if (gauge !== null) {
        gauge.destroy();
        gauge = null;
    }
}

function submitForm(event) {
    event.preventDefault();

    const form = document.getElementById('fileUploadForm');
    const fileInput = document.getElementById('fileInput');
    const invalidTasks = document.getElementById('invalidTasks');
    const totalTasks = document.getElementById('totalTasks');
    const labelsTextarea = document.getElementById('labels');

    const fileName = fileInput.value;

    let validation = validateFile(fileName);
    if (validation != null) {
        labelsTextarea.value = validation + " Please upload a valid .bpmn file";
        resetResults(invalidTasks, totalTasks);
        return;
    }

    const formData = new FormData(form);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log('data: ' + data)
            invalidTasks.textContent = data.invalid_tasks;
            totalTasks.textContent = data.total_tasks;

            let labelsText = '';

            data.labels_score.forEach(item => {
                const style = item.score === 1 ? '(OK)' : '(NOT OK)';
                labelsText += item.label + ' ' + style + '\n';
            });

            labelsTextarea.innerHTML = labelsText;

            gauge = new JustGage({
                id: 'scoreGauge',
                value: data.score * 100,
                min: 0,
                max: 100,
                label: 'Score',
                width: 500,
                height: 250,
                gaugeWidthScale: 1.0,
                relativeGaugeSize: true,
                levelColors: ["#ff0000", "#f9c802", "#a9d70b"]
            });

        })
        .catch(error => {
            labelsTextarea.value = 'Error: ' + error;
            resetResults(invalidTasks, totalTasks)
        });
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('fileUploadForm');
    form.addEventListener('submit', submitForm);
});

document.getElementById('clearFileInput').addEventListener('click', function () {
    document.getElementById('fileUploadForm').reset();
});

document.addEventListener('DOMContentLoaded', function () {
    let buttons = document.querySelectorAll('.download-button');
    buttons.forEach(button => {
        button.addEventListener('click', function () {
            const analysisId = button.getAttribute('data-id');
            const downloadLink = document.createElement("a");
            downloadLink.href = `/download/${analysisId}`;
            downloadLink.download = "";
            downloadLink.click();
        });
    });
});


