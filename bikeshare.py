import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "None" to apply no month filter
        (str) day - name of the day of week to filter by, or "None" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
        cities= ['chicago','new york city','washington']
        city= input("\n Which city are you interested in? (Chicago, New york city, Washington) \n").lower()
        if city in cities:
            break
        else:
            print("\n Kindly enter a correct city name")    


    while True:
        months= ['January','February','March','April','June','May','None']
        month = input("\n Which month are you interested in? (January, February, March, April, May, June)? Type 'None' for no month filter\n").title()
        if month in months:
            break
        else:
            print("\n Kindly enter a correct month")    

    while True:
        days= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','None']
        day = input("\n Which day of the week are you interested in? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)? Type 'None' for no day filter \n").title()         
        if day in days:
            break
        else:
            print("\n Kindly enter a correct week day")    
    


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "None" to apply no month filter
        (str) day - name of the day of week to filter by, or "None" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    if month != 'None':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)+1
    
    
        df = df[df['month']==month] 

    if day != 'None':
        df = df[df['day_of_week']==day]

    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month =='None':
        com_month= df['month'].mode()[0]
        months= ['January','February','March','April','May','June']
        com_month= months[com_month-1]
        print("The most common month is",com_month)


    # display the most common day of week
    if day =='None':
        com_day= df['day_of_week'].mode()[0]
        print("The most Popular day is",com_day)


    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    com_start_hour=df['Start Hour'].mode()[0]
    print("The popular Start Hour is {}:00 hrs".format(com_start_hour))


    print("\nComputed in %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nComputing The Most Common Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    com_start_station= df['Start Station'].mode()[0]
    print("The most commonly used Start Station is {}".format(com_start_station))


    # display most commonly used end station
    com_end_station= df['End Station'].mode()[0]
    print("The most commonly used End Station is {}".format(com_end_station))

    # display most frequent combination of start station and end station trip
    df['combination']=df['Start Station']+" "+"to"+" "+ df['End Station']
    pop_com= df['combination'].mode()[0]
    print("The most common combination of Start and End Station is {} ".format(pop_com))


    print("\nComputed in %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nComputing Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    minute,second=divmod(total_travel_time,60)
    hour,minute=divmod(minute,60)
    print("The total travel time is: {} hour(s) {} minute(s) {} second(s)".format(hour,minute,second))
    
    # display mean travel time
    average_travel_time=round(df['Trip Duration'].mean())
    m,sec=divmod(average_travel_time,60)
    if m>60:
        h,m=divmod(m,60)
        print("The average travel time is: {} hour(s) {} minute(s) {} second(s)".format(h,m,sec))
    else:
        print("The average travel time is: {} minute(s) {} second(s)".format(m,sec))

    print("\nComputed in %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nComputing User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts= df['User Type'].value_counts()
    print("The user types are:\n",user_counts)


    # Display counts of gender
    if city.title() == 'Chicago' or city.title() == 'New York City':
        gender_counts= df['Gender'].value_counts()
        print("\nThe counts of each gender are:\n",gender_counts)
    
    # Display earliest, most recent, and most common year of birth
        earliest= int(df['Birth Year'].min())
        print("\nThe oldest user is born in the year",earliest)
        most_recent= int(df['Birth Year'].max())
        print("The youngest user is born in the year",most_recent)
        common= int(df['Birth Year'].mode()[0])
        print("Most users are born in the year",common)


    print("\nComputed in %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):

    while True:
        response=['yes','no']
        choice= input("Would you like to look through individual trip data (5 entries)? Type 'yes' or 'no'\n").lower()
        if choice in response:
            if choice=='yes':
                start=0
                end=5
                data = df.iloc[start:end,:9]
                print(data)
            break     
        else:
            print("Kindly enter a correct response")
    if  choice=='yes':       
            while True:
                choice_2= input("Would you like to look through more trip data? Type 'yes' or 'no'\n").lower()
                if choice_2 in response:
                    if choice_2=='yes':
                        start+=5
                        end+=5
                        data = df.iloc[start:end,:9]
                        print(data)
                    else:    
                        break  
                else:
                    print("Kindly enter a correct response")              


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to start afresh? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
