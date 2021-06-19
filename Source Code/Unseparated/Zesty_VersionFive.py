from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from tkinter import colorchooser
import tkinter.scrolledtext as scrolledtext
import pyttsx3
import pygame

# Initialize pygame audio player
pygame.mixer.init()

# Initialize pyttsx3
engine = pyttsx3.init()
# Produce a available voice list
voices = {}
system_voices = engine.getProperty("voices")
for system_voice in system_voices:
    voices[system_voice.name] = system_voice.id

# Create the application window
root = Tk()
root.title("Zesty - A Visual and Audio Tool")
# The window has a width of 800 pixels and a height of 700 pixels
# Initial position from top left corner is 200 pixels right and 50 pixels down
root.geometry("800x700+200+50")
# Make the application window resizable
root.resizable(True, True)
root.minsize(800, 700)

# Tag sequence to mark the text properties
tag_sequence = 0
paused = False

def open_file():
    """Opens a file explorer window that asks the user to select an existing text file,
    and assigns it to the string variable text.
    """
    existing_file = filedialog.askopenfile(filetypes=[('Text File', '.txt'), ('Python File', '.py')])
    text.delete(1.0, END)
    text.insert(INSERT, existing_file.read())


def save_file():
    """Opens a file explorer window that allows the user to save the string variable text as a new txt
    file.
    """
    new_file_path = filedialog.asksaveasfilename(filetypes=[('Text File', '.txt'), ('Python File', '.py')], defaultextension=".txt")
    new_file_name = new_file_path
    write = open(new_file_name, mode='w')
    write.write(text.get(1.0, END))


def copy_text():
    """Copies the selected text to the clipboard.
    """
    root.clipboard_clear()
    text.clipboard_append(text.selection_get())


def cut_text():
    """Copies the selected text to the clipboard, then deletes the selected text from the string variable
    text.
    """
    root.clipboard_clear()
    text.clipboard_append(text.selection_get())
    text.delete(SEL_FIRST, SEL_LAST)


def paste_text():
    """Pastes the current clipboard text to the string variable text at the current cursor location.
    Then clears the clipboard.
    """
    text.insert(INSERT, root.clipboard_get())
    root.clipboard_clear()


def undo_text():
    """Undoes the last change to the text that wasn't an undo.
    """
    text.edit_undo()


def redo_text():
    """If the last change to the text was an undo, reverses the effect of that undo.
    """
    text.edit_redo()


def find_text():
    """Creates a popup window that allows the user to type in the passage they want to search for.
    """
    search_popup = Toplevel(root)
    search_popup.title('Word Search')
    search_popup.transient(root)
    search_popup.resizable(False, False)
    search_popup.geometry("+800+75")
    Label(search_popup, text="Enter a word: ").grid(row=0, column=0)
    search_input = Entry(search_popup, width=20)
    search_input.grid(row=0, column=1, padx=2)
    search_input.focus_set()
    Button(search_popup, text="Search", command=lambda: find_text_search(search_input.get())).grid(row=1, column=0, padx=2, pady=2, sticky="E")
    Button(search_popup, text="Close", command=lambda: find_text_close(search_popup)).grid(row=1, column=1, padx=2, pady=2, sticky="W")


def find_text_search(word):
    """Searches the entire text for a passage, and turns the text into purple for all occurrences of the
    passage. Not case sensitive.

    :param word: the passage to be searched for in the text, defaults to None
    :type word: string, optional
    """
    if len(word) == 0:
        return

    text.tag_remove("found_text", 1.0, END)
    text.tag_config("found_text", foreground="purple")
    index = 1.0
    while index:
        index = text.search(word, nocase=1, index=index, stopindex=END)
        if index:
            new_index = str(index) + "+" + str(len(word)) + "c"
            text.tag_add('found_text', index, new_index)
            index = new_index


def find_text_close(search_popup):
    """Removes the highlight and closes the search popup window.
    :param search_popup: the search popup window to be closed
    :type search_popup: Toplevel
    """
    text.tag_remove("found_text", 1.0, END)
    search_popup.destroy()


