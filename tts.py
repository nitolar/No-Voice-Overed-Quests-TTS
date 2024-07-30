from PIL import ImageGrab
from time import sleep
from gradio_client import Client as g_Client
from multiprocessing import Process, Pipe, Value
from keyboard import is_pressed, press, release
from fuzzywuzzy import fuzz
import easyocr, os, yaml, pyttsx3, ctypes, signal, psutil, win32api, subprocess
with open('settings.yaml', 'r') as file:
    settings = yaml.full_load(file)

"""COLORS"""
CEND     = '\33[0m'
CBLACK   = '\33[30m'
CRED     = '\33[31m'
CGREEN   = '\33[32m'
CYELLOW  = '\33[33m'
CBLUE    = '\33[34m'
CVIOLET  = '\33[35m'
CBEIGE   = '\33[36m'
CWHITE   = '\33[37m'
CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

def wait_for_input(conn1, conn2, search):
    print(CBEIGE2 + "Wait for input | ON" + CEND)
    val = 0
    p1_pid = conn2.recv()
    p2_pid = conn1.recv()
    psutil.Process(p1_pid).nice(psutil.BELOW_NORMAL_PRIORITY_CLASS) # Lowers process priority
    psutil.Process(p2_pid).nice(psutil.BELOW_NORMAL_PRIORITY_CLASS) # Lowers process priority
    state_left = win32api.GetKeyState(0x01)
    while True:
        if settings['mode'] == 'auto':
            if val == 1:
                if is_pressed("space"):
                    print(CYELLOW2 + "Input detected" + CEND)
                    sleep(settings['auto-sleep'])
                    search.value = 1
                a = win32api.GetKeyState(0x01)
                if a != state_left: # It fucking works!!!
                    state_left = a
                    if a < 0:
                        print(CYELLOW2 + "Input detected" + CEND)
                        sleep(settings['auto-sleep'])
                        search.value = 1
                    else:
                        pass

        if is_pressed(settings['key']):
            if settings['mode'] == 'key':
                print(CYELLOW2 + "Input detected" + CEND)
                search.value = 1
                sleep(1)
            elif settings['mode'] == 'auto':
                if val == 0:
                    print(CBLUE + "Turned on auto mode" + CEND)
                    val = 1
                    sleep(1)
                elif val == 1:
                    print(CBLUE + "Turned off auto mode" + CEND)
                    val = 0
                    sleep(1)

        if is_pressed(settings['exit-key']):
            print(CRED + "Turning off" + CEND)
            os.kill(p2_pid, signal.SIGTERM)
            os.kill(p1_pid, signal.SIGTERM)
        
