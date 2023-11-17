import io
import pandas


def create_results_data_frame(results):
    return pandas.DataFrame(
        [(x.id, x.filename, x.total_tasks, x.invalid_tasks, x.score, x.created_time) for x in results],
        columns=['ID', 'Filename', 'Total tasks', 'Invalid tasks', 'Model score', 'Created at']
    )


def export_to_csv_file(data):
    data_frame = create_results_data_frame(data)
    export_file = io.BytesIO()
    data_frame.to_csv(export_file, index=False, encoding='utf-8')
    export_file.seek(0)
    return export_file


def export_to_xls_file(data):
    data_frame = create_results_data_frame(data)
    export_file = io.BytesIO()
    with pandas.ExcelWriter(export_file, engine='openpyxl') as writer:
        column_widths = {'A': 4, 'B': 40, 'C': 15, 'D': 15, 'E': 15, 'F': 16}
        data_frame.to_excel(writer, index=False, sheet_name='History')
        worksheet = writer.sheets['History']
        for column, width in column_widths.items():
            worksheet.column_dimensions[column].width = width
    export_file.seek(0)
    return export_file
