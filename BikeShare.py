import time
import pandas as pd
import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


MONTH = ["all", "january", "february", "march", "april", "may", "june"]

DAY = [
    "all",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    # Get user input for city (chicago, new york city, washington).
    while True:
        city = input("Choose City- Chicago, New York City or Washington: ").lower()
        if city.lower() not in CITY_DATA:
            print("Check spelling, try again")
        else:
            break

    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "Choose Month- all, or january, february, march, april, may, june: "
        ).lower()
        if month not in MONTH:
            print("Check spelling, try again")
        else:
            break

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "Choose Day- all, monday, tuesday, wednesday, thursday, friday, saturday, sunday: "
        ).lower()
        if day not in DAY:
            print("Check spelling, try again")
        else:
            break

    print("-" * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month

    df["day_of_week"] = df["Start Time"].dt.weekday_name

    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month)+1
        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()
    # extract hour from the Start Time column to create an hour column
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    # extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["hour"] = df["Start Time"].dt.hour
    df["day"] = df["Start Time"].dt.day

    # Display the most common month
    popular_month = df["month"].mode()[0]
    print("\nMost Frequent Month:", popular_month)

    # Display the most common day of week
    popular_day = df["day"].mode()[0]
    print("\nMost Frequent Day:", popular_day)

    # Display the most common start hour
    popular_hour = df["hour"].mode()[0]
    print("\nMost Frequent Hour:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # Display most commonly used start station
    popular_station = df["Start Station"].value_counts().idxmax()
    print("\nMost Common Start Station:", popular_station)

    # Display most commonly used end station
    popular_end_station = df["End Station"].value_counts().idxmax()
    print("\nMost Common End Station:", popular_end_station)

    # Display most frequent combination of start station and end station trip
    popular_start_end_station = (
        df.groupby(["Start Station", "End Station"]).size().idxmax()
    )
    print(
        "\nMost Common combination of Start and End Stations:",
        popular_start_end_station,
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Display total travel time
    trip_duration = df["Trip Duration"].value_counts()
    print("\nTotal Travel Time: ", trip_duration)

    # Display mean travel time
    average_duration = df["Trip Duration"].mean()
    print("\nAverage Travel Time: ", average_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_type = df["User Type"].value_counts()
    print("\nCount of User Types: ", user_type)

    # Display counts of gender
    try:
        gender = df["Gender"].value_counts()
        print("\nCount of genders: ", gender)
    except KeyError:
        print("Gender Data Unavailable")

    # Display earliest year of birth
    try:
        earliest_birth = df["Birth Year"].min()
        print("\nEarliest Birth Year: ", earliest_birth)

        # Display most recent year of birth
        recent_birth = df["Birth Year"].max()
        print("\nMost Recent Birth Year: ", recent_birth)

        # Display most common year of birth
        common_birth = df["Birth Year"].value_counts().idxmax()
        print("\nMost Common Birth Year: ", common_birth)
    except KeyError:
        print("Birth Year Data Unavailable")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def display_data(df):
    """Displays 5 lines of raw data."""
    view_data = input('\nWould you like to view the first 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while True:
        if view_data.lower() != "yes":
            break
        print(df.iloc[start_loc:start_loc +5])
        start_loc += 5
        view_data = input('Do you wish to see the next 5 rows?: Enter yes or no.\n ')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
