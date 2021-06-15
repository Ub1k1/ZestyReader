# tkinter is the standard Python interface to the Tk GUI toolkit.
# https://docs.python.org/3/library/tkinter.html

# pyttsx3 is a text-to-speech conversion library in Python.
# Unlike alternative libraries, it works offline, and is compatible with both Python 2 and 3.
# https://pypi.org/project/pyttsx3/

# I think lines 10 to 13 are probably unnecessary here. import * already imports everything in the tkinter package. Maybe try removing those lines and see if it still works?
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from tkinter import colorchooser
import tkinter.scrolledtext as scrolledtext
import pyttsx3

# Initialize pyttsx3
engine = pyttsx3.init()
# Produce a available voice list
voices = {}
system_voices = engine.getProperty("voices")
for system_voice in system_voices:
    voices[system_voice.name] = system_voice.id

# Create the application window.
root = Tk()
root.title("Zesty - A Visual and Audio Tool")
# The window has width of 800 pixels and height of 700 pixels
# Initial position from top left corner is 200 pixels right and 50 pixels down
root.geometry("800x700+200+50")
# Make the application window resizable
root.resizable(True, True)
root.minsize(800, 700)

# Tag sequence to mark the text properties
tag_sequence = 0

# Open the existing text file
def open_file():
    # Open the dialog and ask the user to select a file
    existing_file = filedialog.askopenfile(filetypes=[('Text File', '.txt'), ('Python File', '.py')])
    # Need clear the existing text in the window first
    text.delete(1.0, END)
    # Then we can insert the new text
    text.insert(INSERT, existing_file.read())


# Save the text to a file for future usage
def save_file():
    # Open the dialog and ask the user to enter the file name
    new_file_path = filedialog.asksaveasfilename(filetypes=[('Text File', '.txt'), ('Python File', '.py')], defaultextension=".txt")
    new_file_name = new_file_path
    # Create the file with the text
    write = open(new_file_name, mode='w')
    write.write(text.get(1.0, END))


# Mark the selected text for later
def copy_text():
    # Need clear the clipboard first
    root.clipboard_clear()
    # Append the selected text to the clipboard
    text.clipboard_append(text.selection_get())


# Cut the selected text
def cut_text():
    # Need clear the clipboard first
    root.clipboard_clear()
    # Append the selected text to the clipboard
    text.clipboard_append(text.selection_get())
    # Delete the selected text
    text.delete(SEL_FIRST, SEL_LAST)


# Paste the selected text
def paste_text():
    # Paste the selected text at the cursor
    text.insert(INSERT, root.clipboard_get())
    # Need to clear keyboard a
    # root.clipboard_clear()


# To undo the change
def undo_text():
    text.edit_undo()


# To redo the change
def redo_text():
    text.edit_redo()


# Search the text and highlight words 
def find_text():
    # Create a popup window for search function, and the popup is transient (temporary) to the main window
    search_popup = Toplevel(root)
    search_popup.title('Word Search')
    search_popup.transient(root)
    search_popup.resizable(False, False)
    # Initial position from top left corner is 800 pixels right and 75 pixels down
    search_popup.geometry("+800+75")
    # The popup window contains a Label and Entry to allow users to enter the word
    Label(search_popup, text="Enter a word: ").grid(row=0, column=0)
    search_input = Entry(search_popup, width=20)
    search_input.grid(row=0, column=1, padx=2)
    search_input.focus_set()
    # Action button to search or cancel.
    # If you need pass a parameter to the function, must use 'lambda:' keyword
    Button(search_popup, text="Search", command=lambda: find_text_search(search_input.get())).grid(row=1, column=0, padx=2, pady=2, sticky="E")
    Button(search_popup, text="Close", command=lambda: find_text_close(search_popup)).grid(row=1, column=1, padx=2, pady=2, sticky="W")


# Search the text from the beginning to the end. If the word found, highlight it in yellow
def find_text_search(word):
    text.tag_remove("found_text", 1.0, END)
    text.tag_config("found_text", foreground="purple")
    # Search the text with nocase=1 (ignore case, case insensitive)
    index = 1.0
    while index:
        index = text.search(word, nocase=1, index=index, stopindex=END)
        if index:
            # Text index is following the row.column format. Means if the starting point is 1.277 (row 1, column 277),
            # and the search keyword is 3 characters long, then the new index is 1.277+3c (means row 1, column 277 plus 3 characters)
            new_index = str(index) + "+" + str(len(word)) + "c"
            text.tag_add('found_text', index, new_index)
            index = new_index


