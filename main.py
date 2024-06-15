import tkinter as tk
from PIL import Image, ImageTk  # Ensure you have the Pillow library installed
import databaseAccessor
import combine  # Ensure you have combine.py in your project
import fetchAndPopulateDB

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Screen Application with Text Input")
        self.geometry("800x480")

        self.card1 = None
        self.card2 = None
        
        # Create a StringVar to hold the input text
        self.input_text = tk.StringVar()
        self.input_text2 = tk.StringVar()

        # Initialize frames
        self.frames = {}
        for F in (HomePage, CombinePage, ClonePage, ComputerPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            
            # Place all frames in the same location, but only the one that should be visible
            # is on the top of the stacking order
            frame.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)  # Ensure the main window expands properly
        self.rowconfigure(0, weight=1)
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
    
    def configure_grid(self, frame):
        '''Configure the grid layout for a given frame'''
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)
        frame.columnconfigure(2, weight=3)
        frame.columnconfigure(3, weight=3)
        frame.columnconfigure(4, weight=3)
        frame.columnconfigure(5, weight=3)
        frame.columnconfigure(6, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(4, weight=1)
        frame.rowconfigure(5, weight=1)
        frame.rowconfigure(6, weight=1)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        controller.configure_grid(self)

        label = tk.Label(self, text="This is the Home page")
        label.grid(row=0, column=2, columnspan=3, pady=10, padx=10)
        
        computerButton = tk.Button(self, text="Computer",
                           command=lambda: controller.show_frame("ComputerPage"))
        computerButton.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        ringCrafterButton = tk.Button(self, text="Ring Crafter",
                           command=lambda: controller.show_frame("RingPage"))
        ringCrafterButton.grid(row=2, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        makeDBButton = tk.Button(self, text="Fetch Scryfall Data for DB",
                           command=lambda: self.fetchAndPopulateDB())
        makeDBButton.grid(row=3, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.display_label1 = tk.Label(self, text="")
        self.display_label1.grid(row=3, column=3, pady=10, padx=10)

        fetchImagesButton = tk.Button(self, text="Fetch Images for Cards",
                           command=lambda: self.fetchCardImages())
        fetchImagesButton.grid(row=4, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.display_label2 = tk.Label(self, text="")
        self.display_label2.grid(row=4, column=3, pady=10, padx=10)
        

    def fetchAndPopulateDB(self):
        if fetchAndPopulateDB.main():
            self.display_label1.config(text="✓", fg="green")            
        else:
            self.display_label1.config(text="✗", fg="red")

    def fetchCardImages(self):
        file_path = 'mtg_rogue.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            card_names = [line.strip() for line in file.readlines()]

        if databaseAccessor.download_card_images(card_names):
            self.display_label2.config(text="✓", fg="green")            
        else:
            self.display_label2.config(text="✗", fg="red")

class ComputerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        controller.configure_grid(self)

        label = tk.Label(self, text="Computer")
        label.grid(row=0, column=2, columnspan=3, pady=10, padx=10)

        combineButton = tk.Button(self, text="Combine",
                           command=lambda: controller.show_frame("CombinePage"))
        combineButton.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        upgradeButton = tk.Button(self, text="Upgrade",
                           command=lambda: controller.show_frame("UpgradePage"))
        upgradeButton.grid(row=2, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        cloneButton = tk.Button(self, text="Clone",
                           command=lambda: controller.show_frame("ClonePage"))
        cloneButton.grid(row=3, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        homeButton = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("HomePage"))
        homeButton.grid(row=0, column=6, pady=10, padx=10, sticky="nsew")

class ClonePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        controller.configure_grid(self)
        
        label = tk.Label(self, text="This is the clone page")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        
        # Create a button to go to Start Page
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("HomePage"))
        button.grid(row=1, column=0, pady=10, padx=10)

        self.entry1 = tk.Entry(self, textvariable=controller.input_text)
        self.entry1.grid(row=2, column=0, pady=10, padx=10)

        self.display_label1 = tk.Label(self, text="")
        self.display_label1.grid(row=3, column=0, pady=10, padx=10)

        button1 = tk.Button(self, text="Find Card",
                            command=lambda: self.getCard(controller.input_text.get()))
        button1.grid(row=4, column=0, pady=10, padx=10)

        self.image_label = tk.Label(self)
        self.image_label.grid(row=0, column=1, rowspan=6, pady=10, padx=10)

    def getCard(self, cardName):
        card = databaseAccessor.fetch_card_by_name(cardName)
        if card:
            # Display a green checkmark if card is found
            self.display_label1.config(text="✓", fg="green")
            self.controller.card1 = card
            image_path = f'images/{card["mainCard"][0]}.jpg'
            self.display_card_image(image_path)
            
        else:
            # Display a red cross if card is not found
            self.display_label1.config(text="✗", fg="red")
            self.controller.card1 = None
        print(card)

    def display_card_image(self, image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((250, 350))  # Resize image as needed
            self.card_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.card_image)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_label.config(image='') 


class CombinePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        controller.configure_grid(self)

        label = tk.Label(self, text="This is the combine page")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        
        # Create a button to go back to Start Page
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("HomePage"))
        button.grid(row=1, column=0, pady=10, padx=10)

        # Create an Entry widget for text input
        self.entry1 = tk.Entry(self, textvariable=controller.input_text)
        self.entry1.grid(row=2, column=0, pady=10, padx=10)

        # Placeholder for display label
        self.display_label1 = tk.Label(self, text="")
        self.display_label1.grid(row=3, column=0, pady=10, padx=10)

        button1 = tk.Button(self, text="Find Card",
                            command=lambda: self.getCard(controller.input_text.get()))
        button1.grid(row=4, column=0, pady=10, padx=10)

        self.entry2 = tk.Entry(self, textvariable=controller.input_text2)
        self.entry2.grid(row=5, column=0, pady=10, padx=10)

        # Placeholder for display label
        self.display_label2 = tk.Label(self, text="")
        self.display_label2.grid(row=6, column=0, pady=10, padx=10)

        button2 = tk.Button(self, text="Find Card",
                            command=lambda: self.getCard2(controller.input_text2.get()))
        button2.grid(row=7, column=0, pady=10, padx=10)

        # Combine button (initially disabled)
        self.combine_button = tk.Button(self, text="Combine", state=tk.DISABLED,
                                        command=self.combine_cards)
        self.combine_button.grid(row=8, column=0, pady=10, padx=10)

    def getCard(self, cardName):
        card = databaseAccessor.fetch_card_by_name(cardName)
        if card:
            # Display a green checkmark if card is found
            self.display_label1.config(text="✓", fg="green")
            self.controller.card1 = card
        else:
            # Display a red cross if card is not found
            self.display_label1.config(text="✗", fg="red")
            self.controller.card1 = None
        self.update_combine_button_state()
        print(card)

    def getCard2(self, cardName):
        card = databaseAccessor.fetch_card_by_name(cardName)
        if card:
            # Display a green checkmark if card is found
            self.display_label2.config(text="✓", fg="green")
            self.controller.card2 = card
        else:
            # Display a red cross if card is not found
            self.display_label2.config(text="✗", fg="red")
            self.controller.card2 = None
        self.update_combine_button_state()
        print(card)

    def update_combine_button_state(self):
        # Enable the combine button only if both cards are found
        if self.controller.card1 and self.controller.card2:
            self.combine_button.config(state=tk.NORMAL)
        else:
            self.combine_button.config(state=tk.DISABLED)

    def combine_cards(self):
        card1 = self.controller.card1
        card2 = self.controller.card2
        combine.combine(card1, card2)  # Call the combine method from combine.py
        print("Cards combined")

if __name__ == "__main__":
    app = App()
    app.mainloop()
