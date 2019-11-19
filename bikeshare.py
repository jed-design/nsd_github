import time
import pandas as pd
import numpy as np
import datetime as dt

# **************** List of CSV files **********************************************************
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# ***********************************************************************************************

"""	Displays statistics on the most popular stations and trip.
	The columns in the data frame  is:
	['Start Time', 'End Time', 'Trip Duration', 'Start Station',
       'End Station', 'User Type', 'Gender', 'Birth Year']  """

# ***********************************************************************************************
rawdata = "on"   # this is a switch that is used for showing raw data. It can be set to "on" or "off".
# ***********************************************************************************************


def raw_data_switch():  	# this function switches on and off the viewing of raw data. Default is on.
    global rawdata 		# creates the (global) variable "rawdata". 
    if rawdata == "on":		# Check if rawdata is on or not	
        s = "1"			# If it is, set "s" to 1
    elif rawdata == "off":	# 	
        s = "0"			# If not; s = 0	
    if s == "1":		# If rawdata is "on", s = 1. So rawdata must be switched to "off"
        rawdata = "off"		#
    elif s == "0":		# If rawdata was off, it is now switched on!
        rawdata = "on"		#
 
    selector(df)
# ***********************************************************************************************

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # set global variables
    global city
    global month
    global day
    global num
    global df
    


    # TO DO: get user input for city (chicago, new york city, washington). 
	# HINT: Use a while loop to handle invalid inputs
	
    print("+" + "-"*78)
    print('Hello! Let\'s explore some US bikeshare data!')
    print("Choose your city. \nType the number for the City you want below.")
    print("Chicago = 0")
    print("New York City = 1")
    print("Washington = 2")
    cities = ['chicago', 'new york city', 'washington']	
    num = input("Select your city: ")
	
	#  Checking if the input value is valid. First is what happen if it is not.
    while num not in ['0', '1' ,'2']:   	
        print("You had one task; Type 0, 1 or 2. Nothing else. \n -Try again")
        num = input("Select your city: ")
    else: 
        city = cities[int(num)]				# this picks the city from the list a few lines up here...
        df = pd.read_csv(CITY_DATA[city])   # This picks the .csv file for the city.

    # TO DO: get user input for month (all, january, february, ... , june)
	# We first state a list of valid inputs. 
    list_of_months = ['all', 'january', 'februry', 'mars', 'april', 'may', 'june']

    print("\nNow, type the month you want. Choose from januari to june.")	   # instruktion of wath to input.
    print("You can also choose to watch results from all months. Then, type all: \n")
    month = input("Type the month: ").lower()		

	# Check loop to if the value is valid. If it is not, the user have to make a new try.
    while month not in list_of_months:			
        print("You better type a valid month! Try again: \n")
        month = input("Type the month: ").lower()
    else:
        print("You selected month: ", month)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
	# First we make a list of all valid values.
    list_of_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
	
    print("\nNow, type the Day of the Week you want. Choose from sunday to saturday.")
    print("You can also choose to watch results from whole week. Then, type all: \n")
    day = input("Type the Day of the Week: ").lower()

	# While loop that checks if the inputde value is valid.
    while day not in list_of_days:
        print("Please type a valid day! Try again: \n")
        day = input("Type the Day of the Week: ").lower()
    else:
        print("You selected day :", day)
    
    day = day.title()  # fix big letter in front of dayname.

	# Print a little message to the user to of what is seleted. 
    print("+" + "-"*78)
    print("+")
    print("+  You have selected: ", city, "-",  month,  "-",  day)
    print("+")
    print("+" + "-"*78)
    return city, month, day

def load_data(city, month, day):
    """ ************************************************************************
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    ************************************************************************ """
	# We shall do some way to pick the correct csv, correct month and day from the csv.
    pd.read_csv(CITY_DATA[city])
	
	# now, we limit the DataField to only contain values from the selected month 
	# and day, if not all is selected.
	# We change the "Start time" into datetime format and make a new column, csv_month with
	# month. This is used for filtering.
	
    df['Start Time'] = pd.to_datetime(df['Start Time'])		#time convertion 
    df['End Time'] = pd.to_datetime(df['End Time']) 		#time convertion     
    df['csv_month'] =  df['Start Time'].dt.month    # create a new column with the month
	
	# **************************************************************************
        
	# If month is all, this filering is skipped. All months that is not selected
	# will be droped. So it is an inversed seletion - toss all that is not selected
    if month != 'all':
        # We need a number for the month. The number is given from the position in the list. 
        month_list = ['january', 'februry', 'mars', 'april', 'may', 'june']
        month_index = month_list.index(month) + 1 	# get a number from the list correponding to month
        months_to_drop = df.loc[df['csv_month'] != month_index].index   # making a list of rows to drop
        df.drop(months_to_drop, inplace=True)   # drop the rows	
   
    df['day_of_week'] = df['Start Time'].dt.weekday_name   # make a column with weekdays
		
    # Filtering the days. All days that are not selected will be dropped.
    if day != 'All':
        days_to_drop = df.loc[df['day_of_week'] != day].index # listing the row lines of days to drop
        df.drop(days_to_drop, inplace=True)   
    
    return df

	