# Remove the highlight and close the search popup window
def find_text_close(search_popup):
    text.tag_remove("found_text", 1.0, END)
    search_popup.destroy()


# Popup window for how to use the application
def help_popup():
    # Create a popup window for help function, and the popup is transient (temporary) to the main window
    help_panel = Toplevel(root)
    help_panel.title('Hep')
    help_panel.transient(root)
    help_panel.resizable(False, False)
    # Initial position from top left corner is 250 pixel right and 200 pixel down
    help_panel.geometry("550x450+250+200")
    # Create each help items for the first toolbar
    create_help_item(help_panel, 0, "Open:", "Explanation")
    create_help_item(help_panel, 1, "Save:", "Explanation")
    create_help_item(help_panel, 2, "Copy:", "Explanation")
    create_help_item(help_panel, 3, "Cut:", "Explanation")
    create_help_item(help_panel, 4, "Paste:", "Explanation")
    create_help_item(help_panel, 5, "Undo:", "Explanation")
    create_help_item(help_panel, 6, "Redo:", "Explanation")
    create_help_item(help_panel, 7, "Find:", "Explanation")
    # Create each help items for the second toolbar
    create_help_item(help_panel, 8, "------", "")
    create_help_item(help_panel, 9, "Font:", "Explanation")
    create_help_item(help_panel, 10, "Bold:", "Explanation")
    create_help_item(help_panel, 11, "Italic:", "Explanation")
    create_help_item(help_panel, 12, "Underline:", "Explanation")
    create_help_item(help_panel, 13, "Color:", "Explanation")
    # Create each help items for the third toolbar
    create_help_item(help_panel, 14, "------", "")
    create_help_item(help_panel, 15, "Explanation")


# Create each help item by passing in the parent widget and row number, with the function name and description of the function
def create_help_item(parent_widget, row_number, function_name, function_description):
    Label(parent_widget, text=function_name, font="Arial 10 bold").grid(row=row_number, column=0, padx=2, pady=2, sticky="W")
    Label(parent_widget, text=function_description, font="Arial 10").grid(row=row_number, column=1, padx=20, pady=2, sticky="W")


