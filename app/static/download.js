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
