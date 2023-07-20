import numpy as np

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def data_over_time(df,col):
   nation_over_time=df.drop_duplicates(['Year' , col])['Year'].value_counts().reset_index().sort_values('Year')
   nation_over_time.rename(columns={'Year':"Edition" , 'count':col},inplace =True) 
   return nation_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    
    if sport != 'Overall':
        temp_df=temp_df[temp_df['Sport']==sport]
        
    x= temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[['Name','count','region','Sport']].drop_duplicates('Name')
    x.rename(columns = {'count':'Medals'},inplace =True)
    return x
   

def yearwise_meda_tally(df,country):
    temp_df=df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region']==country]
    new_df=temp_df.groupby('Year').count()['Medal'].reset_index()
    return new_df

def country_event_heatmap(df,country):
     temp_df=df.dropna(subset = ['Medal'])
     temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'],inplace=True)
     new_df = temp_df[temp_df['region']==country]
     pt=new_df.pivot_table(index='Sport',columns = 'Year',values = 'Medal',aggfunc='count').fillna(0).astype('int')
     return pt

def most_successful_athelete(df, country):
    temp_df = df.dropna(subset=['Medal'])
    
    temp_df=temp_df[temp_df['region']==country]
        
    x= temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns = {'count':'Medals'},inplace =True)
    return x
   