# Make the highlighted text bold
def bold_text():
    # We need make the tag_sequence as global, so any change to tag_sequence will be visible from other methods
    global tag_sequence
    # Check if there's any selected text. If no text is selected, no need for further action
    if text.tag_ranges("sel"):
        # Get a list of existing tag for the selected text
        tags = text.tag_names(SEL_FIRST)
        tag_found = 0
        # Check if the selected text has a bold tag
        for tag_name in tags:
            if tag_name.startswith("bold_text_"):
                tag_found = 1
        if tag_found == 1:
            # If the selected text already has a bold tag, then make the text un-bolded
            text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
        else:
            # If the selected text does not have a bold tag, then make the text bolded
            font_style = font.Font(text, text.cget("font"))
            font_style.configure(weight="bold")
            text.tag_add("bold_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
            text.tag_configure("bold_text_" + str(tag_sequence), font=font_style)
            tag_sequence += 1


# Make the highlighted text italized
def italic_text():
    # We need make the tag_sequence as global, so any change to tag_sequence will be visible from other methods
    global tag_sequence
    # Check if there's any selected text. If no text is selected, no need for further action
    if text.tag_ranges("sel"):
        # Get a list of existing tag for the selected text
        tags = text.tag_names(SEL_FIRST)
        tag_found = 0
        # Check if the selected text has a italic tag
        for tag_name in tags:
            if tag_name.startswith("italic_text_"):
                tag_found = 1
                current_tag_name = tag_name
        if tag_found == 1:
            # If the selected text already has a italic tag, then make the text un-italized
            text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
        else:
            # If the selected text does not have a italic tag, then make the text italized
            font_style = font.Font(text, text.cget("font"))
            font_style.configure(slant="italic")
            text.tag_add("italic_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
            text.tag_configure("italic_text_" + str(tag_sequence), font=font_style)
            tag_sequence += 1


# Add underline to the highlighted text
def underline_text():
    # We need make the tag_sequence as global, so any change to tag_sequence will be visible from other methods
    global tag_sequence
    # Check if there's any selected text. If no text is selected, no need for further action
    if text.tag_ranges("sel"):
        # Get a list of existing tag for the selected text
        tags = text.tag_names(SEL_FIRST)
        tag_found = 0
        # Check if the selected text has a underline tag
        for tag_name in tags:
            if tag_name.startswith("underline_text_"):
                tag_found = 1
        if tag_found == 1:
            # If the selected text already has a underline tag, then remove the underline
            text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
        else:
            # If the selected text does not have a underline tag, then add the underline
            font_style = font.Font(text, text.cget("font"))
            font_style.configure(underline=1)
            text.tag_add("underline_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
            text.tag_configure("underline_text_" + str(tag_sequence), font=font_style)
            tag_sequence += 1


# Change the font type of the selected text
def change_text_type(event):
    # We need make the tag_sequence as global, so any change to tag_sequence will be visible from other methods
    global tag_sequence
    # Check if there's any selected text. If no text is selected, no need for further action
    if text.tag_ranges("sel"):
        # Get a list of existing tag for the selected text
        tags = text.tag_names(SEL_FIRST)
        tag_found = 0
        # Check ig the selected text has a font type tag
        for tag_name in tags:
            if tag_name.startswith("font_type_text_"):
                tag_found = 1
        if tag_found == 1:
            # If the selected text already has a font type tag, then remove the font type
            text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
        else:
            # If the selected text does not have a font type tag, then add the font type
            font_style = font.Font(text, text.cget("font"))
            font_style.configure(family=font_type.get())
            text.tag_add("font_type_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
            text.tag_configure("font_type_text_" + str(tag_sequence), font=font_style)
            tag_sequence += 1


# Change the font size of the selected text
def change_text_size(event):
    # We need make the tag_sequence as global, so any change to tag_sequence will be visible from other methods
    global tag_sequence
    # Check if there's any selected text. If no text is selected, no need for further action
    if text.tag_ranges("sel"):
        # Get a list of existing tag for the selected text
        tags = text.tag_names(SEL_FIRST)
        tag_found = 0
        # Check id the selected text has a font size tag
        for tag_name in tags:
            if tag_name.startswith("font_size_text_"):
                tag_found = 1
        if tag_found == 1:
            # If the selected text already has a font size tag, then remove the font size
            text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
        else:
            # If the selected text does not have a font size tag, then add the font size
            font_style = font.Font(text, text.cget("font"))
            font_style.configure(size=font_size.get())
            text.tag_add("font_size_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
            text.tag_configure("font_size_text_" + str(tag_sequence), font=font_style)
            tag_sequence += 1


# Change the colour of the selected text
def change_text_color():
    # We need make the tag_sequence as global, so any change to tag_sequence will be visible from other methods
    global tag_sequence
    # Open the color chooser dialog
    color = colorchooser.askcolor(initialcolor="red")
    color_name = color[1]
    # Check if there's any selected text. If no text is selected, no need for further action
    if text.tag_ranges("sel"):
        # Get a list of existing tag for the selected text
        tags = text.tag_names(SEL_FIRST)
        tag_found = 0
        # Check ig the selected text has a font size tag
        for tag_name in tags:
            if tag_name.startswith("font_color_text_"):
                tag_found = 1
        if tag_found == 1:
            # If the selected text already has a font color tag, then remove the font colour
            text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
        else:
            # If the selected text does not have a font color tag, then add the font colour
            text.tag_add("font_color_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
            text.tag_configure("font_color_text_" + str(tag_sequence), foreground=color_name)
            tag_sequence += 1


# Play the text user highlighted, otherwise, play all the text
def play_text():
    read_text = text.get(1.0, END)
    if text.tag_ranges('sel'):
        read_text = text.get(SEL_FIRST, SEL_LAST)
    engine.setProperty("rate", voice_speed.get())
    engine.setProperty('voice', voices[voice_type_combo.get()])
    engine.say(read_text)
    engine.runAndWait()
    engine.stop()


# Create tool bar one
toolbar_one = Frame(root, pady=2)
toolbar_one.pack(side=TOP, fill="x")
# Arrange tool bar one
# Open
open_image = PhotoImage(file="icons/Open.png")
open_button = Button(text="Open", image=open_image, compound=LEFT, width=60, height=24, command=open_file)
open_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
# Save
save_image = PhotoImage(file="icons/Save.png")
save_button = Button(text="Save", image=save_image, compound=LEFT, width=60, height=24, command=save_file)
save_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
# Copy
copy_image = PhotoImage(file="icons/Copy.png")
copy_button = Button(text="Copy", image=copy_image, compound=LEFT, width=60, height=24, command=copy_text)
copy_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
# Cut
cut_image = PhotoImage(file="icons/Cut.png")
cut_button = Button(text="Cut", image=cut_image, compound=LEFT, width=60, height=24, command=cut_text)
cut_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
# Paste
paste_image = PhotoImage(file="icons/Paste.png")
paste_button = Button(text="Paste", image=paste_image, compound=LEFT, width=60, height=24, command=paste_text)
paste_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
# Undo
undo_image = PhotoImage(file="icons/Undo.png")
undo_button = Button(text="Undo", image=undo_image, compound=LEFT, width=60, height=24, command=undo_text)
undo_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
# Redo
redo_image = PhotoImage(file="icons/Redo.png")
redo_button = Button(text="Redo", image=redo_image, compound=LEFT, width=60, height=24, command=redo_text)
redo_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
# Find
find_image = PhotoImage(file="icons/Find.png")
find_button = Button(text="Find", image=find_image, compound=LEFT, width=60, height=24, command=find_text)
find_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
# Help
help_image = PhotoImage(file="icons/Help.png")
help_button = Button(text="Help", image=help_image, compound=LEFT, width=60, height=24, command=help_popup)
help_button.pack(in_=toolbar_one, side=RIGHT, padx=2, pady=2)

# Create tool bar two
toolbar_two = Frame(root, pady=2)
toolbar_two.pack(side=TOP, fill="x")
# Arrange tool bar two
# Font Type
font_type = StringVar()
font_type_combo = ttk.Combobox(toolbar_two, textvariable=font_type, values=sorted(font.families()), font="Arial 10")
font_type_combo.bind('<<ComboboxSelected>>', change_text_type)
font_type_combo.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)
selected_index = sorted(font.families()).index("Arial")
font_type_combo.current(selected_index)
# Font Size
font_size = StringVar()
font_size_combo = ttk.Combobox(toolbar_two, width=4, font="Arial 10", textvariable=font_size,
                               values=("10", "12", "14", "16", "18", "20", "22", "24", "26", "28"))
font_size_combo.bind('<<ComboboxSelected>>', change_text_size)
font_size_combo.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)
font_size_combo.current(1)
# Bold
bold_image = PhotoImage(file="icons/Bold.png")
bold_button = Button(text="Bold", image=bold_image, compound=LEFT, width=60, height=24, command=bold_text)
bold_button.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)
# Italic
italic_image = PhotoImage(file="icons/Italic.png")
italic_button = Button(text="Italic", image=italic_image, compound=LEFT, width=60, height=24, command=italic_text)
italic_button.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)
# Underline
underline_image = PhotoImage(file="icons/Underline.png")
underline_button = Button(text="Underline", image=underline_image, compound=LEFT, width=75, height=24, command=underline_text)
underline_button.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)
# Color Picker
color_picker_image = PhotoImage(file="icons/ColorPicker.png")
color_picker_button = Button(text="Color", image=color_picker_image, compound=LEFT, width=60, height=24, command=change_text_color)
color_picker_button.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)

