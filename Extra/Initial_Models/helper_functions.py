import pandas as pd
import numpy as np

from datetime import datetime

def a(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret

def get_month(date_string):
    POSSIBLE_DATE_FORMATS = ['%d %b %Y ', '%b %Y ', '%Y '] 
    for date_format in POSSIBLE_DATE_FORMATS:
        try:
            return datetime.strptime(date_string, date_format).month 
        except ValueError:
            pass # if incorrect format, keep trying other formats
    return 0
        
    
    

def get_dates_df(df,y):
    '''input the dataframe of movie info (df) and vector of nominee info (y)
    outputs two dataframes:
    a dataframe with imdb_id, day, month, year, and country of original_air_date and
    a dataframe of the corresponding nominee status'''
    dates_df= pd.DataFrame({'imdb_id': [],
                        'day':[],
                        'month':[] ,
                        'year':[],
                        'country':[]})
    new_y=pd.DataFrame({'is_nominee':[]})
    for i in range(0, len(df)):
        #print(i)
        newrow=[]
        row=df.iloc[i]
        #print(row)
        if row['original_air_date'] == []:
            #skip because we don't have info
            pass            
        elif row['original_air_date'][2] == ' ':
            #we have day-month-year
            #print('Day-MY')
            newrow.append(row['imdb_id'])
            newrow.append(row['original_air_date'][0:2] )
            newrow.append(row['original_air_date'][3:6])
            newrow.append(row['original_air_date'][7:11])
            newrow.append(row['original_air_date'][12:])
        elif row['original_air_date'][0] in 'JFMASOND':
            #we have month-year
            #print('MONTH-YEAR!')
            newrow.append(row['imdb_id'])
            newrow.append('')
            newrow.append(row['original_air_date'][0:3])
            newrow.append(row['original_air_date'][4:8])
            newrow.append(row['original_air_date'][9:])
        else: #row['origingal air date'][2] in '1234567890':
            #we have year
            #print('YEAR ONLY!')
            #print(i)
            newrow.append(row['imdb_id'])
            newrow.append('')
            newrow.append('')
            newrow.append(row['original_air_date'][0:5])
            newrow.append(row['original_air_date'][6:])
        #print('newrow is')
        #print(newrow)
        if newrow !=[] :
            dates_df.loc[len(dates_df.index)] = newrow 
            new_y.loc[len(new_y.index)]=y.iloc[i]
    return(dates_df, new_y)

#This is a helper function
def drop_test(df,L):
    '''input a dataframe of movies (df) and a list of years as int (L)
    outputs a dataframe that does not include the movies in years in L'''
    indices =[]
    for i in range(len(df)):
        if df.iloc[i]['year'] in L:
            indices.append(i)
    new_df=df.drop(indices)
    return(new_df)

def timeseries_split(df, k):
    '''takes in a movie dataframe (df),  k (int)
    and outputs a tuple that behaves like kfold.split when kfold =kfold = TimeSeriesSplit(n_splits = k,
                           test_size = 1)
    that is, the output is a tuple of 2-tuples, where
    the first element of each tuple is the indices of the train set and
    the second element is the indices of the test set
    unlike TimeSeriesSplit it can only handle one dataframe at a time'''
    if len(df['year'].value_counts()) <k:
        raise ValueError("Not enough data for given k")
        
    df=df.copy()
    
    answer=[]
    i=0
    while i <k:
        last_year=df['year'].max()
        
        #get array of indices of last year in list
        index_set=np.array(df[df['year']==last_year].index)
        
        #delete rows from dataframe
        df=drop_test(df,[last_year])
        
        #get array of indices of training set
        index_set2=np.array(df.index)
        
        #create the tuple for this
        new_set=(index_set2, index_set)
        
        #append it to our final answer
        answer=[new_set] + answer
        
        i=i+1
    
    return tuple(answer)