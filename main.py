import tkinter as tk
import databaseAccessor

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
        for F in (StartPage, Combine):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            
            # Place all frames in the same location, but only the one that should be visible
            # is on the top of the stacking order
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()



class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page")
        label.pack(pady=10, padx=10)
        

        
        # Create a button to go to Page One
        button = tk.Button(self, text="Combine",
                           command=lambda: controller.show_frame("Combine"))
        button.pack()

class Combine(tk.Frame):
    def __init__(self, parent, controller):
        card1 = None
        card2 = None
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="This is page one")
        label.pack(pady=10, padx=10)

        # Create an Entry widget for text input
        self.entry1 = tk.Entry(self, textvariable=controller.input_text)
        self.entry1.pack(pady=10, padx=10)

        if card1:
            self.display_label = tk.Label(self, textvariable=card1['mainCard'][10])
            self.display_label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Find Card",
                           command=lambda: Combine.getCard(self, controller.input_text.get()))
        button1.pack()

        self.entry2 = tk.Entry(self, textvariable=controller.input_text2)
        self.entry2.pack(pady=10, padx=10)

        button2 = tk.Button(self, text="Find Card",
                           command=lambda: Combine.getCard2(self, controller.input_text2.get()))
        button2.pack()
        
        
        self.display_label2 = tk.Label(self, textvariable=controller.input_text2)
        self.display_label2.pack(pady=10, padx=10)
        
        # Create a button to go back to Start Page
        button = tk.Button(self, text="Go to Start Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


    def getCard(self, cardName):
        card1 = databaseAccessor.fetch_card_by_name(cardName)
        self.display_label = tk.Label(self, textvariable=card1['mainCard'][10])
        self.display_label.pack(pady=10, padx=10)
        print(card1)

    def getCard2(cardName):
        card2 = databaseAccessor.fetch_card_by_name(cardName)
        print(card2)

if __name__ == "__main__":
    app = App()
    app.mainloop()
