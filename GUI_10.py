import tkinter as tk
from datetime import datetime
from tkinter import *
import pandas as pd
import pyodbc
from PIL import ImageTk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import filedialog
import os
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A3
from reportlab.platypus import Image as ReportlabImage
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image


script_dir = os.path.dirname(__file__)

root = tk.Tk()
root.geometry("800x685")
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
root.title(f"Material Handling - {current_time}")

# Creating the logo on the window
logo_path = os.path.join(script_dir, 'CTPL', 'CTPL2.png')
root.iconphoto(True, PhotoImage(file=logo_path))

# Creating the first Frame on the window
view_bar_frame = tk.Frame(root, width=5000, height=600)
view_bar_frame.pack(fill=X, padx=10, pady=10)
view_bar_frame.config(bg="#b0bed1", relief=RAISED, bd=5)

# Creating a logo inside a Frame
logo_img = ImageTk.PhotoImage(file=logo_path)
logo_w = tk.Label(view_bar_frame, image=logo_img)
logo_w.image = logo_img
logo_w.config(bg="#b0bed1")
logo_w.pack(side=tk.LEFT)
# ------------------------------------------------------------------------------------
# creating a Frame inside the view_bar_frame for View Report and Refresh button
generate = tk.Frame(view_bar_frame, width=500, height=600)
generate.pack(side=RIGHT, fill=Y)
generate.config(bg="#d5dfed")

# -----------------------------------------------------------------------------------

def connection():
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= AYUSHP-DELL\\SQLEXPRESS03;'
                          'Database = TAPR102_1;'
                          'Trusted_Connection=yes;')

    return conn


# ------------------------------------------------------------------------------------
# creating Table in Database
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server= AYUSHP-DELL\\SQLEXPRESS03;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

# Define the SQL command to create a table
# table_exists_query = ("IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Data_Log1') "
#                       "CREATE TABLE Data_Log1 (DateTime DATETIME , [User] NVARCHAR(50), [Operational Shift] NVARCHAR(50),"
#                       " [Station Name] NVARCHAR(50), [Process Name] NVARCHAR(50), [Battery ID] NVARCHAR(50), "
#                       "[Cycle Time] INT, [Glue Weight] FLOAT  );")
#
# cursor.execute(table_exists_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

# -----------------------------------------------------------------------------------------------------------------

# creating a function to remove displayed in the table
def refresh_frames():
    # Clear table content
    for row in table.get_children():
        table.delete(row)

    # Clear date entries
    start_date_entry.delete(0, tk.END)
    end_date_entry.delete(0, tk.END)

    # Clear battery ID entry
    battery_id_entry.delete(0, tk.END)
    var.set(0)

# creating the view() function to display the combined results in the table
def view():
    serial_number = 1

    if var.get() == 1:  # Filtering by date range
        start = start_date_entry.get_date().strftime('%Y-%m-%d')  # Getting an entry for date to be fetched
        end = end_date_entry.get_date().strftime('%Y-%m-%d')
        # Write the sql query to be performed to fetch the data from sql server
        sql = "SELECT * FROM TAPR102_1.dbo.Table_1 WHERE DateTime BETWEEN ? AND ?"
        cursor = connection().execute(sql, (start, end))
        rows = cursor.fetchall()
        for row in rows:
            date_time = row[0].strftime('%Y-%m-%d %H:%M:%S')
            table.insert(parent='', index=tk.END, iid=None, values=[serial_number, date_time] + list(row[1:]))
            serial_number += 1  # Increment serial number for each row
        root.update_idletasks()

    elif var.get() == 2:  # Filtering by battery ID
        battery_id_val = battery_id_entry.get()

        sql = "SELECT * FROM TAPR102_1.dbo.Table_1 WHERE [Battery ID] = ?"
        cursor = conn.execute(sql, battery_id_val)
        rows = cursor.fetchall()
        for row in rows:
            date_time = row[0].strftime('%Y-%m-%d %H:%M:%S')
            table.insert(parent='', index=tk.END, iid=None, values=[serial_number, date_time] + list(row[1:]))
            serial_number += 1  # Increment serial number for each row
        root.update_idletasks()
    else:
        pass

# creating a button called refresh inside the Frame generate
refresh_button = tk.Button(generate, text='Refresh', command=refresh_frames)
refresh_button.pack(side=tk.RIGHT, padx=5)
# =====================================================================

