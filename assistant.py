import speech_recognition as sr
import pyttsx3
import webbrowser
import wolframalpha
import cv2
import numpy as np
import pyautogui
import time
import requests

flag = False

# Speech engine initialization
engine = pyttsx3.init()
#voices = engine.setProperty('voice', voices[0].id) # 0 = male, 1 = female
activationWords = ['hey', 'bob']

#Wolframalpha client
appID = '7RQU72-HP85QHAQ7K'
wolframClient = wolframalpha.Client(appID)

#Uses text to speech to allow the computer to 'speak'
def speak(text, rate = 150):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

# Configruing Browser
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))

#Uses the speech recognition library to 'understand' what you said
def parseCommand():

    #This code uses the speech recgonition library to use the microphone to begin listning
    listener = sr.Recognizer()
    print('Listening for command')

    #This code says listens to what is said by using the micrphone
    with sr.Microphone() as source:
       listener.pause_threshhold = 2
       listener.energy_threshold = 4000
       input_speech = listener.listen(source)

    try:
        print("Reconizing speech....")
        query = listener.recognize_google(input_speech, language='en-US')
        print(f'The input speech was: {query}')

    except Exception as exception:
        print(exception)
        return 'None'
    
    return query


def search(text):
    time.sleep(3)
    speak("Searching")
    try:
        # Load the target image
        target_image = cv2.imread('search.PNG')
        target_image = cv2.cvtColor(target_image, cv2.COLOR_RGB2BGR)

        # Capture a screenshot of the screen
        screen_image = pyautogui.screenshot()
        screen_image = cv2.cvtColor(np.array(screen_image), cv2.COLOR_RGB2BGR)

        # Perform template matching
        result = cv2.matchTemplate(screen_image, target_image, cv2.TM_CCOEFF_NORMED)

        # Define a threshold for matching
        threshold = 0.7
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # Get the center coordinates of the matched regions
        center_coordinates = []
        for loc in locations:
            top_left = loc
            bottom_right = (top_left[0] + target_image.shape[1], top_left[1] + target_image.shape[0])
            center_x = ((top_left[0] + bottom_right[0])-100) // 2
            center_y = (top_left[1] + bottom_right[1]) // 2
            center_coordinates.append((center_x, center_y))

        # Print the center coordinates
        for coordinates in center_coordinates:
            print(f"Center coordinates: {coordinates}")
        
        pyautogui.click(center_x, center_y)

        time.sleep(0.2)

        for char in text:
            pyautogui.typewrite(char)
            time.sleep(0.01)
        
        pyautogui.press('enter')

    except:
        speak("Couldnt search")

def listOrDict(var):
    if isinstance(var, 'list'):
        return var[0]['plaintext']
    else:
        return var['plaintext']
    
def openThings(app):
    global flag
    pyautogui.press('win')
    
    try:
        for char in app:
            pyautogui.typewrite(char)
            time.sleep(0.01)

    except Exception as exception:
        print(exception)
        return 'None'
    
    pyautogui.press("enter")
    flag = True

def search_wolframalpha(query):
    url = f"https://api.wolframalpha.com/v1/spoken?appid={appID}&i={query}%3f"
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        spoken_result = response.text
        speak(spoken_result)
    else:
        speak("Unable to fetch spoken result.") 

def find_repeated_indices(lst, word):
    indices = []
    for i, item in enumerate(lst):
        if item == word:
            indices.append(i)
    return indices

# Main loop
if __name__ == '__main__':
    #current_time = datetime.now().time()
    #speak(f"Greetings Kalpa, the time is currently {current_time.strftime('%H:%M')}")

    # Parse the command as a list by listening to keywords
    while True:
        #This will split the sentence said by me into a list of words
        query = parseCommand().lower().split()

        if activationWords[0] in query and activationWords[1] in query:
            hey = query.index('hey')
            bob = query.index('bob')

            if query[hey + 1] == 'bob':
                query = query[bob:]
                query.pop(0)
                print(f"The command is {query}")

                queryBackup = query
                
                try:
                    num_of_ands = query.count('and') + 1
                    print(f"THe number of ands are in query is: {num_of_ands-1}")
                except:
                    print("No ands in query")

                a = 0
                while a < num_of_ands:
                    print("Started running while loop")
                    if 'and' in query:
                        and_pos = [i for i, x in enumerate(query) if x == 'and']
                        print(f"The positiob of ands: {and_pos}")
                        print(query)
                        
                        filtered_query = query[0: and_pos[0]] #open dovg and do this
                        print(f"{a+1} command running: {filtered_query}")
                            
                    else:
                        print("Running last command")
                        filtered_query = query
                        print(f"Filtered query is: {filtered_query}")
                        
                        

                    # Navigation
                    if 'go' in filtered_query and 'to' in filtered_query:
                        print(f"Query at the start of go_to function: {filtered_query}")
                        go_pos = filtered_query.index('go')
                        to_pos = filtered_query.index('to')

                        if go_pos < to_pos:
                            app = filtered_query[go_pos + 1:to_pos]
                            speak("Going to...")
                            website = "".join(filtered_query[to_pos + 1:])
                            if '.' not in website:
                                website += '.com'
                            print(f"The website is: {website}")
                            webbrowser.get('brave').open_new(website)
                        
                    if 'open' in filtered_query: 
                        print("Opening...")
                        if 'and' in filtered_query:
                            filtered_query2 = list(filter(lambda word: word != 'open', filtered_query))
                            print(f"Query after all opens have been removed: {filtered_query2}")

                            filtered_query2 = [word for word in filtered_query2 if word != 'and']
                            print(f"after all ands removed: {filtered_query2}")

                            i = 0
                            print(len(filtered_query2))
                            while i < len(filtered_query2): #While i is smaller than the number of ands
                                flag = False
                                app = filtered_query2[i] #it will get the words between the ands
                                print(f"App currently opening: {app}")

                                while not flag:
                                    speak(f"Opening {app}")
                                    openThings(app)
                                    
                                i += 1

                        else:
                            open = filtered_query.index('open')
                            app = filtered_query[open + 1:]  
                            speak("Opening...")
                            openThings(app)
                        
                    if 'search' in filtered_query:
                        search_pos = filtered_query.index('search')
                        filtered_query3 = filtered_query[search_pos + 1: ]
                        print(f"What is being searched on yt: {filtered_query3}")
                        filtered_query3 = ' '.join(filtered_query3)
                        search(filtered_query3)

                    #Wolframalpha
                    if 'compute' in filtered_query:
                        compute_pos = filtered_query.index('compute')
                        filtered_query = filtered_query[compute_pos: ]
                        print(f"Filtered query wolframalpha: {filtered_query}")                
                        filtered_query = '+'.join(filtered_query)
                        print(f"Searching this: {filtered_query}")
                        result = search_wolframalpha(filtered_query2)

                    try:
                        query = query[and_pos[0] + 1:]
                        print(f"setnece after removing and: {query}")
                    except: print("no more ands after executing command")
                    a += 1

            