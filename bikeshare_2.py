import time
import pandas as pd
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities = ['chicago','new york city','washington']
        city = input("\nWhich of these cities would you like to analyze? (Chicago, New York City or Washington):\n").casefold()
        if city in cities:
            break
        else:
            print("Please choose one of the cities stated above")


    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month = input("\nWhich month would you like to analyze? (All, January, February, March, April, May, June:\n").casefold()
        if month in months:
            break
        else:
            print("Please choose one of the month stated or check the bike share data without month filter (all)")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = input("\nWhich day would you like to analyze? (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday:\n").casefold()
        if day in days:
           break
        else:
            print("Please choose one of the days stated or check the bike share data without day filter (all)")

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

    # load data file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time column to datatime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # Extract month and day of the week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']== month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    popular_month = df['month'].mode()[0]

    print('Most Popular Start Month:', popular_month, "\n")

    # display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['day_of_week'] = df['Start Time'].dt.weekday

    popular_day = df['day_of_week'].mode()[0]

    print('Most Popular Start Day:', popular_day, "\n")

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("Most commonly used start station: ", start_station, "\n")

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("Most commonly used end station: ", end_station, "\n")

    # display most frequent combination of start station and end station trip
    df['start_end_comb'] = "From " + df['Start Station'] + " to " + df['End Station']
    start_end_comb = df['start_end_comb'].mode()[0]

    print("Most frequent combination of start station and end station trip:\n", start_end_comb, "\n")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time:", str(datetime.timedelta(seconds=int(total_travel_time))))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Total travel time:", str(datetime.timedelta(seconds=int(mean_travel_time))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:\n", user_types, "\n")

    # Display counts of gender
    if "Gender" in df.columns:
        gender = df['Gender'].value_counts()
        print("Counts of gender:\n", gender, "\n")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest = df['Birth Year'].min()
        print("Oldest customer was born in", earliest, "\n")
        most_recent = df['Birth Year'].max()
        print("Youngest customer was born in", most_recent, "\n")
        most_common = df['Birth Year'].mode()[0]
        print("Average brith year of customers is", most_common, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays raw data upon request"""

    while True:
        answers = ['yes', 'y', 'no', 'n']
        answer = input("Do you want to see raw data? (Yes or No): ").casefold()
        if answer in answers:
            if answer == 'yes' or answer == 'y':
                n = 0
                m = 5
                print(df.iloc[n:m])
            break
        else:
            print("Please answer yes or no")
    if  answer == 'yes' or answer == 'y':
            while True:
                more_answers = ['yes', 'y', 'no', 'n']
                more_answer = input("Do you want to see more raw data? (Yes/y or No/n): ").casefold()
                if more_answer in more_answers:
                    if more_answer == 'yes' or more_answer == 'y':
                        n += 5
                        m += 5
                        print(df.iloc[n:m])
                    else:
                        break
                else:
                    print("Please answer yes or no")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