# creating second Frame on the window
toolBar_frame = tk.Frame(root, width=5000, height=1500)
toolBar_frame.config(bg="#b0bed1", relief=GROOVE, bd=5)
toolBar_frame.pack(fill=X, padx=10)

# creating the label for button View Report
view_report = tk.LabelFrame(toolBar_frame)
view_report.config(bg="#b0bed1", relief=FLAT, bd=5)
view_report.pack(fill=Y, side=LEFT)

# crating a tk.Intvar() variable for radiobuttons Option1 and Option2 i.e. Date Time and Battery ID
var = tk.IntVar()

# Function for condition to select and deselect the radiobuttons
def datetime():
    if var.get() == 1:
        start_date.grid(row=1, column=0)
        start_date_entry.grid(row=1, column=1)
        space.grid(row=1, column=2)

        end_date.grid(row=1, column=3)
        end_date_entry.grid(row=1, column=4)
        space1.grid(row=1, column=5)

        # remove the data of the previous radiobutton press
        battery_id.grid_forget()
        battery_id_entry.grid_forget()
        space2.grid_forget()

def Id():
    if var.get() == 2:
        battery_id.grid(row=1, column=1)
        battery_id_entry.grid(row=1, column=2, padx=3)
        space2.grid(row=1, column=3)

        # remove the data of the previous radiobutton press
        start_date.grid_forget()
        start_date_entry.grid_forget()
        space.grid_forget()

        end_date.grid_forget()
        end_date_entry.grid_forget()
        space1.grid_forget()

def Foam_Module():
    serial_number = 1

    if var.get() == 1:  # Filtering by date range
        start = start_date_entry.get_date().strftime('%Y-%m-%d')
        end = end_date_entry.get_date().strftime('%Y-%m-%d')
        sql = "SELECT * master.dbo.Data_Log1 WHERE [Process Name]='Foam Module' AND DateTime BETWEEN ? AND ?"
        cursor = connection().execute(sql, (start, end))
        rows = cursor.fetchall()
        for row in rows:
            date_time = row[0].strftime('%Y-%m-%d %H:%M:%S')
            table.insert(parent='', index=tk.END, iid=None, values=[serial_number, date_time] + list(row[1:]))
            serial_number += 1  # Increment serial number for each row
        root.update_idletasks()

    elif var.get() == 2:  # Filtering by battery ID
        battery_id_val = battery_id_entry.get()

        sql = "SELECT * FROM master.dbo.Data_Log1 WHERE [Process Name]='Foam Module' AND [Battery ID] = ?"
        cursor = connection().execute(sql, battery_id_val)
        rows = cursor.fetchall()
        for row in rows:
            date_time = row[0].strftime('%Y-%m-%d %H:%M:%S')
            table.insert(parent='', index=tk.END, iid=None, values=[serial_number, date_time] + list(row[1:]))
            serial_number += 1  # Increment serial number for each row
        root.update_idletasks()
    else:
        pass

def Gap_Filling():
    serial_number = 1

    if var.get() == 1:  # Filtering by date range
        start = start_date_entry.get_date().strftime('%Y-%m-%d')
        end = end_date_entry.get_date().strftime('%Y-%m-%d')

        sql = "SELECT * FROM master.dbo.Data_Log1 WHERE [Process Name]='Gap Filling' AND DateTime BETWEEN ? AND ?"
        cursor = connection().execute(sql, (start, end))
        rows = cursor.fetchall()
        for row in rows:
            date_time = row[0].strftime('%Y-%m-%d %H:%M:%S')
            table.insert(parent='', index=tk.END, iid=None, values=[serial_number, date_time] + list(row[1:]))
            serial_number += 1  # Increment serial number for each row
        root.update_idletasks()

    elif var.get() == 2:  # Filtering by battery ID
        battery_id_val = battery_id_entry.get()

        sql = "SELECT * FROM master.dbo.Data_Log1 WHERE [Process Name]='Gap Filling' AND [Battery ID] = ?"
        cursor = connection().execute(sql, battery_id_val)
        rows = cursor.fetchall()
        for row in rows:
            date_time = row[0].strftime('%Y-%m-%d %H:%M:%S')
            table.insert(parent='', index=tk.END, iid=None, values=[serial_number, date_time] + list(row[1:]))
            serial_number += 1  # Increment serial number for each row
        root.update_idletasks()

    else:
        pass

