# Import Packages
import time
import pandas as pd
import numpy as np

# Define File Dictionary
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Create dictionaries 
month_numbers = {"january": "1", "february": "2", "march": "3", "april": "4", "may": "5", "june": "6"}
                 #"july": "7", "august": "8", "september": "9", "october": "10", "november": "11", "december": "12"}
day_numbers = {"monday": "1", "tuesday": "2", "wednesday": "3", "thursday": "4", "friday": "5", "saturday": "6", "sunday": "7"}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Create Input Variables
    city_input = None
    month_input = None
    day_input = None
    filter_input = None
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city_input not in CITY_DATA.keys():
        city_input = input("From which city would you like to see some data? ").lower()
        if city_input != None and city_input not in CITY_DATA.keys():
            print("It appears your selection is invalid. Please choose one of the following cities:" + str(list(CITY_DATA.keys())))

    # Ask user for time filter
    filter_options = ['month', 'day', 'none']
    
    while filter_input not in filter_options:
        filter_input = input('Would you like to apply a filter? Choose "month", "day" or "none": ').lower()
        if filter_input == "month":
            
            while month_input not in list(month_numbers.keys()) + list(month_numbers.values()):
                month_input = input("From which month would you like to see some data? \
                                    Please enter the full name or the number of the specific month: ").lower()
                if month_input not in list(month_numbers.keys()) + list(month_numbers.values()):
                    print("It appears your selection is invalid. Please enter a month name or month number (1-6) until June.")  
                
    
        # get user input for day of week (all, monday, tuesday, ... sunday)
        elif filter_input == "day":
            day_numbers = {"monday": "1", "tuesday": "2", "wednesday": "3", "thursday": "4", "friday": "5", "saturday": "6", "sunday": "7"}
            
            while day_input not in list(day_numbers.keys()) + list(day_numbers.values()):
                day_input = input("From which day would you like to see some data? \
                                  Please enter the full name or the number of the specific day (Monday=1, Sunday=7): ").lower()
                if day_input not in list(day_numbers.keys()) + list(day_numbers.values()):
                    print("It appears your selection is invalid. Please try again.")
        
        elif filter_input == "none":
            continue
        else:
            print('It appears your selection is invalid. Please enter "month, "day" or "none".')

    # Transform input values for filtering
    if day_input is None:
        pass
    elif len(day_input) > 1:
        day_input = int(day_numbers.get(day_input))
    else: 
        day_input = int(day_input)
        
    if month_input is None:
        pass
    elif len(month_input) > 2:
        month_input = int(month_numbers.get(month_input))
    else: 
        month_input = int(month_input)

    print('-'*40)
    return city_input, month_input, day_input, filter_input


def load_data(city_input, month_input, day_input, filter_input):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
        (str) filter - user input for potential filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA.get(city_input))
    
    # Change dtypes
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])   

    
    if filter_input == "month":
        df = df[df["Start Time"].dt.month == month_input]
    elif filter_input == "day":
        df = df[df["Start Time"].dt.weekday  == day_input - 1]    

    return df


def time_stats(df, filter_input):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time() 
    if filter_input == "none":
        print("These are the most common time stats for the entire dataset:")
    else:
        print("These are the most common time stats based on your filters. You filtered on {} level: ".format(filter_input))

    # display the most common month
    most_common_month = df[df.columns[0]].groupby([df["Start Time"].dt.month]).agg('count').idxmax()
    mcm_value = max(df[df.columns[0]].groupby([df["Start Time"].dt.month]).agg('count'))
    mcm_name = list(month_numbers.keys())[list(month_numbers.values()).index(str(most_common_month))].capitalize()
    print("The most common month is: {}. There were a total of {} rentals.".format(mcm_name, mcm_value))

    # display the most common day of week
    most_common_weekday = df[df.columns[0]].groupby([df["Start Time"].dt.weekday]).agg('count').idxmax() + 1
    mcw_value = max(df[df.columns[0]].groupby([df["Start Time"].dt.weekday]).agg('count'))
    mcw_name = list(day_numbers.keys())[list(day_numbers.values()).index(str(most_common_weekday))].capitalize()
    print("The most common weekday is: {}. There were a total of {} rentals.".format(mcw_name, mcw_value))

    # display the most common start hour
    most_common_hr = df[df.columns[0]].groupby([df["Start Time"].dt.hour]).agg('count').idxmax()   
    mch_value = max(df[df.columns[0]].groupby([df["Start Time"].dt.hour]).agg('count'))
    print("The most common hour is: {}h00. There were a total of {} rentals during this particular hour.".format(str(most_common_hr), mch_value))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_freq_start_df = df[['Unnamed: 0']].groupby([df["Start Station"]]).agg('count').sort_values('Unnamed: 0', ascending=False).head(1).reset_index()
    print("Most used start station: \n{} with a total travels of {}.".format(most_freq_start_df['Start Station'][0],\
                                                                                           most_freq_start_df['Unnamed: 0'][0]))
    # display most commonly used end station
    most_freq_end_df = df[['Unnamed: 0']].groupby([df["End Station"]]).agg('count').sort_values('Unnamed: 0', ascending=False).head(1).reset_index()
    print("Most used end station: \n{} with a total travels of {}.".format(most_freq_end_df['End Station'][0],\
                                                                                         most_freq_end_df['Unnamed: 0'][0]))

    # display most frequent combination of start station and end station trip
    most_freq_df = df[['Unnamed: 0', 'Start Station', 'End Station']].groupby(['Start Station', 'End Station']) \
                .agg('count') \
                .sort_values('Unnamed: 0', ascending=False) \
                .head(1) \
                .reset_index()

    print("Most frequent trip: \n{} - {} with a total of {}.".format(most_freq_df['Start Station'][0],\
                                                                                          most_freq_df['End Station'][0],\
                                                                                          most_freq_df['Unnamed: 0'][0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time in the selected period is: {} hours.".format(round((df["Trip Duration"].sum() / 3600),2)))

    # display mean travel time
    print("The mean travel time in the selected period is: {} minutes.".format(round((df["Trip Duration"].mean() / 60),2)))
    
    # Extra number of trips
    print("The total travels in the selected period is: {}".format(df['Unnamed: 0'].nunique()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:    
        # Display counts of user types
        print(df[df.columns[0]].groupby([df["User Type"]]).agg('count')) 
        # Display counts of gender
        print(df[df.columns[0]].groupby([df["Gender"]]).agg('count'))

        # Display earliest, most recent, and most common year of birth
        print("Earliest year of birth: {}".format(str(df['Birth Year'].min()).replace(".0","")))
        print("Most recent year of birth: {}".format(str(df['Birth Year'].max()).replace(".0","")))
        print("Most frequent year of birth: {}".format(str(df[df.columns[0]].groupby([df["Birth Year"]]).agg('count').idxmax()).replace(".0","")))

    except:
        print("The dataset doesn't contain user type, gender or birth year data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city_input, month_input, day_input, filter_input = get_filters()
        df = load_data(city_input, month_input, day_input, filter_input)
        time_stats(df, filter_input)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        else: 
            print("Goodbye!")


if __name__ == "__main__":
	main()
