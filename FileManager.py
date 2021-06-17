from tkinter import filedialog, END, INSERT;

class FileManager:
    # Open the existing text file
    def open_file(self, text):
        # Open the dialog and ask the user to select a file
        existing_file = filedialog.askopenfile(filetypes=[('Text File', '.txt'), ('Python File', '.py')])
        # Need clear the existing text in the window first
        text.delete(1.0, END)
        # Then we can insert the new text
        text.insert(INSERT, existing_file.read())

    # Save the text to a file for future usage
    def save_file(self, text):
        # Open the dialog and ask the user to enter the file name
        new_file_path = filedialog.asksaveasfilename(filetypes=[('Text File', '.txt'), ('Python File', '.py')], defaultextension=".txt")
        new_file_name = new_file_path
        # Create the file with the text
        write = open(new_file_name, mode='w')
        write.write(text.get(1.0, END))