def Foam_Encloser():
    serial_number = 1

    if var.get() == 1:  # Filtering by date range
        start = start_date_entry.get_date().strftime('%Y-%m-%d')
        end = end_date_entry.get_date().strftime('%Y-%m-%d')

        sql = "SELECT * FROM master.dbo.Data_Log1 WHERE [Process Name]='Foam Encloser' AND DateTime BETWEEN ? AND ?"
        cursor = connection().execute(sql, (start, end))
        rows = cursor.fetchall()
        for row in rows:
            date_time = row[0].strftime('%Y-%m-%d %H:%M:%S')
            table.insert(parent='', index=tk.END, iid=None, values=[serial_number, date_time] + list(row[1:]))
            serial_number += 1  # Increment serial number for each row
        root.update_idletasks()

    elif var.get() == 2:  # Filtering by battery ID
        battery_id_val = battery_id_entry.get()

        sql = "SELECT * FROM master.dbo.Data_Log1 WHERE [Process Name]='Foam Encloser' AND [Battery ID] = ?"
        cursor = connection().execute(sql, battery_id_val)
        rows = cursor.fetchall()
        for row in rows:
            date_time = row[0].strftime('%Y-%m-%d %H:%M:%S')
            table.insert(parent='', index=tk.END, iid=None, values=[serial_number, date_time] + list(row[1:]))
            serial_number += 1  # Increment serial number for each row
        root.update_idletasks()
    else:
        pass

Var1 = IntVar()

button1 = tk.Radiobutton(view_report, text="Foam Module", value=1)
button1.grid(row=0, column=3, padx=10, pady=10)
button1.configure(variable=Var1)

button2 = tk.Radiobutton(view_report, text="Gap Filler", value=2)
button2.grid(row=0, column=4, padx=10, pady=10)
button2.configure(variable=Var1)

button3 = tk.Radiobutton(view_report, text="Foam Encloser", value=3)
button3.grid(row=0, column=5, padx=10, pady=10)
button3.configure(variable=Var1)

button4 = tk.Radiobutton(view_report, text="Combined", value=4)
button4.grid(row=0, column=6, padx=10, pady=10)
button4.configure(variable=Var1)
button4.select()

def clear_data():
    table.delete(*table.get_children())

def view_button():
    clear_data()
    if Var1.get() == 1:
        Foam_Module()
    elif Var1.get() == 2:
        Gap_Filling()
    elif Var1.get() == 3:
        Foam_Encloser()
    elif Var1.get() == 4:
        view()


view_report_button = tk.Button(generate, text="View Report", command=view_button)
view_report_button.config(relief=RAISED)
view_report_button.pack(side=tk.LEFT, padx=5)

Option1 = tk.Radiobutton(view_report, text="Date Time", value=1, command=datetime)
Option2 = tk.Radiobutton(view_report, text="Battery ID", value=2, command=Id)
Option1.grid(row=0, column=0, padx=5)
Option1.configure(variable=var)
Option2.grid(row=0, column=1, padx=5)
Option2.configure(variable=var)

start_date = tk.Label(view_report, text="Start-Date")
start_date.config(bg="#b0bed1")
start_date_entry = DateEntry(view_report, date_pattern='dd/mm/y')

end_date = tk.Label(view_report, text="End-Date")
end_date.config(bg="#b0bed1")
end_date_entry = DateEntry(view_report, date_pattern='dd/mm/y')

battery_id = tk.Label(view_report, text="Battery ID")
battery_id.config(bg="#b0bed1")
battery_id_entry = tk.Entry(view_report)

space = tk.Label(view_report, text="   ")
space.config(bg="#b0bed1")
space1 = tk.Label(view_report, text="   ")
space1.config(bg="#b0bed1")
space2 = tk.Label(view_report, text="   ")
space2.config(bg="#b0bed1")

# ---------------------------------------------------------------------------------------------------------------
menu_bar = tk.Menu(root)
menu_bar.config(font=("Arial", 12))
save_menu = tk.Menu(menu_bar, tearoff=0)
root.config(menu=menu_bar)


def table_info():
    if Var1.get() == 1:
        text1 = "Process Name : Foam Module"
        return text1
    elif Var1.get() == 2:
        text1 = "Process Name : Gap Filling"
        return text1
    elif Var1.get() == 3:
        text1 = "Process Name : Foam Encloser"
        return text1
    elif Var1.get() == 4:
        text1 = "Process Name : All Data "
        return text1


