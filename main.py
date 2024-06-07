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

    def getCard(self, cardName):
        self.card1 = databaseAccessor.fetch_card_by_name(cardName)
        print(self.card1)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page")
        label.pack(pady=10, padx=10)
        

        
        # Create a button to go to Page One
        button = tk.Button(self, text="Go to Page One",
                           command=lambda: controller.show_frame("Combine"))
        button.pack()

class Combine(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="This is page one")
        label.pack(pady=10, padx=10)

        # Create an Entry widget for text input
        self.entry = tk.Entry(self, textvariable=controller.input_text)
        self.entry.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Find Card",
                           command=lambda: controller.getCard(controller.input_text.get()))
        button1.pack()
        
        # Create a label to display the input text
        self.display_label = tk.Label(self, textvariable=controller.input_text)
        self.display_label.pack(pady=10, padx=10)
        
        # Create a button to go back to Start Page
        button = tk.Button(self, text="Go to Start Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
