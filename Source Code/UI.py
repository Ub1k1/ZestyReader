from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
from ButtonFunction import *
from FileManager import *

class UI:
    # Constructor
    def __init__(self):
        self.buttonFunctions = ButtonFunction
        self.fileManager = FileManager

    def run(self):
        # Create the application window.
        root = Tk()
        root.title("Zesty - A Visual and Audio Tool")
        # The window has a width of 800 pixels and a height of 700 pixels
        # The initial position from the top left corner is 200 pixels right and 50 pixels down
        root.geometry("800x700+200+50")
        # Make the application window resizable
        root.resizable(True, True)
        root.minsize(800, 700)

        # Create the text area (undo=True to activate the setting, otherwise edit_undo() and edit_redo() will not work)
        text_area = Frame(root, borderwidth=4)
        text_area.pack(side=TOP, fill="x")
        # Text input (undo=True to activate the setting, otherwise edit_undo() and edit_redo() will not work)
        text = scrolledtext.ScrolledText(wrap="word", font=("Arial", 10), background="WHITE", height=35, undo=True)
        text.pack(in_=text_area, side=LEFT, fill=BOTH, expand=True)

        # Create tool bar one
        toolbar_one = Frame(root, pady=2)
        toolbar_one.pack(side=TOP, fill="x")
        # Arrange tool bar one
        # Open
        open_image = PhotoImage(file="icons/Open.png")
        open_button = Button(text="Open", image=open_image, compound=LEFT, width=60, height=24, command=self.fileManager.open_file(text=text))
        open_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
        # Save
        save_image = PhotoImage(file="icons/Save.png")
        save_button = Button(text="Save", image=save_image, compound=LEFT, width=60, height=24, command=self.fileManager.save_file(text=text))
        save_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
        # Copy
        copy_image = PhotoImage(file="icons/Copy.png")
        copy_button = Button(text="Copy", image=copy_image, compound=LEFT, width=60, height=24, command=self.buttonFunctions.copy_text(text=text, root=root))
        copy_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
        # Cut
        cut_image = PhotoImage(file="icons/Cut.png")
        cut_button = Button(text="Cut", image=cut_image, compound=LEFT, width=60, height=24, command=self.buttonFunctions.cut_text(text=text, root=root))
        cut_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
        # Paste
        paste_image = PhotoImage(file="icons/Paste.png")
        paste_button = Button(text="Paste", image=paste_image, compound=LEFT, width=60, height=24, command=self.buttonFunctions.paste_text(text=text, root=root))
        paste_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
        # Undo
        undo_image = PhotoImage(file="icons/Undo.png")
        undo_button = Button(text="Undo", image=undo_image, compound=LEFT, width=60, height=24, command=self.buttonFunctions.undo_text(text=text))
        undo_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
        # Redo
        redo_image = PhotoImage(file="icons/Redo.png")
        redo_button = Button(text="Redo", image=redo_image, compound=LEFT, width=60, height=24, command=self.buttonFunctions.redo_text(text=text))
        redo_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
        # Find
        find_image = PhotoImage(file="icons/Find.png")
        find_button = Button(text="Find", image=find_image, compound=LEFT, width=60, height=24, command=self.buttonFunctions.find_text(text=text, root=root))
        find_button.pack(in_=toolbar_one, side=LEFT, padx=2, pady=2)
        # Help
        help_image = PhotoImage(file="icons/Help.png")
        help_button = Button(text="Help", image=help_image, compound=LEFT, width=60, height=24, command=self.buttonFunctions.help_popup(root=root))
        help_button.pack(in_=toolbar_one, side=RIGHT, padx=2, pady=2)

        # Create tool bar two
        toolbar_two = Frame(root, pady=2)
        toolbar_two.pack(side=TOP, fill="x")
        # Arrange tool bar two
        # Font Type
        font_type = StringVar()
        font_type_combo = ttk.Combobox(toolbar_two, textvariable=font_type, values=sorted(font.families()), font="Arial 10")
        font_type_combo.bind('<<ComboboxSelected>>', self.buttonFunctions.change_text_type(text=text, font_type=font_type))
        font_type_combo.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)
        selected_index = sorted(font.families()).index("Arial")
        font_type_combo.current(selected_index)
        # Font Size
        font_size = StringVar()
        font_size_combo = ttk.Combobox(toolbar_two, width=4, font="Arial 10", textvariable=font_size,
                                       values=("14", "16", "18", "20", "22", "24", "26", "28", "30", "32", "40"))
        font_size_combo.bind('<<ComboboxSelected>>', self.buttonFunctions.change_text_size(text=text, font_size=font_size))
        font_size_combo.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)
        font_size_combo.current(1)
        # Bold
        bold_image = PhotoImage(file="icons/Bold.png")
        bold_button = Button(text="Bold", image=bold_image, compound=LEFT, width=60, height=24, command=self.buttonFunctions.bold_text(text=text))
        bold_button.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)
        # Italic
        italic_image = PhotoImage(file="icons/Italic.png")
        italic_button = Button(text="Italic", image=italic_image, compound=LEFT, width=60, height=24, command=self.buttonFunctions.italic_text(text=text))
        italic_button.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)
        # Underline
        underline_image = PhotoImage(file="icons/Underline.png")
        underline_button = Button(text="Underline", image=underline_image, compound=LEFT, width=75, height=24, command=self.buttonFunctions.underline_text(text=text))
        underline_button.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)
        # Color Picker
        color_picker_image = PhotoImage(file="icons/ColorPicker.png")
        color_picker_button = Button(text="Color", image=color_picker_image, compound=LEFT, width=60, height=24, command=self.buttonFunctions.change_text_color(text=text))
        color_picker_button.pack(in_=toolbar_two, side=LEFT, padx=2, pady=2)

        # Create tool bar two
        toolbar_three = Frame(root, pady=2)
        toolbar_three.pack(side=TOP, fill="x")
        # Arrange tool bar one
        # Voice Type
        voice_type_combo = ttk.Combobox(toolbar_three, values=sorted(self.buttonFunctions.voices.keys()), font="Arial 10", width="45")
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
        play_button = Button(text="Play", image=play_image, compound=LEFT, width=60, height=24, command=self.buttonFunctions.play_text(text=text, button=play_button))
        play_button.pack(in_=toolbar_three, side=LEFT, padx=2, pady=2)
        pause_image = PhotoImage(file="icons/Pause.png")
        # Stop Reading
        stop_image = PhotoImage(file="icons/Stop/png")
        stop_button = Button(text="Stop", image=stop_image, compound=LEFT, width=60, height=24, command=self.buttonFunctions.stop_text(text=text))
        stop_button.pack(in_=toolbar_three, side=LEFT, padx=2, pady=2)

        root.mainloop()
