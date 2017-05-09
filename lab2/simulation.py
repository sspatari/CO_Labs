import tkinter as tk
import business as bs

class MyApp:
    def __init__(self, master):
        self.master = master
        frame = tk.Frame(self.master)
        frame.pack()

        self.myBusiness = bs.Business(1500)

        self.window_width = 600
        self.window_height = 500
        self.canvas  = tk.Canvas(frame, width = self.window_width, height = self.window_height)
        self.canvas.pack()

        self.createRectElements()
        self.createTextElements()
        self.createButtonElements(frame)

        self.master.bind("<space>", self.nextYearVisualisation)


    def createRectElements(self):
        self.rect1 = self.canvas.create_rectangle(0, 0, 0, 0, fill = "green")
        self.rect2 = self.canvas.create_rectangle(0, 0, 0, 0, fill = "yellow")
        self.rect3 = self.canvas.create_rectangle(0, 0, 0, 0, fill = "purple")

    def createTextElements(self):
        self.text1 = self.canvas.create_text(10, 10, anchor="nw", text="", font=("Helvetica",15))
        self.text2 = self.canvas.create_text(10, 30, anchor="nw", text="", font=("Helvetica",10))
        self.text3 = self.canvas.create_text(10, 45, anchor="nw", text="", font=("Helvetica",10))
        self.text4 = self.canvas.create_text(10, 60, anchor="nw", text="", font=("Helvetica",10))
        self.text5 = self.canvas.create_text(10, 75, anchor="nw", text="", font=("Helvetica",10))
        self.text6 = self.canvas.create_text(10, 90, anchor="nw", text="", font=("Helvetica",10))

    def createButtonElements(self, frame):
        self.button = tk.Button(frame, text="Case 1", command=self.caseOneVisualisation)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(frame, text="Case 2", command=self.caseTwoVisualisation)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(frame, text="Case 3", command=self.caseThreeVisualisation)
        self.button.pack(side = tk.LEFT)

    def caseOneVisualisation(self):
        self.myBusiness.caseOne()
        self.modifyText()
        self.modifyRect()

    def caseTwoVisualisation(self):
        self.myBusiness.caseTwo()
        self.modifyText()
        self.modifyRect()

    def caseThreeVisualisation(self):
        self.myBusiness.caseThree()
        self.modifyText()
        self.modifyRect()

    def modifyText(self):
        self.canvas.itemconfig(self.text1, text="year:" + str(self.myBusiness.currentYear))
        self.canvas.itemconfig(self.text2, text="forest:" + str(self.myBusiness.areaDict["forest"]))
        self.canvas.itemconfig(self.text3, text="potatoes:" + str(self.myBusiness.areaDict["potatoes"]))
        self.canvas.itemconfig(self.text4, text="grape:" + str(self.myBusiness.areaDict["grape"]))
        if(self.myBusiness.yearProfit):
            self.canvas.itemconfig(self.text5, text="yearProfit:" + str(self.myBusiness.yearProfit))
        else:
            self.canvas.itemconfig(self.text5, text="yearProfit: None")
        self.canvas.itemconfig(self.text6, text="availableMoney:" + str(self.myBusiness.availableMoney))

    def modifyRect(self):
        self.canvas.coords(self.rect1, 0, 0,
            (self.myBusiness.areaDict["forest"] / self.myBusiness.landSurface ) * self.window_width,
            self.window_height)
        self.canvas.coords(self.rect2, (self.myBusiness.areaDict["forest"] / self.myBusiness.landSurface ) * self.window_width,
            0,
            (self.myBusiness.areaDict["forest"] / self.myBusiness.landSurface ) * self.window_width +
                (self.myBusiness.areaDict["potatoes"] / self.myBusiness.landSurface ) * self.window_width,
            self.window_height)
        self.canvas.coords(self.rect3,
            (self.myBusiness.areaDict["forest"] / self.myBusiness.landSurface ) * self.window_width +
                (self.myBusiness.areaDict["potatoes"] / self.myBusiness.landSurface ) * self.window_width,
            0,
            (self.myBusiness.areaDict["forest"] / self.myBusiness.landSurface ) * self.window_width +
                (self.myBusiness.areaDict["potatoes"] / self.myBusiness.landSurface ) * self.window_width +
                (self.myBusiness.areaDict["grape"] / self.myBusiness.landSurface ) * self.window_width,
            self.window_height)

    def nextYearVisualisation(self, event):
        self.myBusiness.findSolution()
        self.modifyText()
        self.modifyRect()

if __name__ == "__main__":
    root = tk.Tk()
    myapp = MyApp(root)
    root.mainloop()