# Create tool bar two
toolbar_three = Frame(root, pady=2)
toolbar_three.pack(side=TOP, fill="x")
# Arrange tool bar one
# Voice Type
voice_type_combo = ttk.Combobox(toolbar_three, values=sorted(voices.keys()), font="Arial 10", width="45")
voice_type_combo.pack(in_=toolbar_three, side=LEFT, padx=2, pady=2)
voice_type_combo.current(0)
# Speed
voice_speed_label = Label(toolbar_three, text="Speed", font="Arial 10")
voice_speed_label.pack(in_=toolbar_three, side=LEFT, padx=2, pady=2)
voice_speed = ttk.Scale(toolbar_three, orient=HORIZONTAL, length=110, from_=100, to=200)
voice_speed.set(150)
voice_speed.pack(in_=toolbar_three, side=LEFT, padx=2, pady=2)
# Read Out
play_image = PhotoImage(file="icons/Sound.png")
play_button = Button(text="Play", image=play_image, compound=LEFT, width=60, height=24, command=play_text)
play_button.pack(in_=toolbar_three, side=LEFT, padx=2, pady=2)

# Create the textarea (undo=True to activate the setting otherwise edit_undo() and edit_redo() will not work)
text_area = Frame(root, borderwidth=4)
text_area.pack(side=TOP, fill="x")
# Text input (undo=True to activate the setting otherwise edit_undo() and edit_redo() will not work)
text = scrolledtext.ScrolledText(wrap="word", font=("Arial", 10), background="WHITE", height=35, undo=True)
text.pack(in_=text_area, side=LEFT, fill=BOTH, expand=True)

root.mainloop()