def time_stats(df):
    """	****************************************************************************
	Displays statistics on the most frequent times of travel. 
	If "all" has been chosen for month and/or day, the most popular is shown.
	Also, the most common start time is shown.
	Before we do anythng else, we change the time format of the df to time stamp.	
	**************************************************************************   """
	
    df['Start Time'] = pd.to_datetime(df['Start Time'])		#time convertion 
    df['End Time'] = pd.to_datetime(df['End Time'])      	#time convertion 
	
    print('\nCalculating The Most Frequent Times of Travel...')
    print("." + "."*78)
	
    start_time = time.time()  # this is start time for a timer to check processing time.
	
    # TO DO: display the most common month. This is for obvious reasons only done if _all_ months has been choosen.
    df['month'] = df['Start Time'].dt.month  # we make this new month column anyway. Might be nice to have
    if month == 'all':
        month_names = ['January', 'Februry', 'Mars', 'April', 'May', 'June']
        popular_month = df['month'].value_counts().idxmax()  # this picks the most popular month
        popular_month_name = month_names[popular_month - 1]		# this matches the month name with the month number.
        print("Most popular month in {} was: ".format(city) ,popular_month_name)
    else: 
        print("Most popular month: You have choosen to look only in month", month)
	
    # TO DO: display the most common day of week.  This is for obvious reasons only done if _all_ days has been choosen.
    df['day_of_week'] = df['Start Time'].dt.weekday_name  # we make this day_of_week column anyway
	
    if day == 'All':
        popular_day = df['day_of_week'].value_counts().idxmax()	# This picks the moste popular day.
        print("Most poplar day in {} of the week was: ".format(city) ,popular_day)
    else:
        print("Most popular weekday: You have coosen to look only for the weekday", day,  "\n")

    # TO DO: display the most common start hour
    df['hour'] =  df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().idxmax()  # This picks the most popular hour.
    print("Most poplar start hour for you selection was: ", popular_hour)
	
	# *** This shows raw data, if rawdata switch is "on"
    if rawdata == "on":
        print("."*78)
        print("\n Some Raw Data: \n", df.head(7), "\n")  # print 7 raws of raw data
        print("."*78)
	
	# This below shows how long time it took to proess this function.
    print("-" + "-"*50)
    print("This took %s seconds." % round((time.time() - start_time), 3), "to process.") 
    print("-" + "-"*78)
	
# ******************************************************************************

def station_stats(df):   # calculate statistics regarding stations.
    print("\n")		
    print('Calculating The Most Popular Stations and Trip...')
    print("\n")	
	
    start_time = time.time()  # this is a timer for the proess

    # TO DO: display most commonly used start station
    pop_start_station = df['Start Station'].value_counts().idxmax()  # this picks the most popular start station
    print("Most popular start-station: ", pop_start_station)
	
    # TO DO: display most commonly used end station
    pop_end_station = df['End Station'].value_counts().idxmax() # this picks the most popular end station
    print("Most popular End-station: ", pop_end_station)

    # TO DO: display most frequent combination of start station and end station trip
	# NOTE: Start Time is used to count the trips. If 2 trips starts at the same time, the calculation may be faulty!
	
	# first we gruop the combnations of start and end stations and count their occurenses.
    df_top_freq = df.groupby(['Start Station', 'End Station'])['Start Time'].count().reset_index(name='qty')
	# Below: sortng the new qty-value and get the higest, most popular.
    df_top_sorted = df_top_freq.sort_values('qty', ascending=False).head(1)

    print("The most frequent combination of start station and end station is : \n", df_top_sorted, "\n")
    if rawdata == "on":
        print("."*78)
        print("Some Raw Data: \n", df.head(7), "\n")  # print 7 raws of raw data
        print("."*78)	
    print("This took %s seconds." % round((time.time() - start_time), 3), "to process")  # Showing process time
	
    selector(df)