def About_data():
    global battery_id_entry
    start_d = start_date_entry.get_date().strftime('%Y-%m-%d')
    end_d = end_date_entry.get_date().strftime('%Y-%m-%d')
    battery_id1 = battery_id_entry.get()
    if Var1.get() == 1:
        if var.get() == 1:
            text1 = "Date From : {}  To : {}".format(start_d, end_d)
            return text1
        elif var.get() == 2:
            text1 = "Battery_ID  {}".format(battery_id1)
            return text1
    elif Var1.get() == 2:
        if var.get() == 1:
            text1 = "Date From : {}  To : {}".format(start_d, end_d)
            return text1
        elif var.get() == 2:
            text1 = "Battery_ID  {}".format(battery_id1)
            return text1
    elif Var1.get() == 3:
        if var.get() == 1:
            text1 = " Date From : {}  To : {}".format(start_d, end_d)
            return text1
        elif var.get() == 2:
            text1 = "Battery_ID  {}".format(battery_id1)
            return text1
    elif Var1.get() == 4:
        if var.get() == 1:
            text1 = " Date From : {}  To : {}".format(start_d, end_d)
            return text1
        elif var.get() == 2:
            text1 = " Battery_ID  {}".format(battery_id1)
            return text1


def savefile():
    try:
        global current_time
        current_t = current_time
        # Extract the hour, minute, and second
        hour = current_t.hour
        minute = current_t.minute

        # Convert them into strings
        hour_str = str(hour).zfill(2)
        minute_str = str(minute).zfill(2)
        current_time_str = f'{hour_str}:{minute_str}'
        data = []
        for i in table.get_children():
            data.append([table.set(i, column) for column in table['columns']])

        df = pd.DataFrame(data, columns=['Sr.no', 'DateTime', '[User]', '[Operational Shift]', '[Station Name]',
                                         '[Process Name]', '[Battery ID]', '[Cycle Time]', '[Glue Weight]'])

        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                                 filetypes=[("Excel", ".xlsx"), ("All files", ".*")])
        # Create a workbook
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        # Specify the width for each column (adjust as needed)
        for column in df:
            length = max(df[column].astype(str).map(len).max(), len(str(column))) + 2
            sheet.column_dimensions[openpyxl.utils.get_column_letter(df.columns.get_loc(column) + 1)].width = length

        # adding text to the cell A1
        text = table_info()
        font = openpyxl.styles.Font(size=10, name='Helvetica')
        font1 = openpyxl.styles.Font(size=16, name='Helvetica', bold=True)
        sheet['A6'] = text
        sheet['A7'] = "  "

        # Add logo and text to the Excel sheet
        logo = os.path.join(script_dir, 'CTPL', 'CTPL2.png')
        sheet.add_image(logo, 'A1')
        sheet['A5'] = f"Material Handling Report - {current_time_str}"

        sheet['A5'].font = font1
        sheet['A6'].font = font

        # Write DataFrame data to Excel
        for r in dataframe_to_rows(df, index=False, header=True):
            sheet.append(r)

        # Save the workbook
        workbook.save(file_path)

    except Exception as e:
        print(f'An error occurred: {e}')


save_menu.add_command(label="Excel Sheet", command=savefile)
save_menu.add_separator()
# ================================================================================================================

table_frame = tk.LabelFrame(root, width=5000, height=5000, text="Module Report", font=('Times New Roman', 20, 'bold'))
table_frame.config(relief=GROOVE, bd=5)
table_frame.pack(padx=10, fill=BOTH)

# table_name=tk.Label(table_frame, text="Module Report", font=('Times New Roman',20, 'bold'))
# table_name.pack()
# ---------------------------------------------------------------------------------------------------------

table = ttk.Treeview(table_frame, columns=(
    'Sr.no', 'DateTime', 'User', 'Operational Shift', 'Station Name', 'Process Name', 'Battery ID', 'Cycle Time',
    'Glue Weight'
), show="headings", height=1000)

# --------------------------------------------------------------------------------------------------
scrollbar_table = ttk.Scrollbar(table_frame, orient='horizontal', command=table.xview)
table.configure(xscrollcommand=scrollbar_table.set)
scrollbar_table.place(relx=0, rely=1, relwidth=1, anchor='sw')
# -------------------------------------------------------------------------------------------------

table.column("#0", width=0, stretch=tk.NO)
# table.column("Sr.No", anchor=tk.CENTER, width=50)
table.column("Sr.no", anchor=tk.CENTER, width=50)
table.column("DateTime", anchor=tk.CENTER, width=100)
table.column("User", anchor=tk.CENTER, width=100)
table.column("Operational Shift", anchor=tk.CENTER)
table.column("Station Name", anchor=tk.CENTER, width=100)
table.column("Process Name", anchor=tk.CENTER, width=100)
table.column("Battery ID", anchor=tk.CENTER)
table.column("Cycle Time", anchor=tk.CENTER)
table.column("Glue Weight", anchor=tk.CENTER)

