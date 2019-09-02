class MomentumBasedTacticalAllocation(QCAlgorithm):
    
    def Initialize(self):
        
        self.SetStartDate(2007, 8, 1) 
        self.SetEndDate(2010, 8, 1)  
        self.SetCash(3000)  
        
        #add 2 equities to compare
        self.spy = self.AddEquity("SPY", Resolution.Daily)  
        self.bnd = self.AddEquity("BND", Resolution.Daily)  

        #set up momentum percent indicator
        # M(t) = P(t)-P(t-n)
        # M% = M(t)/M(max)
        self.spyMomentum = self.MOMP("SPY", 50, Resolution.Daily) 
        self.bondMomentum = self.MOMP("BND", 50, Resolution.Daily) 
       
        self.SetBenchmark(self.spy.Symbol)  

        #walm up algo with 50 days data before the start date
        self.SetWarmUp(50) 
  
    def OnData(self, data):
        
        #check if warm up done. opp of IsWarmingUp is IsReady
        if self.IsWarmingUp:
            return
        
        #1. Limit trading to happen once per week on wed
        #monday is 0
        #place trade on tue(1) so that it can trade on wednesday
        if not self.Time.weekday() == 1:
            return

        #compare momentum% inducator. this is just syntax
        if self.spyMomentum.Current.Value > self.bondMomentum.Current.Value:
            #liquidate 1 and convert to the other one fully(100%=1)
            self.Liquidate("BND")
            self.SetHoldings("SPY", 1)
            
        else:
            self.Liquidate("SPY")
            self.SetHoldings("BND", 1)
            


