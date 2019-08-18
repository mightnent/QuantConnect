#Market order: 
class BootCampTask(QCAlgorithm):

    def Initialize(self):
        self.SetCash(100000)
        self.SetStartDate(2017, 5, 1)
        self.SetEndDate(2017, 5, 31)
        
        #1. Request the forex data
        self.AddForex("AUDUSD",Resolution.Hour,Market.Oanda)
        
        #2. Set the brokerage model
        self.SetBrokerageModel(BrokerageName.OandaBrokerage)
        
    def OnData(self, data):
        #3. Using "Portfolio.Invested" submit 1 order for 2000 AUDUSD:
        if not self.Portfolio["AUDUSD"].Invested:
            self.MarketOrder("AUDUSD", 2000)
            
########################################################################################################################################
unrelated segment of code below
########################################################################################################################################

#Round lotsize: 
class BootCampTask(QCAlgorithm):
 
    def Initialize(self):

        self.SetCash(100000)
        self.SetStartDate(2017, 5, 1)
        self.SetEndDate(2017, 5, 31)
        self.AddForex("EURUSD", Resolution.Hour, Market.Oanda)
        self.SetBrokerageModel(BrokerageName.OandaBrokerage)
        
        #1. Save lot size to "self.lotSize"
        self.lotSize = float(self.Securities["EURUSD"].SymbolProperties.LotSize)
        
        #2. Print the lot size:
        self.Debug("The lot size is " + str(self.lotSize))
        
        #3. Round the order to the log size, save result to "self.roundedOrderSize"
        self.orderQuantity = 20180.12
        self.roundedOrderSize = round(self.orderQuantity/self.lotSize) * self.lotSize
        self.Debug("The order size is " + str(self.roundedOrderSize))
        
    def OnData(self, data):
        pass
