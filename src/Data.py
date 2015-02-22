import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import os.path
import pandas as pd
import random
import re

def to_number(s):
    try:
        s1 = float(s)
        return s1
    except ValueError:
        return np.NaN
    
if __name__ == '__main__':
    minwage = pd.read_csv("C:/Users/itaraday/Downloads/CODE2015/historicalminimumwageratesincanada-ENG.csv")
    minwage['Effective Date'] = pd.to_datetime(minwage['Effective Date'])
    minwage['year'] = minwage['Effective Date'].dt.year
    minwage["min wage"] = minwage["Minimum Wage"].str.replace(r'[$,]', '').astype('float')
    minwage = minwage[minwage["min wage"] < 20]
    
    prov_yearly_min_wage_avg = minwage.groupby(["Jurisdiction","year"])["min wage"].mean()
    
    prov_yearly_min_wage_avg_graph = prov_yearly_min_wage_avg.unstack("Jurisdiction")
    colors = plt.cm.rainbow(np.linspace(0, 1, len(prov_yearly_min_wage_avg_graph.columns)))
    prov_yearly_min_wage_avg_graph.plot(title="Average Min Wage per Year in Canada", color=colors)
    plt.xlabel('Year')
    plt.ylabel('Amount in $')
    plt.show()    

    filePath = os.path.dirname(os.path.abspath(__file__)) 
    undergrads = pd.read_csv(filePath + "/Weighted Avg Under Grad.csv")
    undergrads = undergrads[undergrads["GEO"] != "Canada"]
    undergrads["year"] = undergrads["Ref_Date"].apply(lambda x: x.split("/")[0])
    undergrads = undergrads[["GEO", "Value", "GROUP", "year"]]
    
    undergrads["Value"] = undergrads["Value"].apply(lambda x : to_number(x))
    
    minyear = undergrads["year"].astype('int').min()
    maxyear = undergrads["year"].astype('int').max()+1
    provs = undergrads["GEO"].unique()
    
    for prov in provs:
        groups = undergrads.loc[undergrads["GEO"] == prov, "GROUP"].unique()
        title = "Undergrad tuition in {}".format(prov)
        file = "C:/Users/itaraday/Downloads/CODE2015/{}.png".format(title)
        plt.figure()
        plt.title(title)
        colormap = plt.cm.gist_ncar
        plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, len(undergrads["GROUP"].unique()))])
    
        for group in groups:
            x = undergrads.loc[(undergrads["GEO"] == prov) & (undergrads["GROUP"] == group), "year"].tolist()
            y = undergrads.loc[(undergrads["GEO"] == prov) & (undergrads["GROUP"] == group), "Value"].tolist()
            ticks = np.arange(minyear, maxyear)
            labels = ticks
            plt.plot(x, y, label=group)    
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xlabel('Year')
        plt.ylabel('Amount in $')
        plt.xticks(ticks, labels)
        plt.savefig(file, bbox_inches='tight')
                    

def fit_line2(x, y):
    X = sm.add_constant(x, prepend=True) #Add a column of ones to allow the calculation of the intercept
    ols_test = sm.OLS(y, X,missing='drop').fit()
    """Return slope, intercept of best fit line."""
    X = sm.add_constant(x)
    return ols_test
    
class dataset: 
    def __init__(self):
        filePath = os.path.dirname(os.path.abspath(__file__)) 
        self.undergrads = pd.read_csv(filePath + "/Weighted Avg Under Grad.csv")
        self.employment = pd.read_csv(filePath + "/employment.csv")
        self.undergrads = self.undergrads[self.undergrads["GEO"] != "Canada"]
        print self.undergrads.columns
        
    def getprovs(self):
        print "provs\n{}".format(self.undergrads["GEO"].unique())
        return self.undergrads["GEO"].unique()
    
    def getfields(self):
        print "fields\n{}".format(self.undergrads["GROUP"].unique())
        return self.undergrads["GROUP"].unique()
    #pd.read_csv("C:/Users/itaraday/Downloads/CODE2015/Weighted Avg Under Grad.csv")
    
    def getNAICS(self):
        NAICS = self.employment["NAICS"].unique().tolist()
        pattern = re.compile('[^a-zA-Z ,]+')
        formatedNAICS = {}
        for i in NAICS:
            formatedNAICS[i] = re.sub(pattern, '', i);
        print "NAICS\n{}".format(NAICS)
        return formatedNAICS

        
    def run(self, mysemesters, myyears, mystart, myfield, myprov, NAICS):       
        print "running"
        undergrads = self.undergrads
        undergrads["year"] = undergrads["Ref_Date"].apply(lambda x: x.split("/")[0])
        undergrads["year"] = undergrads["year"].astype(int)
        undergrads = undergrads[["GEO", "Value", "GROUP", "year"]]
        undergrads["Value"] = undergrads["Value"].apply(lambda x : to_number(x))
        undergrads = undergrads[(undergrads["GEO"] == myprov) &
                                (undergrads["GROUP"] == myfield)
                                ]
        if not len(undergrads):
            print "Sorry not enough data for this selection to make a prediction"
            return
        x = undergrads['year'][1:-1]
        y = undergrads['Value'][1:-1]
        model = fit_line2(x,y)
        #print model.summary()
        cost = 0
        for year in range(mystart, mystart+myyears+1):
            yearCost = model.predict([[1,year]])[0]
            yearCost = yearCost * mysemesters
            cost = cost + yearCost
        print "Total cost predicted at ${}".format(round(cost,2))
        
        employment = self.employment[(self.employment["Geography"] == myprov) &
                                (self.employment["NAICS"] == NAICS)
                                ]
        employment = pd.melt(employment, id_vars=["Geography", "Labour force characteristics", "NAICS", "Sex", "Age group"], 
                  var_name="Date", value_name="Value")
        employment["Value"] = employment["Value"].apply(lambda x : to_number(x))
        employment["Value"] = employment["Value"] * 1000
        employment["Year"] = employment["Date"].apply(lambda x: x.split("-")[1]).astype('int')
        employment["Year"] = employment["Year"] + 2000
        employmentGroup = employment[employment["Labour force characteristics"] == "Employment (2)"].groupby("Year")["Value"].sum().reset_index()
        x = employmentGroup['Year'][1:-1]
        y = employmentGroup['Value'][1:-1]
        modelEmployment = fit_line2(x,y)      
        #print modelEmployment.summary()  
        jobyear = mystart+myyears+1
        print "Total jobs predicated for {} is {}".format(jobyear, round(modelEmployment.predict([[1,jobyear]])[0]),0)