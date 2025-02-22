import time
import pandas as pd
import numpy as np

""" 
Project: Explore US Bikeshare Data
Author: Brian Black
"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """ 
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filte
    """
    cities = ('chicago', 'new york city', 'washington')
    
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    while True:
        city = input('For which city do you want to see data? \'Chicago\', \'New York City\', \'Washington\'\n').lower()
        if city in cities:
            print('You selected', city.title())
            break
        else:
            print('Invalid response --', city)

    # Initialize variable in case they do not get set below    
    month = 'all'
    day = 'all'
    
    while True:
        filters = ('month', 'day', 'both', 'none')
        filter = input('Do you want to filter the data by month, day, both or not at all? Type \"none\" for no time filter.').lower()

        if filter in filters:
            if filter == 'month' or filter == 'both':
                # Get user input for month (all, january, february, ... , june)
                months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'all')
                while True:
                    month = input('Enter a month from the following - \'Jan\', \'Feb\', \'Mar\', \'Apr\', \'May\', \'Jun\', \'All\'\n').lower()
                    if month in months:
                        print('You selected', month.title())
                        day = 'all'
                        break
                    else:
                        print('Invalid response --', month)
            
            if filter == 'day' or filter == 'both':
                # Get user input for day of week (all, monday, tuesday, ... sunday)
                days = ('m', 't', 'w', 'th', 'f', 'sat', 'sun', 'all')
                while True:
                    day = input('Enter a weekday from the following - \'M\', \'T\', \'W\', \'Th\', \'F\', \'Sat\', \'Sun\', \'All\'\n').lower()
                    if day in days:
                        print('You selected', day.title())
                        break
                    else:
                        print('Invalid response --', day)
                
            if filter == 'none':
                month = 'all'
                day = 'all'
                break
        else:
            print('Invalid response --', filter)
        break   
                        
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load data for selected city
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Add month and day of week as new columns    
    df['month'] = df['Start Time'].dt.month
    df['dayofweek'] = df['Start Time'].dt.dayofweek

    # Filter data by month
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        print('1', month)
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1
        # Filter by month to create the new dataframe
        df = df[df['month']==month]
    
    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        days = ['m', 't', 'w', 'th', 'f', 'sat', 'sun']
        day = days.index(day)
        df = df[df['dayofweek']==day]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    if month == 'all':
        date_pop = df['Start Time'].mode()[0]
        date_pop.isoformat()
    # Gets the month
        m = date_pop.strftime("%B")
        print('The most common month for rentals was:',m)
    else:
        print('The most common month for rentals was: N/A - you already selected the month of ', month.title())

    # Display the most common day of week
    if day == 'all':
        date_pop = df['Start Time'].mode()[0]
        date_pop.isoformat()
    # Gets the day of the week
        d = date_pop.strftime("%A")
        print('The most common day of week for rentals was:',d)
    else:
        print('The most common day of week for rentals was: N/A - you already selected the day as ', day.title())
        
    # Display the most common start hour
    df['st_hr'] = df['Start Time'].dt.hour
    hr_pop = df['st_hr'].mode()[0]
    if hr_pop < 13:
        hr_pop = int(hr_pop)
        AM_PM = 'AM'
    else:
        hr_pop = hr_pop % 12
        hr_pop = int(hr_pop)
        AM_PM = 'PM'
        
    print('The most popular hour to start a trip was:', hr_pop, AM_PM)
    
    # Display run time for the calculation
    run_time = round((time.time() - start_time),6)
    print("\nThis took %s seconds." % run_time)
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_stn = df['Start Station'].mode()[0]
    start_cnt = df['Start Station'].value_counts().get(start_stn,0)
    print ('Most popular start station is',start_stn, 'with', f"{start_cnt:,}",'occurrences.')
    
    # Display most commonly used end station
    end_stn = df['End Station'].mode()[0]
    end_cnt = df['End Station'].value_counts().get(end_stn,0)
    print ('Most popular end station is',end_stn,'with', f"{end_cnt:,}",'occurrences.')

    # Display most frequent combination of start station and end station trip
    start_end_counts = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    max_cnts = start_end_counts.max()
    print ('Most popular start and end station combination is',max_cnts['Start Station'], '&', max_cnts['End Station'],'with', max_cnts['count'],'occurrences.')

    # Display run time for the calculation
    run_time = round((time.time() - start_time),6)
    print("\nThis took %s seconds." % run_time)
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total number of trips in the period
    trips = df['Start Time'].count()
    print('The total number of trips taken in the period was:',f"{trips:,}")
    
    # Display total travel time
    secs =  int(df['Trip Duration'].sum())
    mins = int(secs/60)
    hrs = int(mins/60)
    days = int(hrs/24)

    print('The total trip time was:\n')
    print('    ', f"{secs:,}",'seconds, equivalent to ..')
    print('    ', f"{mins:,}",'minutes, equivalent to ..')
    print('    ', f"{hrs:,}",'hours, equivalent to ..') 
    print('    ', f"{days:,}",'days.')

    # Display mean travel time
    secs =  df['Trip Duration'].mean()
    mins = int(secs/60)
    m_rem = int(secs%60)
    
    print('\nThe mean trip time was:\n')
    print('    ', f"{int(secs):,}",'seconds, equivalent to ..')
    print('    ', f"{mins:,}",'minutes and', f"{m_rem:,}",'seconds.')
 
    # Display run time for the calculation
    run_time = round((time.time() - start_time),6)
    print("\nThis took %s seconds." % run_time)
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    cust_cnt = df['User Type'].value_counts().get('Customer')
    sub_cnt = df['User Type'].value_counts().get('Subscriber')
    print('The count of users by category is as follows:')
    print('     Customers:', f"{cust_cnt:,}")
    print('     Subscribers:', f"{sub_cnt:,}",'\n')

    # Display counts of gender
    try:
        f_users = df['Gender'].value_counts().get('Female')
        m_users = df['Gender'].value_counts().get('Male')
        print('The count of users by gender is as follows:')
        print('     Male:', f"{m_users:,}")
        print('     Female:', f"{f_users:,}",'\n')
    except:
        print('Sorry, user statistics by gender are not available for this city.')
        
    # Display earliest, most recent, and most common year of birth
    try:
        yob_max = df['Birth Year'].max()
        yob_min = df['Birth Year'].min()
        yob_mode = df['Birth Year'].mode().iloc[0]
        print('The profile of user birth years is follows:')
        print('     Earliest year:', int(yob_min)) 
        print('     Most recent year:',  int(yob_max))
        print('     Most common year:',  int(yob_mode))        
    except:
        print('Sorry, user statistics for year of birth are not available for this city.')
    
    # Display run time for the calculation
    run_time = round((time.time() - start_time),6)
    print("\nThis took %s seconds." % run_time)
    print('-'*40)


def show_data(df):
    """Display the raw data 5 lines at a time."""
    
    show_data = input('\nWould you like to display 5 lines of the raw data? Enter yes or no.\n')
    n = 0
    while show_data == 'yes':
        print(df.iloc[n:n+5])
        n += 5
        show_data = input('\nDisplay 5 more lines? Enter yes or no.\n')


def main():
    while True:
        city, month, day = get_filters()
        print('Selection summary: City =', city.title())
        print('                   Month =', month.title())
        print('                   Day =', day.title())
        df = load_data(city.lower(), month.lower(), day.lower())

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in 'yes':
            break

if __name__ == "__main__":
    main()