table.heading("Sr.no", text="Sr.no")
# table.heading("Sr.No", text="Sr.No")
table.heading("DateTime", text="DateTime")
table.heading("User", text="User")
table.heading("Operational Shift", text="Operational Shift")
table.heading("Station Name", text="Station Name")
table.heading("Process Name", text="Process Name")
table.heading("Battery ID", text="Battery ID")
table.heading("Cycle Time", text="Cycle Time")
table.heading("Glue Weight", text="Glue Weight")

table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


def truncate_string(string, max_length):
    if string is None:
        return ''  # or return 'Error: None input string'
    elif len(string) > max_length:
        return string[:max_length - 3] + '...'
    else:
        return string


def create_image_table(image_path):
    img = Image(image_path)
    img_width = 250 * mm  # You can adjust this value according to your needs
    img.drawWidth = img_width

    img_table_data = [[img]]

    # Specify the width of the image column
    img_col_widths = [img_width]

    img_table = Table(img_table_data, colWidths=img_col_widths)
    img_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return img_table


def generate_pdf():
    try:
        global table, Date_Time
        current_t = Date_Time
        # Extract the hour, minute, and second
        hour = current_t.hour
        minute = current_t.minute

        # Convert them into strings
        hour_str = str(hour).zfill(2)
        minute_str = str(minute).zfill(2)

        # Create a new string that represents the current time in the format you want
        current_time_str = f'{hour_str}:{minute_str}'
        pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf")
        pdf = SimpleDocTemplate(pdf_filename, pagesize=A3)
        elements = []
        img = os.path.join(script_dir, 'CTPL', 'CTPL2.png')
        elements.append(img)

        # Adding text to the pdf
        text = f"Material Handling Report - {current_time_str}"
        text1 = table_info()
        text2 = About_data()

        body_text_style = ParagraphStyle('BodyText', fontName='Helvetica', fontSize=20, leading=18, bold=True,
                                         spaceBefore=15)
        body_text_style1 = ParagraphStyle('BodyText', fontName='Helvetica', fontSize=14, leading=18,
                                          spaceBefore=10)
        body_text_style2 = ParagraphStyle('BodyText', fontName='Helvetica', fontSize=12, leading=18,
                                          spaceBefore=10, spaceAfter=35)
        p = Paragraph(text, style=body_text_style)
        p1 = Paragraph(text1, style=body_text_style1)
        p2 = Paragraph(text2, style=body_text_style2)
        elements.append(p)
        elements.append(p1)
        elements.append(p2)

        # Get table data
        table_data = []
        headings = ['Sr.no', 'DateTime', 'User', 'Operational Shift', 'Station Name', 'Process Name', 'Battery ID',
                    'Cycle Time', 'Glue Weight']
        table_data.append(headings)

        for item in table.get_children():
            values = [truncate_string(table.item(item, 'values')[0], 20),
                      truncate_string(table.item(item, 'values')[1], 20),
                      truncate_string(table.item(item, 'values')[2], 20),
                      truncate_string(table.item(item, 'values')[3], 20),
                      truncate_string(table.item(item, 'values')[4], 20),
                      truncate_string(table.item(item, 'values')[5], 20),
                      truncate_string(table.item(item, 'values')[6], 20),
                      truncate_string(table.item(item, 'values')[7], 20),
                      truncate_string(table.item(item, 'values')[8], 20)]

            table_data.append(values)

        # Calculate column widths based on content
        col_widths = [max(len(str(row[i])) for row in table_data) * 30 for i in range(len(headings))]

        # Define the table style with adjusted column widths
        style = TableStyle([
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                               ('BOTTOM PADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), '#d5dfed'),
                               ('GRID', (0, 0), (-1, -1), 1, '#000000')
                           ] + [('WIDTH', (i, 0), (i, -1), col_widths[i]) for i in range(len(headings))])

        # Create a Table object and apply the style
        table = Table(table_data)
        table.setStyle(style)
        elements.append(Table(table_data, style=style, hAlign='CENTER'))

        # Build the PDF document
        pdf.build(elements)

    except Exception as e:
        print(f'An error occurred: {e}')


save_menu.add_command(label="PDF", command=generate_pdf)
menu_bar.add_cascade(label="Save as", menu=save_menu, font=("Arial", 12))

root.mainloop()
