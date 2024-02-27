import pandas as pd

df=pd.read_csv("Top Indian Places to Visit.csv")
df=df.drop(columns=['Unnamed: 0', 'Establishment Year','Weekly Off','Zone','State','Significance','Type'])



#Encoding and giving values
pd.set_option('future.no_silent_downcasting', True)
df['DSLR Allowed'] = df['DSLR Allowed'].replace({'Yes'or'yes': 1, 'No'or'no': 0})
df['Best Time to visit'] = df['Best Time to visit'].replace({'All':3,'All ':3,'Anytime':3,'Morning':2,'Afternoon':2,'Evening':1,'Night':0})
df['Airport with 50km Radius'] = df['Airport with 50km Radius'].replace({'Yes'or'yes': 1, 'No'or'no': 0})

'''df['DSLR Allowed'] = df['DSLR Allowed'].replace({'Yes'or'yes': 1, 'No'or'no': 0})
df['Best Time to visit'] = df['Best Time to visit'].replace({'All':3,'All ':3,'Anytime':3,'Morning':2,'Afternoon':2,'Evening':1,'Night':0})
df['Airport with 50km Radius'] = df['Airport with 50km Radius'].replace({'Yes'or'yes': 1, 'No'or'no': 0})''' #Giving warning 

#Assigning new Rating 
df = df.assign(Rating = df['Google review rating'] * df['Number of google review in lakhs'])

df=df.drop(columns=['Google review rating','Number of google review in lakhs'])

# Define Weighted Scoring Function
def calculate_score(row, weights):
    score = 0
    for column_name, weight in weights.items():
        score += row[column_name] * weight
        #score += row[time needed to visit in hrs] *-1
    return score

# Define User Preferences
weights = {
    'time needed to visit in hrs': -1,  # Minimize time needed
    'Entrance Fee in INR': -1,  # Minimize entrance fee
    'Airport with 50km Radius': 1,  # Prefer airport within 50km
    'DSLR Allowed': 1,  # Prefer DSLR allowed
    'Best Time to visit': 1,  # Prefer best time to visit
    'Rating': 1  # Prefer higher rating
}

# Filter DataFrame for Given City
df['City'] = df['City'].str.lower()
city_name = input("Enter a city name to find 5 best places to travel there : ").lower()



#city_df = df[df['City'] == city_name] #SettingWithCopyWarning
city_df = df[df['City'] == city_name].copy()

# Apply Weighted Scoring Function to Filtered DataFrame
city_df['Score'] = city_df.apply(lambda row: calculate_score(row, weights), axis=1)
#city_df.loc[:, 'Score'] = city_df.apply(lambda row: calculate_score(row, weights), axis=1)

sorted_df = city_df.sort_values(by='Score', ascending=False)
#top_5_places = sorted_df.head(5)['Name'].tolist()
print("\nTop 5 places are : \n")
#print(sorted_df.loc[0,5])
for i in range(5):
    print(sorted_df['Name'].iloc[i])
#print(sorted_df.head(5)['Name'].tolist())