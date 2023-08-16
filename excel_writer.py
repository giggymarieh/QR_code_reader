import openpyxl
import pandas as pd
from datetime import datetime

class ExcelWriter:
    def __init__(self):
        pass

    def append_row_to_excel(self, file_path, value, timestamp, sheet_name):
        try:
            # Load the existing Excel workbook if it exists
            workbook = openpyxl.load_workbook(file_path)
        except FileNotFoundError:
            # Create a new workbook if the file doesn't exist
            workbook = openpyxl.Workbook()

        # Check if the specified sheet already exists
        if sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
        else:
            # Create a new sheet if it doesn't exist
            sheet = workbook.create_sheet(title=sheet_name)

        # Calculate the index for the new row (after the last row)
        insert_index = sheet.max_row + 1

        # Create a DataFrame with the new row data
        data = {'Value': value, 'Timestamp': timestamp}
        df_row = pd.DataFrame([data])

        # Convert the DataFrame row to a list
        row_values = df_row.values.tolist()[0]

        # Insert a new row at the calculated index
        sheet.insert_rows(insert_index)

        # Populate the cells in the new row with data
        for col, value in enumerate(row_values, start=1):
            sheet.cell(row=insert_index, column=col, value=value)

        # Save the modified workbook
        workbook.save(file_path)

        # Close the workbook
        workbook.close()

if __name__ == "__main__":
    writer = ExcelWriter()
    file_path = 'your_excel_file.xlsx'
    value = 'Some value'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet_name = 'Sheet1'

    writer.append_row_to_excel(file_path, value, timestamp, sheet_name)