from tkinter import *
from tkinter import font, colorchooser
import pyttsx3

class ButtonFunction:
    #constructor
    def __init__(self):
        self.voices = {}

    # Play the text user highlighted, otherwise, play all the text
    def play_text(self, text, voice_speed, voice_type_combo):
        # Initialize pyttsx3
        engine = pyttsx3.init()
        # Produce a available voice list
        system_voices = engine.getProperty("voices")
        for system_voice in system_voices:
            self.voices[system_voice.name] = system_voice.id

        read_text = text.get(1.0, END)
        if text.tag_ranges('sel'):
            read_text = text.get(SEL_FIRST, SEL_LAST)
        engine.setProperty("rate", voice_speed.get())
        engine.setProperty('voice', self.voices[voice_type_combo.get()])
        engine.say(read_text)
        engine.runAndWait()
        engine.stop()

    # Tag sequence to mark the text properties
    tag_sequence = 0

    # Mark the selected text for later
    def copy_text(self, text, root):
        # Need clear the clipboard first
        root.clipboard_clear()
        # Append the selected text to the clipboard
        text.clipboard_append(text.selection_get())


    # Cut the selected text
    def cut_text(self, text, root):
        # Need clear the clipboard first
        root.clipboard_clear()
        # Append the selected text to the clipboard
        text.clipboard_append(text.selection_get())
        # Delete the selected text
        text.delete(SEL_FIRST, SEL_LAST)


    # Paste the selected text
    def paste_text(self, text, root):
        # Paste the selected text at the cursor
        text.insert(INSERT, root.clipboard_get())
        # Need to clear keyboard a
        # root.clipboard_clear()


    # To undo the change
    def undo_text(self, text):
        text.edit_undo()


    # To redo the change
    def redo_text(self, text):
        text.edit_redo()


    # Search the text and highlight words
    def find_text(self, text, root):
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
        Button(search_popup, text="Search", command=lambda: self.find_text_search(search_input.get())).grid(row=1, column=0, padx=2, pady=2, sticky="E")
        Button(search_popup, text="Close", command=lambda: self.find_text_close(search_popup)).grid(row=1, column=1, padx=2, pady=2, sticky="W")


    # Search the text from the beginning to the end. If the word found, highlight it in yellow
    def find_text_search(self, text, word):
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
    def find_text_close(self, text, search_popup):
        text.tag_remove("found_text", 1.0, END)
        search_popup.destroy()


    # Popup window for how to use the application
    def help_popup(self, root):
        # Create a popup window for help function, and the popup is transient (temporary) to the main window
        help_panel = Toplevel(root)
        help_panel.title('Hep')
        help_panel.transient(root)
        help_panel.resizable(False, False)
        # Initial position from top left corner is 250 pixel right and 200 pixel down
        help_panel.geometry("550x450+250+200")
        # Create each help items for the first toolbar
        self.create_help_item(help_panel, 0, "Open:", "Explanation")
        self.create_help_item(help_panel, 1, "Save:", "Explanation")
        self.create_help_item(help_panel, 2, "Copy:", "Explanation")
        self.create_help_item(help_panel, 3, "Cut:", "Explanation")
        self.create_help_item(help_panel, 4, "Paste:", "Explanation")
        self.create_help_item(help_panel, 5, "Undo:", "Explanation")
        self.create_help_item(help_panel, 6, "Redo:", "Explanation")
        self.create_help_item(help_panel, 7, "Find:", "Explanation")
        # Create each help items for the second toolbar
        self.create_help_item(help_panel, 8, "------", "")
        self.create_help_item(help_panel, 9, "Font:", "Explanation")
        self.create_help_item(help_panel, 10, "Bold:", "Explanation")
        self.create_help_item(help_panel, 11, "Italic:", "Explanation")
        self.create_help_item(help_panel, 12, "Underline:", "Explanation")
        self.create_help_item(help_panel, 13, "Color:", "Explanation")
        # Create each help items for the third toolbar
        self.create_help_item(help_panel, 14, "------", "")
        self.create_help_item(help_panel, 15, "Explanation")


    # Create each help item by passing in the parent widget and row number, with the function name and description of the function
    def create_help_item(self, parent_widget, row_number, function_name, function_description):
        Label(parent_widget, text=function_name, font="Arial 10 bold").grid(row=row_number, column=0, padx=2, pady=2, sticky="W")
        Label(parent_widget, text=function_description, font="Arial 10").grid(row=row_number, column=1, padx=20, pady=2, sticky="W")


    # Make the highlighted text bold
    def bold_text(self, text):
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
    def italic_text(self, text):
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
    def underline_text(self, text):
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
    def change_text_type(self, text, font_type, event):
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
    def change_text_size(self, text, font_size, event):
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
    def change_text_color(self, text):
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
