class BootCampTask(QCAlgorithm):
    #in general, anything with self becomes a global variable
    
    # Order ticket for our stop order, Datetime when stop order was last hit
    stopMarketTicket = None
    stopMarketOrderFillTime = datetime.min

    #this merely sets a starting var for us to update later
    highestSPYPrice = -1
    
    def Initialize(self):
        self.SetStartDate(2018, 12, 1)
        self.SetEndDate(2018, 12, 10)
        self.SetCash(100000)
        spy = self.AddEquity("SPY", Resolution.Daily)
        spy.SetDataNormalizationMode(DataNormalizationMode.Raw)
        
    def OnData(self, data):
        
        # 1. Plot the current SPY price to "Data Chart" on series "Asset Price"
        #refer to plotting doc @ https://www.quantconnect.com/docs/algorithm-reference/charting
        self.Plot("Data Chart", "Asset Price", data["SPY"].Close)
        
        #if previous stop loss fulfilled in less than 15 days, do nothing
        if (self.Time - self.stopMarketOrderFillTime).days < 15:
            return

        #check if invested in this asset
        if not self.Portfolio.Invested:
            #if not, buy 500 of this asset
            self.MarketOrder("SPY", 500)
            #setting a stop loss
            #stopMarketOrder will have a OrderId
            self.stopMarketTicket = self.StopMarketOrder("SPY", -500, 0.9 * self.Securities["SPY"].Close)
            #stopMarketTicket has been updated, will not be none.
        
        else:            
            #2. Plot the moving stop price on "Data Chart" with "Stop Price" series name
            self.Plot("Data Chart", "Stop Price", self.stopMarketTicket.Get(OrderField.StopPrice))
            
            #if close is > than var highestSPYPrice(which is currently -1)
            if self.Securities["SPY"].Close > self.highestSPYPrice:
                #update the var to the actual price
                self.highestSPYPrice = self.Securities["SPY"].Close
                #updating new stop loss based on the new highestSPYPrice
                updateFields = UpdateOrderFields()
                updateFields.StopPrice = self.highestSPYPrice * 0.9
                self.stopMarketTicket.Update(updateFields) 
            
    def OnOrderEvent(self, orderEvent):
        #check if order has been filled based on orserStatus.Filled    
        if orderEvent.Status != OrderStatus.Filled:
            return
        #orderStatus will also generate an Id. check againt that stopMarketTicket
        if self.stopMarketTicket is not None and self.stopMarketTicket.OrderId == orderEvent.OrderId: 
            #note down the time when order is filled
            self.stopMarketOrderFillTime = self.Time
            
            
