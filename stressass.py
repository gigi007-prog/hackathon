import requests
import random
import psycopg2
import datetime
import json
from datetime import datetime 
from entertainment_rec_functions import *
from config import *
from terminal_effects import *

clear_terminal()
print(datetime.now().date())

print('\nHello this is an app which will help you deal with your stress and anxiety\n\nWe will ask you a few questions on your stress/anxiety levels and moods')

#we will also ask the users age, name to make this app more personalized

class StressAssessement:
    def __init__(self,name, age, stress_lv):
        '''
        will initialize the stress assessement object with basic details.
        '''
        self.stress_lv=stress_lv
        self.name =name
        self.age =age 
    
    #im including name and age so it would be easier to store in sql and maybe if the person is really old and has high stress levels you can recommend going to a hospital like fr not joking 
    def information(self):
        '''
        will display the name age and stress level
        '''
        print(f'Entered Details: \n Name {self.name}\n Age {self.age}\n Stress level {self.stress_lv}')

        # Dynamic responses depending on users stress levels

        if self.stress_lv < 0 or self.stress_lv > 10:
                print("Although times can be stressful and make it hard to focus, please input a number between  0 - 10 so we can provide proper help.")

        elif self.stress_lv == 0:
            print("\nYou're feeling great! Keep up the positive vibes. 😊 Maybe treat yourself to something you enjoy today!\n")

        elif self.stress_lv <=6:
            # Low stress - Goal: light entertainment to relax further
            print("\n\nHey there! It seems like you might need a little boost. Let's make your day a bit brighter! I have three great suggestions for you:\n\t1 - Watch a relaxing movie to unwind\n\t2 - Listen to some calming music to lift your spirits\n\t3 - Try a fun recipe for some therapeutic cooking\n")

            suggest_entertainment = True
            something_else = True

            while suggest_entertainment == True:
                entertainment_selection = (input("Which one sounds good to you? Please type `movie`, `music`, or `recipe` (or the corresponding number for each) to choose!\n"))

                if entertainment_selection == "movie" or entertainment_selection == "1":
                    suggest_entertainment = False
                    something_else = True
                    recommend_movies()
                        
                    while something_else == True:
                        something_else_input = input("Would you like a different recommendation? Input 'yes' if so, or anything else if not.")
                        if something_else_input == 'yes':
                            recommend_movies()
                        else:
                            something_else = False
                            print("Looks like you've decided on your movie, enjoy!")

                elif entertainment_selection == "music" or entertainment_selection == "2":
                    suggest_entertainment = False
                    something_else = True
                    get_calming_music()

                    while something_else == True:
                        something_else_input = input("Would you like a different recommendation? Input 'yes' if so, or anything else if not.")
                        if something_else_input == 'yes':
                            get_calming_music()
                        else:
                            something_else = False
                            print("Looks like you've decided on your music, enjoy!")

                elif entertainment_selection == "recipe" or entertainment_selection == "3":
                    suggest_entertainment = False
                    something_else = True
                    suggest_recipe()

                    while something_else == True:
                        something_else_input = input("Would you like a different recommendation? Input 'yes' if so, or anything else if not.")
                        if something_else_input == 'yes':
                            suggest_recipe()
                        else:
                            something_else = False
                            print("Looks like you've decided on your recipe, bon apetit!")
                else:
                    print("Whoops! That wasn't a valid input. Let's try that again.")

        elif self.stress_lv <=9:
            # Medium stress level, suggest a video for meditation or a meditation technique
            breathing_exercises()

        elif self.stress_lv == 10:
            print("\nIt’s okay to feel overwhelmed right now. Remember, you don’t have to face this alone. Talking to someone you trust, like a friend, family member, or a professional, can really help. \n\nWhen you’re ready, let’s try a calming breathing exercise together.\n")
            breathing_exercises()

    @classmethod 
    #@classmethod for Input:
    #Allows creating an object from user input and validates the data during instantiation.
    def info_from_input(cls): #okay so i have to look this up but cls is not like self it refers to the class itself allows the method to create and return a new instance of the class.
        '''
        Basically the input itself and 
        '''
        name = input("Please enter your name here: ")
        #will start the while loop so it ensures that the data is correct and if its not it will ask the user for the correct data until he enters the correct data
        while True:
            try: #this is used a lot for input validation to check whether its acceptable or not 
                age = int(input("Please enter your age: "))
                if 150<= age <= 0:
                    print("Age cannot be zero or negative. Please enter a valid age.")
                    continue
                break
            except ValueError:
                print("You entered an invalid number for age.")
        
        while True:
            try:
                stress_lv = int(input("Please rate your stress level from 0 to 10: "))
                if 0 <= stress_lv <= 10:
                    break
                else:
                    print("Stress level must be between 0 and 10.")
            except ValueError:
                print("You entered an invalid number for stress level.")
        return cls(name, age, stress_lv) #returns the class itself and is usually used in @classmethod refers to a classs and not an instance 
    

    def save_in_sql(self, conn):
        '''
        Saves user details to the PostgreSQL database.
        '''
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO stress_lvs (name, age, stress_level, date_todays)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (self.name, self.age, self.stress_lv, datetime.now().date())
                )
                conn.commit()
                print("Data saved successfully!")
        except Exception as e:
            print(f"Error saving to database: {e}")
            with open("error_log.txt", "a") as log_file:
                log_file.write(f"{datetime.datetime.now()} - Error during INSERT operation: {e}\n")
                log_file.write(f"Attempted data: Name={self.name}, Age={self.age}, Stress Level={self.stress_lv}, Date={datetime.now().date()}\n")
            conn.rollback()