def help_popup():
    """Creates a popup window that explains how to use the application.
    """
    help_panel = Toplevel(root)
    help_panel.title('Hep')
    help_panel.transient(root)
    help_panel.resizable(False, False)
    help_panel.geometry("550x450+250+200")
    create_help_item(help_panel, 0, "Open:", "Open an existing text file and configure it to your liking!")
    create_help_item(help_panel, 1, "Save:", "Save the text to a new file")
    create_help_item(help_panel, 2, "Copy:", "Save the highlighted text to the clipboard")
    create_help_item(help_panel, 3, "Cut:", "Cut the highlighted text")
    create_help_item(help_panel, 4, "Paste:", "Paste the text you previously copied/cut to the current position")
    create_help_item(help_panel, 5, "Undo:", "Undo a text change")
    create_help_item(help_panel, 6, "Redo:", "Redo a text change")
    create_help_item(help_panel, 7, "Find:", "Find the word you entered within the text")
    create_help_item(help_panel, 8, "------", "")
    create_help_item(help_panel, 9, "Font:", "Change the font type and size for the highlighted text")
    create_help_item(help_panel, 10, "Bold:", "Make the highlighted text bold")
    create_help_item(help_panel, 11, "Italic:", "Italicize the highlighted text")
    create_help_item(help_panel, 12, "Underline:", "Underline the highlighted text")
    create_help_item(help_panel, 13, "Color:", "Change the color of the highlighted text")
    create_help_item(help_panel, 14, "------", "")
    create_help_item(help_panel, 15, "Select your preferred voice type, change the playback speed, and play it outloud using the play button")


# Create each help item by passing in the parent widget and row number, with the function name and description of the function
def create_help_item(parent_widget, row_number, function_name, function_description):
    """Create each help item by passing in the parent widget and row number,
    with the function name and description of the function.

    :param parent_widget: The popup window that the help item is to be created in
    :type parent_widget: Toplevel
    :param row_number: The row order of appearance of the help item in the help window
    :type row_number: int
    :param function_name: The name of the button whose function is being explained
    :type function_name: string
    :param function_description: The description of the button's function
    :type function_description: string
    """
    Label(parent_widget, text=function_name, font="Arial 12 bold").grid(row=row_number, column=0, padx=2, pady=2, sticky="W")
    Label(parent_widget, text=function_description, font="Arial 12").grid(row=row_number, column=1, padx=20, pady=2, sticky="W")


