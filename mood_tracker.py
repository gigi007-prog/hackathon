import json
from datetime import datetime 

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