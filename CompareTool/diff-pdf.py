from io import StringIO
import tkinter as tk
from tkinter import filedialog, messagebox
from PdfToTextConverter import PdfToText
from FolderHelper import*

global source_file_path, target_file_path, margin_value, output_file_path
source_file_path = ''
target_file_path = ''
margin_value = 0.2
output_file_path = source_file_path


def get_source_file_path():
    global source_file_path
    #source_file_path = filedialog.askopenfilename(filetypes=[("PDF files", ".pdf"), ('All Files', '*.*')])
    source_file_path= filedialog.askdirectory()
    messagebox.showinfo("INFO", f"Source file {source_file_path} uploaded.")
    print(source_file_path)


def get_target_file_path():
    global target_file_path
    #target_file_path = filedialog.askopenfilename(filetypes=[("PDF files", ".pdf"), ('All Files', '*.*')])
    target_file_path = filedialog.askdirectory()
    messagebox.showinfo("INFO", f"Target file {target_file_path} uploaded.")
    print(target_file_path)


def update_output_filename(entry):
    global output_file_path
    output_file_path = filedialog.askdirectory()
    #if output_file_path is None or output_file_path == '':
       # output_file_path = 'output.html'
    messagebox.showinfo("INFO", f"Target file {output_file_path} uploaded.")   
    print(output_file_path)


def update_margin(entry):
    global margin_value
    margin_value = entry.get()
    try:
        margin_value = float(margin_value)
    except:
        margin_value = 0.2
    print(margin_value)


def merge_html(output_html1, output_html2):
    html = StringIO()
    html.write('<!DOCTYPE HTML PUBLIC>\n')
    html.write('<html><head>\n')
    html.write('<meta http-equiv="Content-Type" content="text/html; charset=%s">\n' % 'utf-8')
    html.write('</head><body>\n')

    html.write('<table><tr><td>\n')
    html.write(output_html1)
    html.write('</td>\n')
    html.write('<td>\n')
    html.write(output_html2)
    html.write('</td></tr></table>\n')

    html.write('</body></html>\n')
    return html.getvalue()


def compare_pdf(file1folder, file2folder, output_file, compare_margin=0.2):
    sourcefiles=FilterFilesinFolder(file1folder)
    destfiles=FilterFilesinFolder(file2folder)      
    if output_file:      
        if  len (sourcefiles) == len (destfiles):
            for file1, file2 in zip( sourcefiles, destfiles):
                file1filename =  os.path.basename(file1)
                file2filename =  os.path.basename(file2)
                if file1 is not None and file1 != '' and file2 is not None and file2 != '':
                    if file1filename != file2filename:
                       matchedfile = GetMatchedFile(destfiles,file1filename)
                       file2 = matchedfile
                    pdf_reader = PdfToText()
                    output_html1 = pdf_reader.compare_pdf(file1, file2, 'AS-IS', compare_margin=compare_margin)
                    output_html2 = pdf_reader.compare_pdf(file2, file1, 'TO-BE', 650, compare_margin=compare_margin)

                    html = merge_html(output_html1, output_html2)
                    file1filename = os.path.splitext(file1filename)[0]
                    file2filename = os.path.splitext(file2filename)[0]
                    createPath = os.path.join(output_file,file1filename+'_'+file2filename)
                    CreateFolder(createPath)
                    fullouputfile = os.path.join(createPath,'outputfile.html')

                    f_out = open(fullouputfile, 'w', -1, 'utf-8')
                    f_out.write(html)
                    messagebox.showinfo("INFO", f"Comparison completed. \nResult saved in {output_file} file.")

                    global source_file_path, target_file_path, margin_value, output_file_path
                    source_file_path = ''
                    target_file_path = ''
                    margin_value = 0.2
                    output_file_path = ''

                else:
                    messagebox.showerror("ERROR", "Please Upload a file first")
        else:
            messagebox.showerror("ERROR", "Source and Destination file count mismatch") 
    else:
        messagebox.showerror("ERROR", "Please Upload Output Folder")        

def replace_string_to_sql_format(sql_str):
    sql_str = str(sql_str)
    sql_str = sql_str.replace('\\', '\\\\')
    sql_str = sql_str.replace("'", "\\'")
    return sql_str


def main():
    global source_file_path, target_file_path, margin_value, output_file_path
    scores = tk.Tk()
    scores.geometry('350x200')
    scores.winfo_screenwidth(), scores.winfo_screenheight()
    scores.resizable(width=False, height=False)

    label1 = tk.Label(scores, text="PDF Compare Tool", font=("Verdana", 20))
    label1.grid(row=0, column=0, columnspan=4)

    uploadFile1 = tk.Button(
        scores,text="Upload Source Folder",width=20, font=("Verdana", 9),command=get_source_file_path)
    uploadFile1.grid(row=1, column=0, pady=7)

    uploadFile2 = tk.Button(
        scores,text="Upload Target Folder",width=20,font=("Verdana", 9), command=get_target_file_path)
    uploadFile2.grid(row=1, column=1, padx=10, pady=7)

    output_file = tk.Entry(scores)
    output_file.insert(0, output_file_path)
    output_file.grid(row=2, column=0, pady=5)
    update_output_file_btn = tk.Button(
        scores, text="Upload Output Folder", width=20,font=("Verdana", 9), command=lambda: update_output_filename(output_file))
    update_output_file_btn.grid(row=2, column=1, padx=10, pady=5)
    
    margin = tk.Entry(scores)
    margin.insert(0, margin_value)
    margin.grid(row=3, column=0, pady=5)
    update_margin_btn = tk.Button(
        scores, text="Update Margin Value", width=20,font=("Verdana", 9), command=lambda: update_margin(margin))
    update_margin_btn.grid(row=3, column=1, padx=10, pady=5)

    dfButton = tk.Button(
        scores,text="PDF Compare",width=20,bg="green",fg="white",font=("Verdana", 9),
        command=lambda: compare_pdf(source_file_path,target_file_path, output_file_path, margin_value))
    dfButton.grid(row=4, column=0, pady=5)
    
    closeButton = tk.Button(
        scores,text="Close",width=20,bg="red",fg="white",font=("Verdana", 9),command=exit)
    closeButton.grid(row=4, column=1, padx=10, pady=5)

    scores.mainloop()


if __name__ == "__main__":
    main()