def sql_connection():
    '''
    Establishes connection to PostgreSQL.
    '''
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"{datetime.datetime.now()} - Database connection error: {e}\n")
        return None



#the function to run the program cause who wants to waste code lines 

def the_program():
    '''
    runs the whole thing
    '''
    connection = sql_connection()
    if connection:
        print("\n--- Successfully connected to the database ---\n")
        stress_assessment = StressAssessement.info_from_input()  # Collect user input
        stress_assessment.information()  # Display recommendations
        stress_assessment.save_in_sql(connection)  # Save to the database
        connection.close()


if __name__ == "__main__": #used to make sure that only a specific block of code runs only
    the_program()    




print("In this section we will evaluate your mood ")

# the file that will store the mood
MOOD_FILE = "mood_data.json"

# starting by initializing the JSON file
def json_initialize():
    '''
    will create the json file
    '''
    try:
        with open(MOOD_FILE, "r") as file:
            json.load(file)
    except (FileNotFoundError, json.JSONDecodeError): #if the file doesnt exist and it contains invalid json 
        #data it will create a new file with an empty list
        with open(MOOD_FILE, "w") as file:
            json.dump([], file)


# to add a new mood entry 
def mood_input():
    '''
    input for mood 
    '''
    mood = input("How are you feeling today? Are you happy, sad, angry, etc: ").strip()
    extra = input("Would you like to add anything else, like a note? ").strip()
    timestamp = datetime.now().isoformat()  # Convert datetime object into a string
    
    mood_entry = {"timestamp": timestamp, "mood": mood, "notes": extra}

    #will read whats already in the json file and append it with the input we got
    with open(MOOD_FILE, "r") as file:
        info = json.load(file)
    info.append(mood_entry)

    #saves updated data to the file
    with open(MOOD_FILE, "w") as file:
        json.dump(info, file, indent=5) #indent is used to format the json output with the 
        #indentation of 5 space and provides better readability
    
    print("Mood entry has been added!")


#to view mood history 
def mood_his():
    '''
    View previous moods.
    '''
    with open(MOOD_FILE, "r") as file:
        data = json.load(file)
    
    if not data:
        print("No mood entries found.")
        return
    
    print("\nMood History:")
    for entry in data:
        # Handle old and new key names
        timestamp = entry.get("timestamp") or entry.get("time right now")
        notes = entry.get("notes") or entry.get("details")
        
        if timestamp:
            timestamp = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M:%S")#converting and formatting the recorded timestamps
        else:
            timestamp = "Unknown Time"
        
        mood = entry.get("mood", "Unknown Mood")
        print(f"- {timestamp} | Mood: {mood} | Notes: {notes}")



#making a mood menu to pick if the user wants to see mood history or input more moods
def menu():
    json_initialize()
    while True:
        print("\nMood Tracker Menu:")
        print("\n1. To Add Mood")
        print("\n2. To View Mood History")
        print("\n3. To Exit")

        choose = input("Select the option you want: ").strip()
        if choose=="1":
            mood_input()
        elif choose=="2":
            mood_his()
        elif choose=="3":
            print("Bye thank you for using our app")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()


