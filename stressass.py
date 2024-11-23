import requests
import random
import time
import sys
import os
import psycopg2
import datetime
from entertainment_rec_functions import *
from config import *
from terminal_effects import *

clear_terminal()
print(datetime.date.today())

print('Hello this is an app which will help you deal with your stress and anxiety ')
print('We will ask you a few questions on your stress/anxiety levels and moods')

#we will also ask the users age, name to make this appp more personalized

#create an input of rate your stress level from 0-10 
# stress level rates *idea so far*
# 0-3 low stress levels for this you can give a recommendation something simple like drinking tea watching movie eating favorite food blah blah
#4-6 medium stress levels that you can suggest a video for meditation or a meditation technique
#7-10 very high stress level you should make multiple suggestion to as because this is the highest stress/anxiety level so something like breathing technique some othe rmore serious remedies

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

        # ----------
        if self.stress_lv < 0 or self.stress_lv > 10:
                print("Although times can be stressful and make it hard to focus, please input a number between  0 - 10 so we can provide proper help.")

        elif self.stress_lv == 0:
            # They're officially stress free, nice message and maybe recommendation
            pass

        elif self.stress_lv <=3:
            # Low stress - Goal: light entertainment to relax further
            print("Hey there! It seems like you might need a little boost. Let's make your day a bit brighter! I have three great suggestions for you:\n\t1 - Watch a relaxing movie to unwind\n\t2 - Listen to some calming music to lift your spirits\n\t3 - Try a fun recipe for some therapeutic cooking\n")

            suggest_entertainment = True
            something_else = True

            while suggest_entertainment == True:
                entertainment_selection = (input("Which one sounds good to you? Please type `movie`, `music`, or `recipe` to choose!\n"))

                if entertainment_selection == "movie":
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

                elif entertainment_selection == "music":
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

                elif entertainment_selection == "recipe":
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

        elif self.stress_lv <=6:
            # Medium stress level, suggest a video for meditation or a meditation technique
            breathing_exercises()

        elif self.stress_lv <=9:
            # Very high stress level. Make multiple suggestion as this is the highest stress/anxiety level. Something like breathing technique or some other more serious remedies
            pass

        elif self.stress_lv == 10:
            # Super high, suggestions and tell to talk to someone or write things down.
            pass

    @classmethod 
    #@classmethod for Input:
    #Allows creating an object from user input and validates the data during instantiation.
    def info_from_input(cls): #okay so i have to look this up but cls is not like self it refers to the class itself allows the method to create and return a new instance of the class.
        '''
        Basically the input itself and 
        '''
        name = input("Please enter your name here:")
        #will start the while loop so it ensures that the data is correct and if its not it will ask the user for the correct data until he enters the correct data
        while True:
            try: #this is used a lot for input validation to check whether its acceotable or not 
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
    
    #connecting the information to postgresql 
    def save_in_sql(self, conn): #conn used to connect python and sql together and is basically 'connection'
        '''
        will save the stress levels and other details on the sql database
        '''
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO stress_lvs (name, age, stress_lv, date_todays)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (self.name, self.age, self.stress_lv, datetime.date.today())
                )#inserts into the table these values
                conn.commit()
        except Exception as e:# e is a variable holds the exception object and it contains information about what went wrong while trying to save the data to sql
            conn.rollback()#a method that will undo all changes made to the database in the case of an error

def sql_connection():
    '''
    will connect to postgresql
    '''
    try: 
        connection= psycopg2.connect(
            dbname='stress_lvs',
            user='gigi',
            password='1234',
            host='localhost',
            port='5432')
        return connection

    except Exception as e:#same as in the save_in_sql we use the same notion but without the rollback
        return None    


#the function to run the program cause who wants to waste code lines 

def the_program():
    '''
    runs the whole thing
    '''
    connection= sql_connection()
    if connection:
        stress_assessment = StressAssessement.info_from_input()  # Collect user input
        stress_assessment.information()  # Display recommendations
        stress_assessment.save_in_sql(connection)  # Save to the database
        connection.close()


if __name__ == "__main__": #used to make sure that only a specific block of code runs only
    the_program()    

