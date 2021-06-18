from tkinter import *
from tkinter import font, colorchooser
import pyttsx3
import pygame

class ButtonFunction:
    #Constructor
    def __init__(self):
        self.voices = {}

        # Play the text user highlighted, otherwise, play all the text
    def play_text(text):
        if not paused and not pygame.mixer.get_busy():
            # Initialize pyttsx3
            engine = pyttsx3.init()
            # Produce a available voice list
            system_voices = engine.getProperty("voices")
            for system_voice in system_voices:
            self.voices[system_voice.name] = system_voice.id
            #Initialize pygame
            pygame.mixer.init()
            
            outfile = "temp.wav"
            read_text = text.get(1.0, END)

            if text.tag_ranges('sel'):
                read_text = text.get(SEL_FIRST, SEL_LAST)

            engine.setProperty("rate", voice_speed.get())
            engine.setProperty('voice', voices[voice_type_combo.get()]) 
            engine.save_to_file(read_text, outfile)
            engine.runAndWait()

            pygame.mixer.music.load(outfile)

        elif paused:
            pygame.mixer.music.unpause()

        else:
            pygame.mixer.music.pause()
            
    def update_image(buttonText, buttonImage):
        if(buttonText = "Play"):
            buttonText.set("Pause")
            buttonImage.set("icons/Sound.png")
        else:
            buttonText.set("Play")
            buttonImage.set("icons/Pause.png")        

    def stop_text():
        pygame.mixer.music.stop()

    # Tag sequence to mark the text properties
    tag_sequence = 0

    # Mark the selected text for later
    def copy_text(self, text, root):
        # Clear the clipboard first
        root.clipboard_clear()
        # Append the selected text to the clipboard
        text.clipboard_append(text.selection_get())

    # Cut the selected text
    def cut_text(self, text, root):
        # Clear the clipboard first
        root.clipboard_clear()
        # Append the selected text to the clipboard
        text.clipboard_append(text.selection_get())
        # Delete the selected text
        text.delete(SEL_FIRST, SEL_LAST)


    # Paste the selected text
    def paste_text(self, text, root):
        # Paste the selected text at the cursor
        text.insert(INSERT, root.clipboard_get())
        root.clipboard_clear()

    # To undo the changes
    def undo_text(self, text):
        text.edit_undo()

    # To redo the changes
    def redo_text(self, text):
        text.edit_redo()


    # Search the text and highlight words
    def find_text(self, text, root):
        # Create a popup window for search functions
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
        # Action button to search or cancel
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
        # Create a popup window for the help function
        help_panel = Toplevel(root)
        help_panel.title('Hep')
        help_panel.transient(root)
        help_panel.resizable(False, False)
        # Initial position from top left corner is 250 pixels right and 200 pixels down
        help_panel.geometry("550x450+250+200")
        # Help explanation for the first toolbar
        self.create_help_item(help_panel, 0, "Open:", "Open an existing text file and configure it to your liking!")
        self.create_help_item(help_panel, 1, "Save:", "Save the text to a new file")
        self.create_help_item(help_panel, 2, "Copy:", "Save the highlighted text to the clipboard")
        self.create_help_item(help_panel, 3, "Cut:", "Cut the highlighted text")
        self.create_help_item(help_panel, 4, "Paste:", "Paste the text you previously copied/cut to the current position")
        self.create_help_item(help_panel, 5, "Undo:", "Undo a text change")
        self.create_help_item(help_panel, 6, "Redo:", "Redo a text change")
        self.create_help_item(help_panel, 7, "Find:", "Find the word you entered within the text")
        # Help explanation for the second toolbar
        self.create_help_item(help_panel, 8, "------", "")
        self.create_help_item(help_panel, 9, "Font:", "Change the font type and size for the highlighted text")
        self.create_help_item(help_panel, 10, "Bold:", "Make the highlighted text bold")
        self.create_help_item(help_panel, 11, "Italic:", "Italicize the highlighted text")
        self.create_help_item(help_panel, 12, "Underline:", "Underline the highlighted text")
        self.create_help_item(help_panel, 13, "Color:", "Change the color of the highlighted text")
        # Help explanation for the third toolbar
        self.create_help_item(help_panel, 14, "------", "")
        self.create_help_item(help_panel, 15, "Select your preferred voice type, change the playback speed, and play it outloud using the play button")


    # Create each help item by passing in the parent widget and row number, with the function name and description of the function
    def create_help_item(self, parent_widget, row_number, function_name, function_description):
        Label(parent_widget, text=function_name, font="Arial 18 bold").grid(row=row_number, column=0, padx=2, pady=2, sticky="W")
        Label(parent_widget, text=function_description, font="Arial 18").grid(row=row_number, column=1, padx=20, pady=2, sticky="W")


    # Bold the highlighted text
    def bold_text(self, text):
        # tag_sequence must be global, so any change to tag_sequence will be visible from other methods
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
        #Make the tag_sequence as global, so any change to tag_sequence will be visible from other methods
        global tag_sequence
        # Check if there's any selected text. If no text is selected, no need for further action
        if text.tag_ranges("sel"):
            # Get a list of existing tags for the selected text
            tags = text.tag_names(SEL_FIRST)
            tag_found = 0
            # Check if the selected text has a font type tag
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
        # Make the tag_sequence as global, so any change to tag_sequence will be visible from other methods
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


    # Change the color of the selected text
    def change_text_color(self, text):
        # Make the tag_sequence as global, so any change to tag_sequence will be visible from other methods
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
                # If the selected text already has a font color tag, then remove the font color
                text.tag_remove(tag_name, SEL_FIRST, SEL_LAST)
            else:
                # If the selected text does not have a font color tag, then add the font color
                text.tag_add("font_color_text_" + str(tag_sequence), SEL_FIRST, SEL_LAST)
                text.tag_configure("font_color_text_" + str(tag_sequence), foreground=color_name)
                tag_sequence += 1
