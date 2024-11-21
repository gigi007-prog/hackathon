import datetime
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
        if self.stress_lv <= 3:
            print("Your stress levels are quite low. Here are some things that we might recommend:")
        elif 3< self.stress_lv <=6:
            print("Your stress levels are slightly elevated. Here are some things that we might recommend:")
        elif 6< self.stress_lv<=10:
            print("Your stress levels are quite high maybe it's time you relax and here are some of our recommendations:")
        else:
            print("The stress level you entered is invalid please enter how stressed you are from 0 to 10")

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
                age = int(input("Please enter your age here:"))
                break
            except ValueError:
                print("You have entered an invalid number for age")
        stress_lv= int(input("Please enter how stressed you feel at the moment from the scale of 0-10:"))
        return cls(name, age, stress_lv) #returns the class itself and is usually used in @classmethod refers to a classs and not an instance 
    

stress_assessement=StressAssessement.info_from_input() #collects the input and creates the StressAssessement object
stress_assessement.information() #displayes the logged info


#connecting this to the sql database in pgAdmin first create a database and table there 
# then create virtual environment
# install psycopg2
# import psycopg2
# def connect_to_db():
#     """Connect to the PostgreSQL database."""
#     try:
#         conn = psycopg2.connect(
#             dbname="your_database",
#             user="your_username",
#             password="your_password",
#             host="localhost",  # or your database host
#             port="5432"        # default PostgreSQL port
#         )
#         print("Connected to the database successfully!")
#         return conn
#     except Exception as e:
#         print("Failed to connect to the database:", e)
#         return None