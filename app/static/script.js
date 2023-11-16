const VALID_FILE_EXTENSIONS = ['bpmn'];
const BOOTSTRAP_INVALID_FEEDBACK_CLASS = 'is-invalid';
const BOOTSTRAP_VALID_FEEDBACK_CLASS = 'is-valid';

let gauge = null;

function validateFile(fileName) {
    if (!fileName) {
        return "No file selected!";
    }
    const fileExtension = fileName.split('.').pop().toLowerCase();
    return VALID_FILE_EXTENSIONS.includes(fileExtension) ? null : "Invalid file extension!";
}

function resetResults(invalidTasks, totalTasks, textarea) {
    invalidTasks.textContent = '0';
    totalTasks.textContent = '0';
    textarea.value = '';
    if (gauge !== null) {
        gauge.destroy();
        gauge = null;
    }
}

function submitForm(event) {
    event.preventDefault();

    const form = document.getElementById('fileUploadForm');
    const fileInput = document.getElementById('fileInput');
    const invalidFeedback = document.getElementById('fileInputFeedback');
    const invalidTasks = document.getElementById('invalidTasks');
    const totalTasks = document.getElementById('totalTasks');
    const labelsTextarea = document.getElementById('labels');

    resetResults(invalidTasks, totalTasks, labelsTextarea);

    let validation = validateFile(fileInput.value);
    if (validation != null) {
        fileInput.classList.add(BOOTSTRAP_INVALID_FEEDBACK_CLASS);
        invalidFeedback.style.display = 'block';
        invalidFeedback.textContent = validation + ' Please upload a valid *.bpmn file';
        return;
    } else {
        fileInput.classList.add(BOOTSTRAP_VALID_FEEDBACK_CLASS);
    }
    const formData = new FormData(form);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            invalidTasks.textContent = data.invalid_tasks;
            totalTasks.textContent = data.total_tasks;

            let labelsText = '';

            data.labels_score.forEach(item => {
                const label = item.label.trim() === "" ? '<EMPTY>' : item.label
                const conclusion = item.score === 1 ? '+' : '-';
                labelsText += conclusion + ' ' + label + '\n';
            });

            labelsTextarea.value = labelsText;

            gauge = new JustGage({
                id: 'scoreGauge',
                value: data.score * 100,
                min: 0,
                max: 100,
                label: 'Score',
                gaugeWidthScale: 1.0,
                relativeGaugeSize: true,
                levelColors: ["#ff0000", "#f9c802", "#a9d70b"]
            });

        })
        .catch(error => {
            labelsTextarea.value = 'Error: ' + error;
        });
}

function resetFeedback(input, feedback) {
    return function () {
        input.classList.remove(BOOTSTRAP_INVALID_FEEDBACK_CLASS);
        feedback.style.display = 'none';
    };
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('fileUploadForm');
    form.addEventListener('submit', submitForm);
    const input = document.getElementById('fileInput');
    const feedback = document.getElementById('fileInputFeedback');
    input.addEventListener('change', resetFeedback(input, feedback))
});

document.getElementById('clearFileInput').addEventListener('click', function () {
    document.getElementById('fileUploadForm').reset();
    const fileInput = document.getElementById('fileInput');
    const invalidFeedback = document.getElementById('fileInputFeedback');
    fileInput.classList.remove(BOOTSTRAP_INVALID_FEEDBACK_CLASS);
    invalidFeedback.style.display = 'none';
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


