# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 20:04:09 2019

@author: Sam Purkiss
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

def initiate_browser(chromedriver_path):
    ''' Simple function to intiate and open the browser to the Federal Court page.
    Once the function is run once, it's simple to run the get_all_proceedings function
    and only change the search_query without having to close and reopen the browser.
    Initializes the browser to search by IP.
    parameters:
        chromedriver_path: where you've saved the chromedriver file
    returns:
        driver: an initialized browser that can now run queries
    
    ----------------------------------------------------------------
    Example:
        driver = initiate_browser('C:/Program Files (x86)/chromedriver.exe')
    '''
    driver = webdriver.Chrome(chromedriver_path)
    website = 'http://apps.fct-cf.gc.ca/pq/IndexingQueries/infp_queries_e.php?stype=intltProperty&select_court=T'
    driver.get(website)
    
    return driver    

def get_all_proceedings(web_driver, search_query):
    """
    This function uses the initialized browser to run a search query which
    returns a dataframe containing all the results.
    paramaters:
        web_driver: reference to the initialized browser from the initiate_browser 
        function.
        search_query: any combination of characters saved as a string which can be 
        used to query federal court proceedings.
            see http://apps.fct-cf.gc.ca/pq/IndexingQueries/infp_help_e.php for details
            and tips on search queries
    returns:
        proceedings: a dataframe with a full list of all proceedings identified by 
        the search query with the following columns:
            'court_number_link', 'style_of_cause', 'nature_of_proceeding', 're_link'
    ------------------------------------------------------------------
    Example:
        driver = initiate_browser('C:/Program Files (x86)/chromedriver.exe')
        proceedings_table = get_all_proceedings(driver, 'FACEBOOK')
    """
    
    #Initiate blank dataframe for writing to
    proceedings = pd.DataFrame()
    ########################################################
    # Open browser and search phrase
    ########################################################
    search_index = web_driver.find_element_by_xpath('//*[@id="in1"]')
    #Clear the input line in case there's already a query in it
    search_index.clear()
    search_index.send_keys(search_query)
    submit_button = web_driver.find_element_by_xpath('//*[@id="MainContent"]/form[2]/div/div[7]/input[1]')
    submit_button.click()
    sleep(10)
    
    html = web_driver.page_source
    
    soup = BeautifulSoup(html,'lxml')
    
    
    ########################################################
    # Create data table with results from search phrase
    ########################################################
    
    search_results = soup.find_all('tr')
    #The first reference is blank which is why I start at 1 and not 0
    for i in range(1, len(search_results)):
        first= search_results[i].find_all('td')
        temp = pd.DataFrame()
        #first is a list of all the items in one row.
        #Refer to the specific column values using the following references:
    #    0: Court Number	column
    #    1: Style of Cause column
    #    2: Nature of Proceeding column
    #    3: RE column
        
        
        court_number_link = 'http://apps.fct-cf.gc.ca/pq/IndexingQueries/' + first[0].find_all('a', href=True)[0]['href']
        court_number = first[0].text
        style_of_cause = first[1].text
        nature_of_proceeding = first[2].text
        re_link = 'http://apps.fct-cf.gc.ca/pq/IndexingQueries/' + first[3].find_all('a', href=True)[0]['href']
            
        temp['court_number_link'] = [court_number_link]
        temp['court_number'] = [court_number]
        temp['style_of_cause'] = [style_of_cause]
        temp['nature_of_proceeding']=[nature_of_proceeding]
        temp['re_link']=[re_link]
        proceedings = proceedings.append(temp)
           
        print(str(i)+'. Just finished %s' %style_of_cause)
    
    return proceedings







