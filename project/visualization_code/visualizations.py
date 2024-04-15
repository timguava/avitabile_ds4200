import altair as alt
import numpy as np
import pandas as pd
from collections import Counter


expanded_data = pd.read_csv('processed_data_part5.csv',index_col=0)
expanded_data['effective_end'] = expanded_data['end']
for i in range(len(expanded_data)):
    expanded_data.at[i,'start'] = int(expanded_data.at[i,'start'])
    if (expanded_data.at[i,'end']=='Incumbent'):
        expanded_data.at[i,'effective_end'] = 2025
    else:
        expanded_data.at[i,'end'] = int(expanded_data.at[i,'end'])
        expanded_data.at[i,'effective_end'] = int(expanded_data.at[i,'end'])
    if (expanded_data.at[i,'born']!='unknown'):
        expanded_data.at[i,'born'] = int(expanded_data.at[i,'born'])
    if (expanded_data.at[i,'died'] not in ['unknown','none']):
        expanded_data.at[i,'died'] = int(expanded_data.at[i,'died'])
    
    if (type(expanded_data.at[i,'president']) is float):
        expanded_data.at[i,'president'] = ''
    if (type(expanded_data.at[i,'vice_president']) is float):
        expanded_data.at[i,'vice_president'] = ''
    if (type(expanded_data.at[i,'senator']) is float):
        expanded_data.at[i,'senator'] = ''
    if (type(expanded_data.at[i,'representative']) is float):
        expanded_data.at[i,'representative'] = ''
    if (type(expanded_data.at[i,'state']) is float):
        expanded_data.at[i,'state'] = ''




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

def age_breakdown(expanded_data, office):
    final_table = pd.DataFrame(columns=['year','percentile','value'])
    for year in range(1789,2025):
        year_data = get_members(expanded_data,office,year)
        year_data = year_data[year_data['born']!='unknown']
        year_data['age'] = year - year_data['born']
        ages = list(year_data['age'])
        final_table.loc[len(final_table.index)] = [year,'min',min(ages)]
        final_table.loc[len(final_table.index)] = [year,'25th percentile',np.percentile(ages,25)]
        final_table.loc[len(final_table.index)] = [year,'median',np.percentile(ages,50)]
        final_table.loc[len(final_table.index)] = [year,'75th percentile',np.percentile(ages,75)]
        final_table.loc[len(final_table.index)] = [year,'max',max(ages)]
    return final_table

def duration_breakdown(expanded_data, office):
    final_table = pd.DataFrame(columns=['year','percentile','value'])
    for year in range(1789,2025):
        year_data = get_members(expanded_data,office,year)
        year_data['dur'] = year - year_data['start'] + year_data['prev_time']
        durs = list(year_data['dur'])
        final_table.loc[len(final_table.index)] = [year,'min',min(durs)]
        final_table.loc[len(final_table.index)] = [year,'25th percentile',np.percentile(durs,25)]
        final_table.loc[len(final_table.index)] = [year,'median',np.percentile(durs,50)]
        final_table.loc[len(final_table.index)] = [year,'75th percentile',np.percentile(durs,75)]
        final_table.loc[len(final_table.index)] = [year,'max',max(durs)]
    return final_table

def get_seats(expanded_data, office, template):
    final_columns = ['year','x','y','name','state','party','party_category','gender','born','dur']
    final_table = pd.DataFrame(columns=final_columns)
    for year in range(1789,2025):
        print(office, year)
        year_data = get_members(expanded_data,office,year)
        year_data['year'] = year
        #fix age
        year_data['dur'] = year - year_data['start'] + year_data['prev_time']
        year_data = year_data.sort_values(by=['party_category','dur'],ascending=False)
        leading_empties = int((len(template)-len(year_data))/2)
        xs = list(template['x'])[leading_empties:len(year_data)+leading_empties]
        ys = list(template['y'])[leading_empties:len(year_data)+leading_empties]
        year_data['x'] = xs
        year_data['y'] = ys
        year_data = year_data[final_columns]
        final_table = pd.concat([final_table,year_data])
    return final_table

def make_d3_file(expanded_data):
    d3_file = pd.DataFrame(columns=['year','senate','house'])
    
    senate = breakdown_by_year(expanded_data,'senator','gender')
    house = breakdown_by_year(expanded_data,'representative','gender')
    
    senate = senate[senate['gender']=='F'].reset_index(drop=True)
    house = house[house['gender']=='F'].reset_index(drop=True)
    
    for i in range(len(senate)):
        d3_file.loc[len(d3_file.index)] = [1789+i,senate.iloc[i]['pct'],house.iloc[i]['pct']]
    
    return d3_file

gender_color = alt.Scale(domain=['M', 'F'], range=['blue', 'pink'])
party_color = alt.Scale(domain=['Democratic', 'Republican', 'Democratic-Republican', 'Federalist', 'Whig', 'Independent', 'Other'], range=['blue', 'red', 'green', 'orange', 'yellow', 'purple', 'gray'])


#gender and party charts
senator_parties = breakdown_by_year(expanded_data,'senator','party_category')
representative_parties = breakdown_by_year(expanded_data,'representative','party_category')
senator_gender = breakdown_by_year(expanded_data,'senator','gender')
representative_gender = breakdown_by_year(expanded_data,'representative','gender')