def bold_text():
    """If the selected text is not bold, then makes it bold. Otherwise, makes it unbold.
    """
    global tag_sequence
    if text.tag_ranges("sel"):
        tags = text.tag_names(SEL_FIRST)
        tag_found = 0
        for tag_name in tags:
            if tag_name.startswith("bold_text_"):
                tag_found = 1
        if tag_found == 1:
            text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
        else:
            font_style = font.Font(text, text.cget("font"))
            font_style.configure(weight="bold")
            text.tag_add("bold_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
            text.tag_configure("bold_text_" + str(tag_sequence), font=font_style)
            tag_sequence += 1


def italic_text():
    """If the selected text is not italicized, then makes it italicized. Otherwise, makes it unitalicized.
    """
    global tag_sequence
    if text.tag_ranges("sel"):
        tags = text.tag_names(SEL_FIRST)
        tag_found = 0
        for tag_name in tags:
            if tag_name.startswith("italic_text_"):
                tag_found = 1
                current_tag_name = tag_name
        if tag_found == 1:
            text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
        else:
            font_style = font.Font(text, text.cget("font"))
            font_style.configure(slant="italic")
            text.tag_add("italic_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
            text.tag_configure("italic_text_" + str(tag_sequence), font=font_style)
            tag_sequence += 1


def underline_text():
    """If the selected text is not underlined, then makes it underlined. Otherwise, makes it not underlined.
    """
    global tag_sequence
    if text.tag_ranges("sel"):
        tags = text.tag_names(SEL_FIRST)
        tag_found = 0
        for tag_name in tags:
            if tag_name.startswith("underline_text_"):
                tag_found = 1
        if tag_found == 1:
            text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
        else:
            font_style = font.Font(text, text.cget("font"))
            font_style.configure(underline=1)
            text.tag_add("underline_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
            text.tag_configure("underline_text_" + str(tag_sequence), font=font_style)
            tag_sequence += 1


def change_text_type(event):
    """Changes the font type of the selected text to a user-defined font face.
    """
    global tag_sequence
    if text.tag_ranges("sel"):
        tags = text.tag_names(SEL_FIRST)
        tag_found = 0
        for tag_name in tags:
            if tag_name.startswith("font_type_text_"):
                tag_found = 1
        if tag_found == 1:
            text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
        else:
            font_style = font.Font(text, text.cget("font"))
            font_style.configure(family=font_type.get())
            text.tag_add("font_type_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
            text.tag_configure("font_type_text_" + str(tag_sequence), font=font_style)
            tag_sequence += 1


def change_text_size(event):
    """Changes the font size of the selected text to a user-defined font size.
    """
    global tag_sequence
    if text.tag_ranges("sel"):
        tags = text.tag_names(SEL_FIRST)
        tag_found = 0
        for tag_name in tags:
            if tag_name.startswith("font_size_text_"):
                tag_found = 1
        if tag_found == 1:
            text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
        else:
            font_style = font.Font(text, text.cget("font"))
            font_style.configure(size=font_size.get())
            text.tag_add("font_size_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
            text.tag_configure("font_size_text_" + str(tag_sequence), font=font_style)
            tag_sequence += 1


def change_text_color():
    """Changes the font colour of the selected text to a user-defined font colour.
    """
    global tag_sequence
    color = colorchooser.askcolor(initialcolor="red")
    color_name = color[1]
    if text.tag_ranges("sel"):
        tags = text.tag_names(SEL_FIRST)
        tag_found = 0
        for tag_name in tags:
            if tag_name.startswith("font_color_text_"):
                tag_found = 1
        if tag_found == 1:
            text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
        else:
            text.tag_add("font_color_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
            text.tag_configure("font_color_text_" + str(tag_sequence), foreground=color_name)
            tag_sequence += 1


def play_text(play_button):
    """If no audio is in queue to be played, then starts playing the selected text. If no text is selected, plays the entire text. If audio is being played, pauses the audio
    and updates button image and text to match "Pause". If the audio is currently paused, resumes the audio and updates button image and text to match "Play".
    
    :param play_button: The play/pause button
    :type play_button: Button
    """
    global paused

    print('paused =', paused, ', button text =', play_button['text'], ', busy =', pygame.mixer.music.get_busy())
    if not paused and play_button['text'] == "Play" and not pygame.mixer.music.get_busy():
        outfile = "temp.wav"
        read_text = text.get(1.0, END)
        
        if text.tag_ranges('sel'):
            read_text = text.get(SEL_FIRST, SEL_LAST)
            
        engine.setProperty("rate", voice_speed.get())
        engine.setProperty('voice', voices[voice_type_combo.get()]) 
        engine.save_to_file(read_text, outfile)
        engine.runAndWait()
        pygame.mixer.music.load(outfile)
        pygame.mixer.music.play()

        play_button.configure(text="Pause")
    elif not paused and play_button['text'] == "Pause" and pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        paused = True
        play_button.configure(text="Play")
    else:
        pygame.mixer.music.unpause()
        paused = False
        play_button.configure(text="Pause")


def stop_text(play_button):
    """Stops the current audio and clears the audio queue.
    
    :param play_button: The play/pause button
    :type play_button: Button
    """
    pygame.mixer.music.stop()
    global paused
    paused = False
    play_button.configure(text="Play")


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
                               values=("12", "14", "16", "18", "20", "22", "24", "26", "28", "30"))
font_size_combo.bind('<<ComboboxSelected>>', change_text_size)
font_size_combo.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)
font_size_combo.current(0)
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
play_button = Button(text="Play", image=play_image, compound=LEFT, width=60, height=24, command=lambda: play_text(play_button))
play_button.pack(in_=toolbar_three, side=LEFT, padx=2, pady=2)
# Stop Reading
stop_image = PhotoImage(file="icons/Stop.png")
stop_button = Button(text="Stop", image=stop_image, compound=LEFT, width=60, height=24, command=lambda: stop_text(play_button))
stop_button.pack(in_=toolbar_three, side=LEFT, padx=2, pady=2)

# Create the textarea (undo=True to activate the setting otherwise edit_undo() and edit_redo() will not work)
text_area = Frame(root, borderwidth=4)
text_area.pack(side=TOP, fill="x")
# Text input (undo=True to activate the setting otherwise edit_undo() and edit_redo() will not work)
text = scrolledtext.ScrolledText(wrap="word", font=("Arial", 12), background="WHITE", height=35, undo=True)
text.pack(in_=text_area, side=LEFT, fill=BOTH, expand=True)

root.mainloop()
