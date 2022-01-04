import bs4 as bs
import requests
import numpy as np
from dateutil.parser import parse
import pandas as pd

from style import *
from regression import *


class Stocks(object):

    def get_market_cap(self):
        url = 'https://ycharts.com/companies/'+self.ticker+'/market_cap'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class':'table'})
        string = table.find_all('td')[1].text.strip()
        market_cap = string_to_num(string)
        return market_cap
        
    def get_dividend(self):
        url = 'https://ycharts.com/companies/'+self.ticker+'/dividend_yield'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class':'table'})
        string = table.find_all('td')[1].text.strip()
        string = string.replace('%','')
        dividend = float(string)/100
        dividend = dividend*self.market_cap  
        return dividend
    
    def get_pe(self):
        url = 'https://ycharts.com/companies/'+self.ticker
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        tables = soup.findAll('table', {'class':'table'})
        table = tables[0]        
        for row in table.find_all('tr')[1:]:
            if row.find_all('td')[0].text.strip()  == 'PE Ratio':
                pe = row.find_all('td')[1].text.strip()
                break
        if pe == "--":
            pe = 0.0
            result = "Negative/Problem"
        else:
            pe = float(pe)
            if float(pe) > 20:
                result = "Problem"
            else:
                result = "OK"
                self.pillars += 1
        return pe,result
    
    def get_profit_margins(self):
        url = 'https://ycharts.com/companies/'+self.ticker+'/profit_margin'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        tables = soup.findAll('table', {'class':'table'})
        profits = []
        dates = []
        for table in tables:
            if table.find_all('tr')[1:2] == []:
                result = "Data not found"
                self.not_found += 1
            else:
                for row in table.find_all('tr')[1:]:
                   profit = row.find_all('td')[1].text.strip()
                   if profit != ""  and "K" not in profit and "M" not in profit: #K and M correspond to one-time margins, so we ignore them
                        profit = profit.replace('%','')
                        date = row.find_all('td')[0].text.strip()
                        try:
                            date = parse(date)
                            dates.append(date) 
                            profits.append(float(profit))
                        except:
                            break
        if len(profits) > 20: #20 corresponds to 20 filings - 5 years
            profits = profits[:20]
        profits = np.array(profits)
        dates = dates[:len(profits)]
        if np.mean(profits) < 10:
            result = "Problem"
        else:
            result = "OK"
            self.pillars += 1
        margins = pd.DataFrame(list(zip(dates,profits)), columns =['Date', 'Profit margin (%)'])
        return margins,result
    
    def get_revenues(self):
        url = 'https://ycharts.com/companies/'+self.ticker+'/revenues_ttm'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        tables = soup.findAll('table', {'class':'table'})
        revenues = []
        dates = []
        for table in tables:
            if table.find_all('tr')[1:2] == []:
                result = "Data not found"
                self.not_found += 1
                return 
            for row in table.find_all('tr')[1:]: 
                revenue = row.find_all('td')[1].text.strip() 
                date = row.find_all('td')[0].text.strip()
                try:
                    date = parse(date)
                    dates.append(date) 
                    revenues.append(string_to_num(revenue))
                except:
                    break
        if len(revenues) > 20:
            revenues = revenues[:20]
            dates = dates[:20]
        revenues = pd.DataFrame(list(zip(dates,revenues)), columns =['Date', 'Revenue'])
        if regression(revenues['Revenue'],"up") == 1:
            result = "OK"
            self.pillars += 1
        else:
            result = "Problem"
        return revenues,result
    
    def get_incomes(self):
        url = 'https://ycharts.com/companies/'+self.ticker+'/net_income_ttm'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        tables = soup.findAll('table', {'class':'table'})
        incomes = []
        dates = []
        for table in tables:
            if table.find_all('tr')[1:2] == []:
                result = "Data not found"
                self.not_found += 1
                return 
            for row in table.find_all('tr')[1:]: 
                income = row.find_all('td')[1].text.strip() 
                date = row.find_all('td')[0].text.strip()
                try:
                    date = parse(date)
                    dates.append(date) 
                    incomes.append(string_to_num(income))
                except:
                    break       
        if len(incomes) > 20:
            incomes = incomes[:20]
            dates = dates[:20]
        incomes = pd.DataFrame(list(zip(dates,incomes)), columns =['Date', 'Net income'])
        if regression(incomes['Net income'],"up") == 1:
            result = "OK"
            self.pillars += 1
        else:
            result = "Problem"
        return incomes,result
    
    def get_shares_outstanding(self):
        global pillars
        global not_found
        url = 'https://ycharts.com/companies/'+self.ticker+'/shares_outstanding'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        tables = soup.findAll('table', {'class':'table'})
        shares = []
        dates = []
        for table in tables:
            if table.find_all('tr')[1:2] == []:
                result = "Data not found"
                self.not_found += 1
                return 
            for row in table.find_all('tr')[1:]: 
                date = row.find_all('td')[0].text.strip()  
                share = row.find_all('td')[1].text.strip()
                try:
                    date = parse(date)
                    dates.append(date) 
                    shares.append(string_to_num(share))  
                except:
                    break   
        if len(shares) > 20:
            shares = shares[:20]
            dates = dates[:20]
        shares = pd.DataFrame(list(zip(dates,shares)), columns =['Date', 'Shares'])
        if regression(shares['Shares'],"down") == 1:
            result = "OK"
            self.pillars += 1
        else:
            result = "Problem"
        return shares,result

    def get_assets_liabilities(self):
        url = 'https://ycharts.com/companies/'+self.ticker+'/assets'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class':'table'})
        if table.find_all('tr')[1:2] == []:
            result = "Data not found"
            self.not_found += 1
        assets = table.find_all('td')[1].text.strip()
        url = 'https://ycharts.com/companies/'+self.ticker+'/liabilities'
        resp = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class':'table'})
        if table.find_all('tr')[1:2] == []:
            result = "Data not found"
            self.not_found += 1
        liabilities = table.find_all('td')[1].text.strip()
        assets = [string_to_num(assets)]
        liabilities = [string_to_num(liabilities)]
        if liabilities > assets:
            result = "Problem"
        else:
            result = "OK"
            self.pillars += 1
        return pd.DataFrame(list(zip(assets, liabilities)), columns =['Assets', 'Liabilities']),result


    def get_cashflows(self):
        url = 'https://ycharts.com/companies/'+self.ticker+'/free_cash_flow_ttm'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        tables = soup.findAll('table', {'class':'table'})
        cashflows = []
        dates = []
        for table in tables:
            if table.find_all('tr')[1:2] == []:
                result = "Data not found"
                self.not_found += 1
                return 
            for row in table.find_all('tr')[1:]: 
                cashflow = row.find_all('td')[1].text.strip() 
                date = row.find_all('td')[0].text.strip()
                try:
                    date = parse(date)
                    dates.append(date) 
                    cashflows.append(string_to_num(cashflow))
                except:
                    break   
        if len(cashflows) > 20:
            cashflows = cashflows[:20]
            dates = dates[:20]
        cashflows = pd.DataFrame(list(zip(dates,cashflows)), columns =['Date', 'Free cashflow'])
        if regression(cashflows['Free cashflow'],"up") == 1:
            result = "OK"
            self.pillars += 1
        else:
            result = "Problem"
        return cashflows,result           

    def get_pfcf(self):
        pfcf = self.market_cap/self.cashflows[0]['Free cashflow'][0]
        if pfcf < 0:
            result = "Negative/Problem"
        else:
            if pfcf > 20:
                result = "Problem"
            else:
                result = "OK"
                self.pillars += 1
        return pfcf,result

    def enough_dividend(self):
        if self.dividend > 0:
            if self.cashflows[0]['Free cashflow'][0] > 1.2*self.dividend:
                print("Enough cash to pay dividend (>120%): OK")
            else:
                print("Enough cash to pay dividend (>120%): Problem")
            

        
    def check_existence(self):
        url = 'https://ycharts.com/companies/'+self.ticker+'/market_cap'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        if resp.status_code == 404:
            return 1
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class':'table'})
        if table == None:
            return -1
        else:
            return 0  
        
        


    def __init__(self, ticker):
        self.ticker = ticker
        self.error = self.check_existence()
        if self.error == 0:
            self.pillars = 0
            self.not_found = 0
            self.market_cap = self.get_market_cap()
            self.dividend = self.get_dividend()
            self.pe = self.get_pe()
            self.profit_margins = self.get_profit_margins()
            self.revenues = self.get_revenues()
            self.incomes = self.get_incomes()
            self.shares = self.get_shares_outstanding()
            self.assets_liabilities = self.get_assets_liabilities()
            self.cashflows = self.get_cashflows()
            self.pfcf = self.get_pfcf()
