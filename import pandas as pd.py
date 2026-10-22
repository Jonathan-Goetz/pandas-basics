import pandas as pd

movies_1994 = pd.read_excel("disney_messy_data_activity.xlsx", "movies_1994")
movies_1995 = pd.read_excel("disney_messy_data_activity.xlsx", "movies_1995")
movies_2013 = pd.read_excel("disney_messy_data_activity.xlsx", "movies_2013")
movies_lookup = pd.read_excel("disney_messy_data_activity.xlsx", "movie_lookup")

# melt market, replace market string, fix date format 
def add_market(mov, year):
    mov_melted = pd.melt(
    mov,
    id_vars=['movie_id', 'title', 'rated', 'release_date', 'runtime_minutes'],
    var_name='market',
    value_vars=['rev_US_usd', 'rev_EU_usd'],
    value_name='revenue'
    )
    mov_melted['market'] = mov_melted['market'].replace({
        'rev_US_usd': 'USA',
        'rev_EU_usd': 'Europe'
    })
    mov_melted['release_date'] = mov_melted['release_date'] + f"/{year}"
    return mov_melted
    
movies_94_melted = add_market(movies_1994, 1994)

movies_95_melted = add_market(movies_1995, 1995)


# join dataframes
movies_allyears = pd.concat([movies_94_melted, movies_95_melted, movies_2013], ignore_index=True)

# replace rated strings
movies_allyears['rated'] = movies_allyears['rated'].replace({'Rated G': 'G', 'pg': 'PG'})
print(movies_allyears)

# merge movies with lookup
movies = pd.merge(movies_allyears, movies_lookup, how = 'left', on = 'movie_id')

# caslculate missing runtime minutes
movies['runtime_minutes'] = movies['runtime_minutes'].fillna(movies['runtime_hours'] * 60)

# toy story runtime minutes corrected
movies.loc[movies['movie_id'] == 'D03', 'runtime_minutes'] = movies.loc[movies['movie_id'] == 'D03', 'runtime_hours'] * 60

# add category for those missing (ofc. this is lazy, but these are all animated movies)
movies['category'] = movies['category'].fillna('Animation')

# sort by movie_id and drop runtime_hours
movies = movies.sort_values(by=['movie_id'], ignore_index = True).drop(columns = 'runtime_hours')

movies.to_csv("disney_clean.csv", index=False)
print(movies)
