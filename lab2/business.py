import simplex as sm

class Business:
    landSurface           = 1.2   #sq. km
    __landTypes = ["forest", "potatoes", "grape"]

    __nonForestLandCost    = 200*10*12   #per sq. km per year
    __forestLandCost       = 100*10*12   #per sq. km per year
    __minForestSurface     = 0.5   #sq. km
    __forestRevenuePerSqKm = 20000 #Lei pre sq. km

    __amountPotatoesPerSqKm = 10*2  #tones * times farmed per year
    __costPotatoesSeeds     = 100*2 #Lei/sq. km * times farmed per year
    __costTractor           = 500*2 #Lei/sq. km * times farmed per year
    __pricePerTonPotatoes   = 2000  #Lei/per Ton

    __costGrapeSeed         = 800   #Lei/sq. km
    __amountGrapePerSqKm    = 20    #tones/sq. km
    __costWorkers           = 5000  #Lei/sq. km
    __winePerTonOfGrape     = 400   #Litres
    __priceLitreWine        = 6     #Lei

    def __init__(self, initialMoney):
        self.initialMoney = initialMoney
        self.availableMoney = initialMoney
        self.yearProfit = None
        self.currentYear = 0
        self.caseSpecifier = 0
        # self.yearlySurfaceList = []
        # self.yearlyExpectedProfitList = []
        self.costsBeforeSale_dict = {}
        self.profitPerSqKm_dict = {}

    def findSolution(self): #for one year or what should i do now :D
        # for first year example
        # t = Simplex([-8000,-14800,-18200])
        # t.add_constraint([0, 1200, 5800], 1500, "<=")
        # t.add_constraint([1, 1, 1], 1.2, "<=")
        # t.add_constraint([1, 0, 0], 0.5, ">=")
        if(self.caseSpecifier == 1 or (self.caseSpecifier == 2 and self.currentYear == 0)):
            t = sm.Tabel([-self.profitPerSqKm_dict["forest"],
                -self.profitPerSqKm_dict["potatoes"],
                -self.profitPerSqKm_dict["grape"]])
            t.add_constraint([0,
                self.costsBeforeSale_dict["potatoes"],
                self.costsBeforeSale_dict["grape"]],
                self.availableMoney, "<=")
            t.add_constraint([1, 1, 1], Business.landSurface, "<=")
            t.add_constraint([1, 0, 0], Business.__minForestSurface, ">=")
        elif(self.caseSpecifier == 2):
            t = sm.Tabel([-self.profitPerSqKm_dict["forest"],
                -self.profitPerSqKm_dict["potatoes"],
                -(self.profitPerSqKm_dict["grape"] + Business.__costGrapeSeed)]) # add back the grape seed cost from profit
            t.add_constraint([0,
                self.costsBeforeSale_dict["potatoes"],
                self.costsBeforeSale_dict["grape"] - Business.__costGrapeSeed],# substract back grape seed cost from cost before sale
                self.availableMoney, "<=")
            t.add_constraint([1, 1, 1], Business.landSurface, "<=")
            t.add_constraint([1, 0, 0], Business.__minForestSurface, ">=")
        elif(self.caseSpecifier == 3):
            if(self.currentYear == 0):
                t = sm.Tabel([-self.profitPerSqKm_dict["forest"],
                    -self.profitPerSqKm_dict["potatoes"],
                    -(self.profitPerSqKm_dict["grape"] + (Business.__costWorkers/2 - \
                        100*Business.__priceLitreWine))]) # add back the grape seed cost from profit
                t.add_constraint([0,
                    self.costsBeforeSale_dict["potatoes"],
                    self.costsBeforeSale_dict["grape"] - (Business.__costWorkers/2)],# substract back grape seed cost from cost before sale
                    self.availableMoney, "<=")
            else:
                t = sm.Tabel([-self.profitPerSqKm_dict["forest"],
                    -self.profitPerSqKm_dict["potatoes"],
                    -(self.profitPerSqKm_dict["grape"] + (Business.__costWorkers/2 - \
                        100*Business.__priceLitreWine) + Business.__costGrapeSeed)]) # add back the grape seed cost from profit
                t.add_constraint([0,
                    self.costsBeforeSale_dict["potatoes"],
                    self.costsBeforeSale_dict["grape"] - (Business.__costWorkers/2) - \
                        Business.__costGrapeSeed],# substract back grape seed cost from cost before sale
                    self.availableMoney, "<=")
            t.add_constraint([1, 1, 1], Business.landSurface, "<=")
            t.add_constraint([1, 0, 0], Business.__minForestSurface, ">=")

        t.solve()

        self.areaDict = {Business.__landTypes[i]:value for i,value in enumerate(t.solution_dict.values())}
        self.yearProfit = t.max_result
        print(self.areaDict)
        print(self.yearProfit)

        self.availableMoney += self.yearProfit
        print(self.availableMoney)

        self.currentYear += 1

        # self.yearlySurfaceList.append(self.areaDict)
        # self.yearlyExpectedProfitList.append(self.yearProfit)

    def caseOne(self):
        self.caseSpecifier = 1
        self.valuesInitialisation()
        
    def caseTwo(self):
        self.caseSpecifier = 2
        self.valuesInitialisation()

    def caseThree(self):
        self.caseSpecifier = 3
        self.valuesInitialisation()

    def valuesInitialisation(self):
        self.currentYear = 0
        self.availableMoney = self.initialMoney
        self.yearProfit = None
        self.areaDict = {land_type:0 for land_type in Business.__landTypes}
        self.profitPerSqKm_dict["forest"] = Business.__forestRevenuePerSqKm - \
            Business.__forestLandCost
        self.profitPerSqKm_dict["potatoes"] = Business.__amountPotatoesPerSqKm * \
            Business.__pricePerTonPotatoes - (Business.__nonForestLandCost + \
            Business.__costPotatoesSeeds + Business.__costTractor)
        self.profitPerSqKm_dict["grape"] = Business.__amountGrapePerSqKm * \
            Business.__winePerTonOfGrape * Business.__priceLitreWine - \
            (Business.__nonForestLandCost + Business.__costGrapeSeed + \
            Business.__costWorkers)
        self.costsBeforeSale_dict["potatoes"] = Business.__costPotatoesSeeds + \
            Business.__costTractor
        self.costsBeforeSale_dict["grape"] = Business.__costGrapeSeed + \
            Business.__costWorkers

if __name__ == '__main__':
    my_business = Business(1500)
    my_business.caseOne()