def trip_duration_stats(df):
	""" *******************************************************************************
	Displays statistics on the total and average trip duration.
	******************************************************************************* """
	print('Calculating Trip Duration...')
	
	start_time = time.time()  # This is for the proess timer.

	df['trip_time'] =  df['End Time'] - df['Start Time']  # trip time is the timelength for the trip. As timedelta.

	# TO DO: display total travel time. Sum of travel time.
	sum_time = df['trip_time'].sum()
	print("Sum of all time for all the selected trips: ", sum_time)

	# TO DO: display mean travel time. 
	mean_time = df['trip_time'].mean()  # The internal "mean" function is used for the mean time
	print("The mean time for a trip in the selected interval was: ", mean_time)
	if rawdata == "on":
		print("."*78)
		print("\n Some Raw Data: \n", df.head(7), "\n")  # print 7 raws of raw data
		print("."*78)
	print("This took %s seconds." % round((time.time() - start_time), 3), "to process.")  # this is the procesing time.
	
	selector(df)
    
def user_stats(df):
    """ ***********************************************************************
	**** Displays statistics on bikeshare users.
	**** user information is not pressent in the washinton.csv file	  
	*********************************************************************	"""
    print("-"*78)	
    print('Calculating User Stats...')
	
    start_time = time.time()  # this is the process timer.

    # TO DO: Display counts of user types. 
    user_types = df['User Type'].value_counts()  # gets the types of users. 
    print("User types:   Counts:")
    print(user_types.to_string() )   # we print this as a string as it looks better on the screen.
	
    # TO DO: Display earliest, most recent, and most common year of birth
	# make user data into timestamp. Sort after years up and down. Count the years and get the most common. 
	# Note: Gender and Birth Date is not aviable in washington.csv file

    if num == "2":
        print("You have selected city {}  for witch there is no Birth Year or Gender data are aviable.".format(city))
    else:
        df_new = df['Birth Year']		# we make a new data frame for the Birth Year
        df_new.dropna(inplace=True)		# we drop all Null and empty values
        df_new = df_new.astype('int64')	# we set the typ tp int64. Very handy!

        # TO DO: Display counts of gender. Modify the one above.
		# We count how many travellers of each gender. 
		# Transvestites are just among the others.
        genders = df['Gender'].value_counts()
        print("Genders:   Counts:")
        print(genders.to_string())	

        most_common = df_new.value_counts().idxmax()	# get the most common birth year.
        most_common_qty = df_new.value_counts().max()	# get the how many from that years who are travellers.

        # First, the most reasent = the youngest
        year_resent = df_new.sort_values(ascending=False).head(1).to_string()
        print("The most resent Birth Year is: ", year_resent[-4:])
        # Next: the earliest year = the oldest
        year_early = df_new.sort_values(ascending=True).head(1).to_string()
        print("The most early Birth Year is: ", year_early[-4:])
        print("Most common year is: ", most_common, "with", most_common_qty, "occurrences")
		
        print("This took %s seconds." % round((time.time() - start_time), 3), "to process")  # This is the counter
        print("\n")
        print("+" + "="*78)
	
    if rawdata == "on":
        print("."*78)
        print("\n Some Raw Data: \n", df.head(7), "\n")  # print 7 raws of raw data
        print("."*78)
		
    selector(df)
	
# ***********************************************************************************************

# This is the selector menue. It is called up from several places below

# ***********************************************************************************************
	
def selector(df):
	# ********* Menu to choose from **************************************
	print("="*78)
	print(" *** MENU - Select one by typing the number! ***")
	print("."*60)
	print(" 1 - Times. When does people travel and trip duration.")
	print(" 2 - Stations. Popular Start and End stations")
	print(" 3 - User Stats. Who is the users?")
	print(" 4 - Switch the raw-data viewing on/off. Now it is", rawdata,".")
	print(" 5 - Restart and choose another data selection")
	print(" 6 - Stop the program")
	print("."*78)

	selector_list = ["1", "2", "3", "4", "5", "6" ]

	select = input("Select from the menu: ")

	while select not in selector_list:
		print("\n Your selection was not in the menu.")
		select = input("Please try again, from the menu: ")
	else:
		if select == "1":
			time_stats(df)	        # running the time stats
			trip_duration_stats(df)   # also showing trip duration as this is time related.
		elif select == "2":
			station_stats(df)         # shows info about stations
		elif select == "3":
			user_stats(df)            # shows info about users
		elif select == "4":
			raw_data_switch()         # runs the raw-data switch
		elif select == "5":                 
			main()   			 # start from scratch with new values
		else:                                       # this is what happens if nummer 6 is selected. 
			exit()                                  # stops the program execution

# ******************************************************************************

def main():
    while True:
        city, month, day = get_filters()  # runs the first script that picks up user selections
        df = load_data(city, month, day)	# runs the script that load the data from the file 
        selector(df)  # runs the menu function
        print("\n")	
        restart = input('Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()
