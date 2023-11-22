function exportData(format) {
    let endpoint = format === 'csv' ? '/export_csv' : format === 'xlsx' ? '/export_xls' : '/export';

    fetch(endpoint, {
        method: 'GET',
    })
        .then(response => response.blob())
        .then(blob => {
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(new Blob([blob]));
            link.download = `analysis_results.${format}`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
        .catch(error => console.error('Error exporting data:', error));
}
