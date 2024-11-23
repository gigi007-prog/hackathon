import psycopg2
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
                    INSERT INTO stress_levels (name, age, stress_level, date_todays)
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
            dbname='stress_levels',
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

