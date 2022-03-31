import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze from a predefined set of values.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        try:
            city = str(input("\nWhich city do you want to take a loot at:\n Chicago, Washington or New York City?: ")).lower()
        except ValueError:
            print("\nnot a valid input - try again\n")
            continue
        if city not in ("chicago","new york city","washington"):
            print("\nnot a valid input - try again\n")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input("\nWhich month do you want to analyse?\nChose all or a month between January and June: ")).lower()
        except ValueError:
            print("\nnot a valid input - try again\n")
            continue
        if month not in ("all","january","february","march","april",\
                        "may","june"):
            print("\nnot a valid input - try again\n")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input("\nWhich day of the week do you want to analyse?\nChose all or one day between monday and sunday: ")).lower()
        except ValueError:
            print("not a valid input - try again\n")
            continue
        if day not in ("all","monday","tuesday","wednesday","thursday",\
                        "friday","saturday","sunday"):
            print("\nnot a valid input - try again\n")
        else:
            break

    print('-'*40)
    return city,month,day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df.query(f"month == {month}")

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.query(f'day_of_week == "{day.capitalize()}"')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(f"most common month : {df['month'].mode()[0]}\n")
    # display the most common day of week
    print(f"most common day of the week : {df['day_of_week'].mode()[0]}\n")
    # display the most common start hour
    max_hour=df['Start Time'].dt.hour.mode()[0]
    print(f"most common start hour : {max_hour}\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"most commonly used start station: {df['Start Station'].mode()[0]}\n")
    # display most commonly used end station
    print(f"most commonly used end station: {df['End Station'].mode()[0]}\n")
    # display most frequent combination of start station and end station trip
    max_combo=df.groupby(['Start Station','End Station']).size().idxmax()
    print(f"most commonly used combination of start and end station:\nstart: '{max_combo[0]}' & end: '{max_combo[1]}' \n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time=df["Trip Duration"].sum()
    print(f"total travel time: {tot_travel_time}\n")
    # display mean travel time
    mean_travel_time=df["Trip Duration"].mean()
    print(f"mean travel time: {mean_travel_time}\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nCounts of different user types:\n")
    print(df[["User Type","Start Time"]].groupby("User Type").count().rename(columns={'Start Time':'Count'}))

    # Display counts of gender
    print("\nAnalyzing gender distribution of users:\n")
    try:
        d=df[["Gender","Start Time"]].groupby("Gender").count().rename(columns={'Start Time':'Count'})
        print("\nGender distribution of users:\n")
        print(d)

    except Exception:
        print("Data on gender and date of birth of users not present in chosen dataset.\nGoing to next step.")


    # Display earliest, most recent, and most common year of birth
    print("\nAnalyzing year of birth data of users:\n")
    try:
        earliest=int(df["Birth Year"].min())
        most_recent=int(df["Birth Year"].max())
        most_common=int(df["Birth Year"].mode()[0])
        print(f"Earliest year of birth: {earliest}")
        print(f"Most recent year of birth: {most_recent}")
        print(f"Most common year of birth: {most_common}")

    except Exception:
        print("Data date of birth of users not present in chosen dataset.\nWrapping up analysis now.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    '''Displays raw data if user wishes'''
    while True:
        try:
            answer = str(input("\nWould you like to see the raw data used in the analysis?: ")).lower()
        except ValueError:
            print("\nnot a valid input - try again\n")
            continue
        if answer not in ("yes","no"):
                print("\nnot a valid input - try again\n")
        else:
            break

    if answer == "yes":
        count1=0
        count2=5
        print(df.iloc[count1:count2])
        while True:
            try:
                more = str(input("\nWould you like to see more raw data?: ")).lower()
            except ValueError:
                print("\nnot a valid input - try again\n")
                continue
            if more not in ("yes","no"):
                print("\nnot a valid input - try again\n")
            elif more == "yes":
                count1+=5
                count2+=5
                print(df.iloc[count1:count2])
            else:
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = str(input('\nWould you like to restart? Enter yes or no.\n')).lower()

        if restart.lower() != 'yes':
            print("\nProgram will be stopped now.")
            break


if __name__ == "__main__":
	main()