selected_year = alt.selection_interval(encodings=['x'])

senate_gender = alt.Chart(senator_gender).mark_area().encode(
    alt.X('year').axis(format='i').title('year'),
    alt.Y('pct').axis(format='%').title('percentage'),
    color=alt.Color('gender',scale=gender_color)
).properties(
    title='Senate Gender'
).add_params(
    selected_year
)
house_gender = alt.Chart(representative_gender).mark_area().encode(
    alt.X('year').axis(format='i').title('year'),
    alt.Y('pct').axis(format='%').title('percentage'),
    color=alt.Color('gender',scale=gender_color)
).properties(
    title='House Gender'
).add_params(
    selected_year
)

senate_gender_pie = alt.Chart(senator_gender).mark_arc().encode(
    theta='num',
    color='gender',
).transform_filter(
    selected_year
)
house_gender_pie = alt.Chart(representative_gender).mark_arc().encode(
    theta='num',
    color='gender',
).transform_filter(
    selected_year
)

senate_party = alt.Chart(senator_parties).mark_area().encode(
    alt.X('year').axis(format='i').title('year'),
    alt.Y('pct').axis(format='%').title('percentage'),
    color=alt.Color('party_category',scale=party_color)
).properties(
    title='Senate Party'
).add_params(
    selected_year
)
house_party = alt.Chart(representative_parties).mark_area().encode(
    alt.X('year').axis(format='i').title('year'),
    alt.Y('pct').axis(format='%').title('percentage'),
    color=alt.Color('party_category',scale=party_color)
).properties(
    title='House Party'
).add_params(
    selected_year
)

senate_party_pie = alt.Chart(senator_parties).mark_arc().encode(
    theta='num',
    color='party_category',
).transform_filter(
    selected_year
)
house_party_pie = alt.Chart(representative_parties).mark_arc().encode(
    theta='num',
    color='party_category',
).transform_filter(
    selected_year
)

senate_gender = senate_gender & senate_gender_pie
house_gender = house_gender & house_gender_pie
gender_charts = senate_gender | house_gender

senate_party = senate_party & senate_party_pie
house_party = house_party & house_party_pie
party_charts = senate_party | house_party

gender_charts.save('gender.html')
party_charts.save('party.html')


#age and duration charts
senate_age = age_breakdown(expanded_data,'senator')
representative_age = age_breakdown(expanded_data,'representative')
senate_duration = duration_breakdown(expanded_data,'senator')
representative_duration = duration_breakdown(expanded_data,'representative')


senate_age_chart = alt.Chart(senate_age).mark_line().encode(
    alt.X('year').axis(format='i').title('year'),
    alt.Y('value').axis(format='i').title('age'),
    color='percentile'
).properties(
    title='Senate Age'
)
representative_age_chart = alt.Chart(representative_age).mark_line().encode(
    alt.X('year').axis(format='i').title('year'),
    alt.Y('value').axis(format='i').title('age'),
    color='percentile'
).properties(
    title='House Age'
)

senate_dur_chart = alt.Chart(senate_duration).mark_line().encode(
    alt.X('year').axis(format='i').title('year'),
    alt.Y('value').axis(format='i').title('duration').scale(domain=(0, 60)),
    color='percentile'
).properties(
    title='Senate Duration'
)
representative_dur_chart = alt.Chart(representative_duration).mark_line().encode(
    alt.X('year').axis(format='i').title('year'),
    alt.Y('value').axis(format='i').title('duration').scale(domain=(0, 60)),
    color='percentile'
).properties(
    title='House Duration'
)

age_charts = senate_age_chart | representative_age_chart
dur_charts = senate_dur_chart | representative_dur_chart
all_time_charts = alt.vconcat(age_charts, dur_charts)

all_time_charts.save('age_charts.html')




#main seating chart
senate_template = pd.read_csv('senate_template.csv',index_col=0)
house_template = pd.read_csv('house_template.csv',index_col=0)

senate_seats = get_seats(expanded_data,'senator',senate_template)
house_seats = get_seats(expanded_data,'representative',house_template)


slider = alt.binding_range(min=1789, max=2024, step=1, name='Year: ')
select_year = alt.selection_point(name='year', fields=['year'], bind=slider, value={'year':2024})


senate_chart = alt.Chart(senate_seats).mark_circle(size=250).encode(
    x=alt.X('x',axis=None),
    y=alt.Y('y',axis=None),
    color=alt.Color('party_category',scale=party_color),
    tooltip=['name','state','gender','party','born','dur']
).properties(
    width=800,
    height=400,
    title='Senate'
).configure_axis(
    grid=False
).add_params(
    select_year
).transform_filter(
    select_year
)

house_chart = alt.Chart(house_seats).mark_circle(size=100).encode(
    x=alt.X('x',axis=None),
    y=alt.Y('y',axis=None),
    color=alt.Color('party_category',scale=party_color),
    tooltip=['name','state','gender','party','born','dur']
).properties(
    width=800,
    height=400,
    title='House of Representatives'
).configure_axis(
    grid=False
).add_params(
    select_year
).transform_filter(
    select_year
)


senate_chart.save('senate_chart.html')
house_chart.save('house_chart.html')


d3_file = make_d3_file(expanded_data)
d3_file.to_csv('gender_d3.csv')