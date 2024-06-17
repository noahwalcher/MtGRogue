import tkinter as tk
from PIL import Image, ImageTk  # Ensure you have the Pillow library installed
import databaseAccessor
import alterCards  # Ensure you have combine.py in your project
import fetchAndPopulateDB
import randomEffectLists

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
        for F in (HomePage, CombinePage, ClonePage, ComputerPage, RingPage, UpgradePage, CompanionPage):
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
        frame = self.frames[page_name]
        self.input_text.set("")
        self.input_text2.set("")
        self.card1 = None
        self.card2 = None
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")
        
    
    def configure_grid(self, frame):
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

        companionButton = tk.Button(self, text="Companion",
                           command=lambda: controller.show_frame("CompanionPage"))
        companionButton.grid(row=3, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        makeDBButton = tk.Button(self, text="Fetch Scryfall Data for DB",
                           command=lambda: self.fetchAndPopulateDB())
        makeDBButton.grid(row=4, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.display_label1 = tk.Label(self, text="")
        self.display_label1.grid(row=4, column=3, pady=10, padx=10)

        fetchImagesButton = tk.Button(self, text="Fetch Images for Cards",
                           command=lambda: self.fetchCardImages())
        fetchImagesButton.grid(row=5, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.display_label2 = tk.Label(self, text="")
        self.display_label2.grid(row=5, column=3, pady=10, padx=10)
        

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
        self.bind("<<ShowFrame>>", self.onShow)
        
        label = tk.Label(self, text="Clone Card")
        label.grid(row=0, column=2, columnspan=3, pady=10, padx=10)
        
        homeButton = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("ComputerPage"))
        homeButton.grid(row=0, column=6, pady=10, padx=10, sticky="nsew")

        cardLabel = tk.Label(self, text="Card 1")
        cardLabel.grid(row=1, column=1, columnspan=2, pady=10, padx=10)

        cameraButton = tk.Button(self, text="Take Picture",
                           command=lambda: self.takePicture())
        cameraButton.grid(row=2, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.entry1 = tk.Entry(self, textvariable=controller.input_text)
        self.entry1.grid(row=3, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        manualEntryButton = tk.Button(self, text="Enter",
                            command=lambda: self.getCard(controller.input_text.get()))
        manualEntryButton.grid(row=3, column=3, pady=10, padx=10, sticky="nsew")

        self.display_label1 = tk.Label(self, text="")
        self.display_label1.grid(row=4, column=1, columnspan=2, pady=10, padx=10)

        self.submitButton = tk.Button(self, text="Clone", state=tk.DISABLED,
                           command=lambda: self.printCard())
        self.submitButton.grid(row=5, column=3, pady=10, padx=10, sticky="nsew")
    
    def onShow(self, event):
        self.display_label1.config(text="")
        
    def takePicture():
        print()

    def printCard():
        print()

    def getCard(self, cardName):
        card = databaseAccessor.fetch_card_by_name(cardName)
        if card:
            self.display_label1.config(text=f"{card["mainCard"][10]}", fg="green")
            self.controller.card1 = card
            image_path = f'images/{card["mainCard"][0]}.jpg'
            self.submitButton.config(state=tk.NORMAL)

        else:
            self.display_label1.config(text=f"{cardName} not found", fg="red")
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
        self.bind("<<ShowFrame>>", self.onShow)


        label = tk.Label(self, text="Combine Cards")
        label.grid(row=0, column=2, columnspan=3, pady=10, padx=10)
        
        homeButton = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("ComputerPage"))
        homeButton.grid(row=0, column=6, pady=10, padx=10, sticky="nsew")

        cardLabel = tk.Label(self, text="Card 1")
        cardLabel.grid(row=1, column=1, columnspan=2, pady=10, padx=10)

        cameraButton = tk.Button(self, text="Take Picture",
                           command=lambda: self.takePicture())
        cameraButton.grid(row=2, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.entry1 = tk.Entry(self, textvariable=controller.input_text)
        self.entry1.grid(row=3, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        manualEntryButton = tk.Button(self, text="Enter",
                            command=lambda: self.getCard(controller.input_text.get()))
        manualEntryButton.grid(row=3, column=3, pady=10, padx=10, sticky="nsew")

        self.display_label1 = tk.Label(self, text="")
        self.display_label1.grid(row=4, column=1, columnspan=2, pady=10, padx=10)

        cardLabel2 = tk.Label(self, text="Card 2")
        cardLabel2.grid(row=1, column=4, columnspan=2, pady=10, padx=10)

        cameraButton2 = tk.Button(self, text="Take Picture",
                           command=lambda: self.takePicture())
        cameraButton2.grid(row=2, column=4, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.entry2 = tk.Entry(self, textvariable=controller.input_text2)
        self.entry2.grid(row=3, column=4, columnspan=2, pady=10, padx=10, sticky="nsew")

        manualEntryButton2 = tk.Button(self, text="Enter",
                            command=lambda: self.getCard2(controller.input_text2.get()))
        manualEntryButton2.grid(row=3, column=6, pady=10, padx=10, sticky="nsew")

        self.display_label2 = tk.Label(self, text="")
        self.display_label2.grid(row=4, column=4, columnspan=2, pady=10, padx=10)

        self.submitButton = tk.Button(self, text="Combine", state=tk.DISABLED,
                           command=lambda: self.combine_cards())
        self.submitButton.grid(row=5, column=3, pady=10, padx=10, sticky="nsew")

    def onShow(self, event):
        self.display_label1.config(text="")
        self.display_label2.config(text="")

    def takePicture():
        #TODO
        print()

    def getCard(self, cardName):
        card = databaseAccessor.fetch_card_by_name(cardName)
        if card:
            self.display_label1.config(text=f"{card["mainCard"][10]}", fg="green")
            self.controller.card1 = card
        else:
            self.display_label1.config(text=f"{cardName} not found", fg="red")
            self.controller.card1 = None
        self.update_combine_button_state()
        print(card)

    def getCard2(self, cardName):
        card = databaseAccessor.fetch_card_by_name(cardName)
        if card:
            self.display_label2.config(text=f"{card["mainCard"][10]}", fg="green")
            self.controller.card2 = card
        else:
            self.display_label2.config(text=f"{cardName} not found", fg="red")
            self.controller.card2 = None
        self.update_combine_button_state()
        print(card)

    def update_combine_button_state(self):
        # Enable the combine button only if both cards are found
        if self.controller.card1 and self.controller.card2:
            self.submitButton.config(state=tk.NORMAL)
        else:
            self.submitButton.config(state=tk.DISABLED)

    def combine_cards(self):
        card1 = self.controller.card1
        card2 = self.controller.card2
        cardImages = alterCards.combine(card1, card2)
        if cardImages == "Invalid":
            self.controller.card1 = None
            self.controller.card2 = None
            self.display_label1.config(text="This combination of cards is not possible.", fg="red")
            self.display_label2.config(text="This combination of cards is not possible.", fg="red")
            self.update_combine_button_state()
        else:
            #TODO replace .save with print method
            cardImages[0].save(f"1.png")
            if len(cardImages) == 2:
                cardImages[1].save(f"2.png")

            print("Cards combined")

class CompanionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        controller.configure_grid(self)
        self.bind("<<ShowFrame>>", self.onShow)
        self.companions = ["","",""]
        self.currentCompanionIndex = 0

        label = tk.Label(self, text="Make Companion")
        label.grid(row=0, column=2, columnspan=3, pady=10, padx=10)

        homeButton = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("HomePage"))
        homeButton.grid(row=0, column=6, pady=10, padx=10, sticky="nsew")

        cameraButton = tk.Button(self, text="Take Picture",
                           command=lambda: self.takePicture())
        cameraButton.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.entry1 = tk.Entry(self, textvariable=controller.input_text)
        self.entry1.grid(row=2, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        manualEntryButton = tk.Button(self, text="Enter",
                            command=lambda: self.getCard(controller.input_text.get()))
        manualEntryButton.grid(row=2, column=3, pady=10, padx=10, sticky="nsew")

        self.display_label1 = tk.Label(self, text="")
        self.display_label1.grid(row=3, column=1, columnspan=2, pady=10, padx=10)

        self.companionLabel = tk.Label(self, text=self.companions[self.currentCompanionIndex], font=('Arial', 16))
        self.companionLabel.grid(row=4, column=2, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.prev_button = tk.Button(self, text='←', command=self.prevCompanion)
        self.prev_button.grid(row=4, column=1, pady=10, padx=10, sticky="nsew")

        self.next_button = tk.Button(self, text='→', command=self.nextCompanion)
        self.next_button.grid(row=4, column=5, pady=10, padx=10, sticky="nsew")

        self.submitButton = tk.Button(self, text="Make Companion", state=tk.DISABLED,
                           command=lambda: self.makeCompanion())
        self.submitButton.grid(row=5, column=3, pady=10, padx=10, sticky="nsew")

    def onShow(self, event):
        self.display_label1.config(text="")
        self.currentCompanionIndex = 0
        self.companions = ["","",""]
        self.updateCompanionLabel()

    def makeCompanion(self):
        cardImages = alterCards.upgrade(self.controller.card1, self.companions[self.currentCompanionIndex])
        cardImages[0].save(f"1.png")


    def getCard(self, cardName):
        card = databaseAccessor.fetch_card_by_name(cardName)
        if card:
            self.display_label1.config(text=f"{card["mainCard"][10]}", fg="green")
            self.controller.card1 = card
            self.getCompanionType()
            self.updateSubmitButtonState()
        else:
            self.display_label1.config(text=f"{cardName} not found", fg="red")
            self.controller.card1 = None
            self.updateSubmitButtonState()
            self.companions = ["","",""]
            self.updateCompanionLabel()
        print(card)

    def updateSubmitButtonState(self):
        if self.controller.card1 and self.companions[self.currentCompanionIndex] != "":
            self.submitButton.config(state=tk.NORMAL)
        else:
            self.submitButton.config(state=tk.DISABLED)

    def takePicture():
        #TODO
        print()

    def getCompanionType(self):
        type = alterCards.getUpgradeType(self.controller.card1)
        if type == "Creature":
            self.companions = randomEffectLists.getRandomCompanion()
        else:
            self.companions = ['','','']
        self.updateCompanionLabel()

    def updateCompanionLabel(self):
        self.companionLabel.config(text=self.companions[self.currentCompanionIndex])

    def prevCompanion(self):
        self.currentCompanionIndex = (self.currentCompanionIndex - 1) % len(self.companions)
        self.updateCompanionLabel()

    def nextCompanion(self):
        self.currentCompanionIndex = (self.currentCompanionIndex + 1) % len(self.companions)
        self.updateCompanionLabel()

class UpgradePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        controller.configure_grid(self)
        self.bind("<<ShowFrame>>", self.onShow)
        self.upgrades = ["","",""]
        self.currentUpgradeIndex = 0

        label = tk.Label(self, text="Upgrade Card")
        label.grid(row=0, column=2, columnspan=3, pady=10, padx=10)

        homeButton = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("HomePage"))
        homeButton.grid(row=0, column=6, pady=10, padx=10, sticky="nsew")

        cameraButton = tk.Button(self, text="Take Picture",
                           command=lambda: self.takePicture())
        cameraButton.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.entry1 = tk.Entry(self, textvariable=controller.input_text)
        self.entry1.grid(row=2, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

        manualEntryButton = tk.Button(self, text="Enter",
                            command=lambda: self.getCard(controller.input_text.get()))
        manualEntryButton.grid(row=2, column=3, pady=10, padx=10, sticky="nsew")

        self.display_label1 = tk.Label(self, text="")
        self.display_label1.grid(row=3, column=1, columnspan=2, pady=10, padx=10)

        self.upgradeLabel = tk.Label(self, text=self.upgrades[self.currentUpgradeIndex], font=('Arial', 16))
        self.upgradeLabel.grid(row=4, column=2, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.prev_button = tk.Button(self, text='←', command=self.prevUpgrade)
        self.prev_button.grid(row=4, column=1, pady=10, padx=10, sticky="nsew")

        self.next_button = tk.Button(self, text='→', command=self.nextUpgrade)
        self.next_button.grid(row=4, column=5, pady=10, padx=10, sticky="nsew")

        self.submitButton = tk.Button(self, text="Upgrade", state=tk.DISABLED,
                           command=lambda: self.upgrade())
        self.submitButton.grid(row=5, column=3, pady=10, padx=10, sticky="nsew")

    def onShow(self, event):
        self.display_label1.config(text="")
        self.currentUpgradeIndex = 0
        self.upgrades = ["","",""]
        self.updateUpgradeLabel()

    def upgrade(self):
        cardImages = alterCards.upgrade(self.controller.card1, self.upgrades[self.currentUpgradeIndex])
        cardImages[0].save(f"1.png")
        if len(cardImages) == 2:
            cardImages[1].save(f"2.png")


    def getCard(self, cardName):
        card = databaseAccessor.fetch_card_by_name(cardName)
        if card:
            self.display_label1.config(text=f"{card["mainCard"][10]}", fg="green")
            self.controller.card1 = card
            self.getUpgradeType()
            self.updateSubmitButtonState()
        else:
            self.display_label1.config(text=f"{cardName} not found", fg="red")
            self.controller.card1 = None
            self.updateSubmitButtonState()
            self.upgrades = ["","",""]
            self.updateUpgradeLabel()
        print(card)

    def updateSubmitButtonState(self):
        if self.controller.card1 and self.upgrades[self.currentUpgradeIndex] != "":
            self.submitButton.config(state=tk.NORMAL)
        else:
            self.submitButton.config(state=tk.DISABLED)

    def takePicture():
        #TODO
        print()

    def getUpgradeType(self):
        type = alterCards.getUpgradeType(self.controller.card1)
        if type == "Creature":
            self.upgrades = randomEffectLists.getRandomCreatureUpgrades()
        if type == "Spell":
            self.upgrades = randomEffectLists.getRandomSpellUpgrades()
        if type == "Land":
            self.upgrades = randomEffectLists.getRandomLandUpgrades()
        if type == "ArtifactEnchantment":
            self.upgrades = randomEffectLists.getRandomArtifactEnchantmentUpgrades()
        if type == "Invalid":
            self.upgrades = ['','','']
        self.updateUpgradeLabel()

    def updateUpgradeLabel(self):
        self.upgradeLabel.config(text=self.upgrades[self.currentUpgradeIndex])

    def prevUpgrade(self):
        self.currentUpgradeIndex = (self.currentUpgradeIndex - 1) % len(self.upgrades)
        self.updateUpgradeLabel()

    def nextUpgrade(self):
        self.currentUpgradeIndex = (self.currentUpgradeIndex + 1) % len(self.upgrades)
        self.updateUpgradeLabel()


class RingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        controller.configure_grid(self)
        self.bind("<<ShowFrame>>", self.onShow)

        self.triggers = randomEffectLists.getRandomTriggers()
        self.effects = randomEffectLists.getRandomEffects()
        self.currentTriggerIndex = 0
        self.currentEffectIndex = 0
        homeButton = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("HomePage"))
        homeButton.grid(row=0, column=6, pady=10, padx=10, sticky="nsew")

        pageLabel = tk.Label(self, text="Ringcrafter")
        pageLabel.grid(row=0, column=3, pady=10, padx=10, sticky="nsew")

        self.triggerLabel = tk.Label(self, text=self.triggers[self.currentTriggerIndex], font=('Arial', 16))
        self.triggerLabel.grid(row=1, column=2, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.prev_button = tk.Button(self, text='←', command=self.prevTrigger)
        self.prev_button.grid(row=1, column=1, pady=10, padx=10, sticky="nsew")

        self.next_button = tk.Button(self, text='→', command=self.nextTrigger)
        self.next_button.grid(row=1, column=5, pady=10, padx=10, sticky="nsew")

        self.effectLabel = tk.Label(self, text=self.effects[self.currentEffectIndex], font=('Arial', 16))
        self.effectLabel.grid(row=2, column=2, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.prevEffectButton = tk.Button(self, text='←', command=self.prevEffect)
        self.prevEffectButton.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")

        self.nextEffectButton = tk.Button(self, text='→', command=self.nextEffect)
        self.nextEffectButton.grid(row=2, column=5, pady=10, padx=10, sticky="nsew")

        self.craftButton = tk.Button(self, text='Craft', command=self.craft)
        self.craftButton.grid(row=3, column=2, columnspan=3, pady=10, padx=10, sticky="nsew")

    def onShow(self, event):
        self.triggers = randomEffectLists.getRandomTriggers()
        self.effects = randomEffectLists.getRandomEffects()
        self.currentTriggerIndex = 0
        self.currentEffectIndex = 0
        self.updateEffectLabel()
        self.updateTriggerLabel()

    def updateTriggerLabel(self):
        self.triggerLabel.config(text=self.triggers[self.currentTriggerIndex])

    def prevTrigger(self):
        self.currentTriggerIndex = (self.currentTriggerIndex - 1) % len(self.triggers)
        self.updateTriggerLabel()

    def nextTrigger(self):
        self.currentTriggerIndex = (self.currentTriggerIndex + 1) % len(self.triggers)
        self.updateTriggerLabel()

    def updateEffectLabel(self):
        self.effectLabel.config(text=self.effects[self.currentEffectIndex])

    def prevEffect(self):
        self.currentEffectIndex = (self.currentEffectIndex - 1) % len(self.effects)
        self.updateEffectLabel()

    def nextEffect(self):
        self.currentEffectIndex = (self.currentEffectIndex + 1) % len(self.effects)
        self.updateEffectLabel()

    def craft(self):
        print()#TODO print out crafted ring

if __name__ == "__main__":
    app = App()
    app.mainloop()