def main(search):
    reader = easyocr.Reader(['en'], settings['use-gpu'], verbose=False) 
    if settings['use-ai'] == True:
        client = g_Client(settings['gradio'])
    engine = pyttsx3.init()
    print(CBEIGE2 + "MAIN | ON" + CEND)
    print(f"{CGREEN2}Script is running! {CBLUE}\nYour action key is: {settings['key']} \nYour exit key is: {settings['exit-key']}{CEND}")
    if settings['mode'] == 'auto':
        print(f"{CGREEN2}Your ranning script in auto mode. You need to press your action key to start the script!{CEND}")
    while True:
        if search.value == 1:
            search.value = 0
            print(CBEIGE2 + "MAIN | START" + CEND)
            if os.path.exists("tmp/") == False:
                os.mkdir("tmp/")
            """GET IMG"""
            if settings['game'] == "gs":
                name = ImageGrab.grab(bbox =(700, 830, 1230, 925))
            elif settings['game'] == "hsr":
                name = ImageGrab.grab(bbox =(700, 790, 1230, 860))
            text = ImageGrab.grab(bbox =(200, 780, 1880, 1040))
            options = ImageGrab.grab(bbox =(1260, 380, 1880, 850))
            name.save("tmp/name.png")
            text.save("tmp/text.png")
            options.save("tmp/op.png")
            
            """GET NAME AND TEXT"""
            if settings['alt-tab'] == True:
                press("alt")
                sleep(0.2)
                press("tab")
                sleep(0.2)
                release("tab")
                sleep(0.2)
                release("alt")
            options_l: list = reader.readtext('tmp/op.png', detail = 0, paragraph=True)
            print(f"Options: {options_l}") # ['Claim Daily Commission Reward', 'Claim Adventure Rank Rewards', 'Dispatch Character on Expedition', 'We meet again, Katheryne.', 'Are you also a clockwork puppet,', 'Katheryne?', 'See you:']
            name_l: list = reader.readtext('tmp/name.png', detail = 0)
            print(f"Name: {name_l}") # ['Katheryne', "Receptionist, Adventurers' Guild"]
            text_l: list = reader.readtext('tmp/text.png', detail = 0, paragraph=True)
            print(f"Text original: {text_l}") # ["See you:", 'Katheryne', "Receptionist, Adventurers' Guild", "Ad astra abyssosque! Welcome to the Adventurers' Guild."]
            print(CGREEN + "All: " + ' '.join(name_l) + CEND)
            for i in name_l:
                if ' '.join(name_l) in text_l:
                    print(CBLUE2 + f"1Del: {' '.join(name_l)}" + CEND)
                    text_l.remove(' '.join(name_l))
            for i in name_l:
                for ii in text_l:
                    if fuzz.ratio(ii, i) >= 80:
                        print(CBLUE2 + f"2Del: {ii}" + CEND)
                        text_l.remove(ii)
            if len(name_l) >= 2:
                print(CGREEN + f"0 1: {name_l[0]} {name_l[1]}" + CEND)
                print(CGREEN + f"0 -1: {name_l[0]} {name_l[-1]}" + CEND)
                for i in text_l:
                    if fuzz.ratio(f"{name_l[0]} {name_l[1]}", i) >= 90:
                        print(CBLUE2 + f"3.1Del: {name_l[0]} {name_l[1]}" + CEND)
                        text_l.remove(f"{i}")
                    elif fuzz.ratio(f"{name_l[0]} {name_l[1]}", i) >= 90:
                        print(CBLUE2 + f"3.2Del: {name_l[0]} {name_l[-1]}" + CEND)
                        text_l.remove(f"{i}")
            try:
                print(CGREEN + f"startswith1: {name_l[0]} {name_l[1]}" + CEND)
                print(CGREEN + "startswith2: " + name_l[0] + CEND)
                print(CGREEN + "startswith3: " + name_l[1] + CEND)
                if text_l[0].startswith(f"{name_l[0]} {name_l[1]}"):
                    print(CBLUE2 + f"4.1Del: {name_l[0]} {name_l[1]}" + CEND)
                    text_l[0] = text_l[0][len(name_l[0]) + 1 + len(name_l[1]):]
                elif text_l[0].startswith(name_l[0]):
                    print(CBLUE2 + f"4.2Del: {name_l[0]}" + CEND)
                    text_l[0] = text_l[0][len(name_l[0]):]
                elif text_l[0].startswith(name_l[1]):
                    print(CBLUE2 + f"4.2Del: {name_l[1]}" + CEND)
                    text_l[0] = text_l[0][len(name_l[1]):]
            except Exception: # List empty lol
                pass   
            for i in options_l:
                if i in text_l:
                    print(CBLUE2 + f"5Del: {i}" + CEND)
                    text_l.remove(i)
            for i in options_l:
                for ii in text_l:
                    if fuzz.ratio(ii, i) >= 80 or fuzz.ratio(ii, i[-len(ii):]) >= 80:
                        print(CBLUE2 + f"6Del: {ii}" + CEND)
                        text_l.remove(ii)
            c = 0
            for i in text_l:
                text_l[c] = text_l[c].replace('__', '...')
                text_l[c] = text_l[c].replace('-_', '...')
                text_l[c] = text_l[c].replace('_-', '...')
                text_l[c] = text_l[c].replace('_.', '...')
                text_l[c] = text_l[c].replace('ooo', '...') # It’s rare to have three "o"s in a row, but it can sometimes happen ¯\_(ツ)_/¯. Better than having three "o"s at the end of a word.
                text_l[c] = text_l[c].replace('.=', '...')
                text_l[c] = text_l[c].replace('_', '.')
                text_l[c] = text_l[c].replace(':', '.')
                text_l[c] = text_l[c].replace(';', '.')
                text_l[c] = text_l[c].replace('|', 'I')
                text_l[c] = text_l[c].replace('[', 'I')
                text_l[c] = text_l[c].replace('$', 's')
                text_l[c] = text_l[c].replace('0f', 'of')
                text_l[c] = text_l[c].replace('0t', 'of')
                text_l[c] = text_l[c].replace('Tve', 'I\'ve')
                text_l[c] = text_l[c].replace('Tll', 'I\'ll')
                text_l[c] = text_l[c].replace('Tm', 'I\'m')
                text_l[c] = text_l[c].replace('Td', 'I\'d')
                c += 1
            print(f"Text final: {text_l}" + CEND) # ["Ad astra abyssosque! Welcome to the Adventurers' Guild."]
            
            if not text_l:
                print(CRED + "No text was found" + CEND)
                if settings['alt-tab'] == True:
                    press("alt")
                    sleep(0.2)
                    press("tab")
                    sleep(0.2)
                    release("tab")
                    sleep(0.2)
                    release("alt")
                print(CBEIGE2 + "MAIN | STOP" + CEND)
                continue
            
            if settings['use-ai'] == True:
                """MODEL LOADING"""
                model = None
                for model_ in os.listdir('voices/'):
                    f = os.path.join('voices/', model_)
                    if os.path.isfile(f):
                        if f.endswith(".yaml"):
                            try:
                                if model_.replace('.yaml', '') == name_l[0] or model_.replace('.yaml', '') == f"{name_l[0]} {name_l[1]}":
                                    with open(f, 'r') as file:
                                        model = yaml.full_load(file)
                                    break
                            except IndexError:
                                pass
                
                """GENE SPEECH"""
                if model == None:
                    print(CBEIGE2 + "No voice found" + CEND)
                    if settings['no-voice'] == True:
                        if settings['default-voice'] == None:
                            print(CBEIGE2 + "Using pyttsx3 \nPlaying sound" + CEND)
                            engine.say(' '.join(text_l))
                            engine.runAndWait()
                        else:
                            with open(f, 'r') as file:
                                print(CBEIGE2 + "Setting voice to default" + CEND)
                                with open(f"voices/{settings['default-voice'].replace('.yaml', '')}.yaml", 'r') as file:
                                    model = yaml.full_load(file)
                if model != None:
                    print(CBEIGE2 + f"Voice found. Using: {model['Model']}" + CEND)
                    result = client.predict(
                        model['Model'],	# str 'Model' Dropdown component
                        model['Speed'],	# int | float (numeric value between -100 and 100) in 'Speech speed (%)' Slider component
                        ' '.join(text_l),	# str in 'Input Text' Textbox component
                        model['Voice'], # str 'Voice' Dropdown component
                        model['Transpose'],	# int | float in 'Transpose (the best value depends on the models and speakers)' Number component
                        model['PEM'],	# str in 'Pitch extraction method (pm: very fast, low quality, rmvpe: a little slow, high quality)' Radio component
                        model['Index'],	# int | float (numeric value between 0 and 1) in 'Index rate' Slider component
                        model['Protect'],	# int | float (numeric value between 0 and 0.5) in 'Protect' Slider component
                        fn_index=0
                        )
                    if settings['alt-tab'] == True:
                        press("alt")
                        sleep(0.2)
                        press("tab")
                        sleep(0.2)
                        release("tab")
                        sleep(0.2)
                        release("alt")
                    print(CYELLOW + "Playing sound" + CEND)
                    subprocess.call(["ffplay", "-loglevel", "quiet", "-nodisp", "-autoexit", result[-1].replace('\\', '\\\\')]) # No `playsound` because some files have unusual bitrates and won't play lol
            else:
                print(CYELLOW + "Playing sound" + CEND)
                engine.say(' '.join(text_l))
                engine.runAndWait()
            
            print(CBEIGE2 + "MAIN | STOP" + CEND)
    
if __name__ == "__main__":
    os.system("") # To make colors always work
    if ctypes.windll.shell32.IsUserAnAdmin():
        value = Value("i", 0)
        conn1, conn2 = Pipe()
        p1 = Process(target=wait_for_input, args=(conn2, conn1, value))
        p2 = Process(target=main, args=(value,))
        p1.start()
        p2.start()
        conn1.send(p2.pid)
        conn2.send(p1.pid)
    else:
        print(CRED + "Admin mode is required to detect key presses! Please run as administrator and try again." + CEND)
        quit()