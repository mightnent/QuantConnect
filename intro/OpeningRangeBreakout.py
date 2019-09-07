class OpeningRangeBreakout(QCAlgorithm):

    ############################################################################################
    #   This whole idea of using consolidated bars is to allow customization to your algo.     # 
    #   If your algo needs 40min data, QC has no such methods to retrieve this kind of data.   # 
    #   Hence, you create this type of bars yourself, from smaller resolution.                 #     
    ############################################################################################

    #define variable openingBar to store consolidated bar
    openingBar = None 
    
    def Initialize(self):
        self.SetStartDate(2018, 7, 10)  
        self.SetEndDate(2019, 6, 30)  
        self.SetCash(100000)
        self.AddEquity("TSLA", Resolution.Minute)
        self.Consolidate("TSLA", timedelta(minutes=30), self.OnDataConsolidated)
        
        #3. Create a scheduled event triggered at 13:30 calling the ClosePositions function everyday on TSLA ticker
        self.Schedule.On(self.DateRules.EveryDay("TSLA"),self.TimeRules.At(13,30),self.ClosePositions)
        
    def OnData(self, data):
        
        #if invested or no bar was created, just break
        if self.Portfolio.Invested or self.openingBar is None:
            return
        
        #if breakout high, long 100%
        if data["TSLA"].Close > self.openingBar.High:
            self.SetHoldings("TSLA", 1)

        #if breakout low, short 100%
        elif data["TSLA"].Close < self.openingBar.Low:
            self.SetHoldings("TSLA", -1)  
         
    #we create a starting bar from 9.30, since timedelta is 30min, will end at 10
    def OnDataConsolidated(self, bar):
        if bar.Time.hour == 9 and bar.Time.minute == 30:
            self.openingBar = bar
    #this same code can also be written using EndTime method
        # if bar.EndTime.hour == 10 and bar.EndTime.minute == 0:
        #     self.openingBar = bar
    
    #1. Create a function named ClosePositions(self)
    def ClosePositions(self):
        #2. Set self.openingBar to None, and liquidate TSLA
        self.openingBar = None
        self.Liquidate("TSLA")
