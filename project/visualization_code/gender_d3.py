import numpy as np
import pandas as pd
from collections import Counter

expanded_data = pd.read_csv('processed_data_part5.csv',index_col=0)
expanded_data['effective_end'] = expanded_data['end']

def get_members(expanded_data, office, year):
    sliced_data = expanded_data[expanded_data[office]!='']
    sliced_data = sliced_data[sliced_data['start']<=year]
    sliced_data = sliced_data[sliced_data['effective_end']>year]
    sliced_data = sliced_data.reset_index(drop=True)
    return sliced_data

def breakdown_by_year(expanded_data, office, metric):
    options = list(set(list(expanded_data[metric])))
    final_table = pd.DataFrame(columns=['year',metric,'num','pct'])
    for year in range(1789,2025):
        year_data = get_members(expanded_data,office,year)
        c = Counter(list(year_data[metric]))
        for entry in options:
            final_table.loc[len(final_table.index)] = [year,entry,c[entry],c[entry]/len(year_data)]
    return final_table

senate = breakdown_by_year(expanded_data,'senator','gender')
house = breakdown_by_year(expanded_data,'representative','gender')

d3_file = pd.DataFrame(columns=['year','senate','house'])