# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 22:35:51 2019

@author: Sam Purkiss
"""
import pandas as pd
from get_federal_court_proceedings import initiate_browser, get_all_proceedings
from string import ascii_lowercase

#This master file is set up to run through all proceedings.
#It does so by searching through all letters, returning results
#and then removing duplicates.

chromedriver_path = 'INSERT PATH HERE'

driver = initiate_browser(chromedriver_path)

proceedings_master = pd.DataFrame()
letter_range = list(ascii_lowercase)
letter_range.append('-')


for letter in letter_range:
    print('On letter %s' %(letter))
    proceedings = get_all_proceedings(driver, letter)
    proceedings_master = proceedings_master.append(proceedings)

# Remove duplicate files
proceedings_master.drop_duplicates(keep='first', inplace=True)
    
# Save as csv file
proceedings_master.to_csv('court_proceedings.csv', index=False)


#Get list of all the different proceeding types
type_of_proceeding =[]
for nature in proceedings_master['nature_of_proceeding']:
    if nature not in type_of_proceeding:
        type_of_proceeding.append(nature)
type_of_proceeding = pd.DataFrame(type_of_proceeding)

type_of_proceeding.to_csv('types_of_proceedings.csv', index=False)
