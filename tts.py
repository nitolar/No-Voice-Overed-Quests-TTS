from PIL import ImageGrab
from time import sleep
from gradio_client import Client as g_Client
from multiprocessing import Process, Pipe, Value
from keyboard import is_pressed
import easyocr, os, yaml, pyttsx3, ctypes, signal, psutil, win32api, subprocess
with open('settings.yaml', 'r') as file:
    settings = yaml.full_load(file)

def wait_for_input(conn1, conn2, search):
    print("Wait for input | ON")
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
                    print("Input detected")
                    sleep(settings['auto-sleep'])
                    search.value = 1
                a = win32api.GetKeyState(0x01)
                if a != state_left: # It fucking works!!!
                    state_left = a
                    if a < 0:
                        print("Input detected")
                        sleep(settings['auto-sleep'])
                        search.value = 1
                    else:
                        pass

        if is_pressed(settings['key']):
            if settings['mode'] == 'key':
                print("Input detected")
                search.value = 1
                sleep(1)
            elif settings['mode'] == 'auto':
                if val == 0:
                    print("Turned on auto mode")
                    val = 1
                    sleep(1)
                elif val == 1:
                    print("Turned off auto mode")
                    val = 0
                    sleep(1)

        if is_pressed(settings['exit-key']):
            print("Turning off")
            os.kill(p2_pid, signal.SIGTERM)
            os.kill(p1_pid, signal.SIGTERM)
        
def main(search):
    reader = easyocr.Reader(['en'], settings['use-gpu'], verbose=False) 
    if settings['use-ai'] == True:
        client = g_Client(settings['gradio'])
    engine = pyttsx3.init()
    print("MAIN | ON")
    print(f"Script is running! \nYour action key is: {settings['key']} \nYour exit key is: {settings['exit-key']}")
    if settings['mode'] == 'auto':
        print(f"Your ranning script in auto mode. You need to press your action key to start the script!")
    while True:
        if search.value == 1:
            search.value = 0
            print("MAIN | START")
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
            options_l: list = reader.readtext('tmp/op.png', detail = 0)
            print(f"Options: {options_l}") # ['Claim Daily Commission Reward', 'Claim Adventure Rank Rewards', 'Dispatch Character on Expedition', 'We meet again, Katheryne.', 'Are you also a clockwork puppet,', 'Katheryne?', 'See you:']
            name_l: list = reader.readtext('tmp/name.png', detail = 0)
            print(f"Name: {name_l}") # ['Katheryne', "Receptionist, Adventurers' Guild"]
            text_l: list = reader.readtext('tmp/text.png', detail = 0)
            print(f"Text original: {text_l}") # ["See you:", 'Katheryne', "Receptionist, Adventurers' Guild", "Ad astra abyssosque! Welcome to the Adventurers' Guild."]
            for i in name_l:
                if i in text_l:
                    text_l.remove(i)
            for i in options_l:
                if i in text_l:
                    text_l.remove(i)
            c = 0
            for i in text_l:
                text_l[c] = i.replace('__', '...')
                text_l[c] = i.replace('_', '.')
                text_l[c] = i.replace('$', 's')
                text_l[c] = i.replace(':', '.')
                c += 1
            print(f"Text final: {text_l}") # ["Ad astra abyssosque! Welcome to the Adventurers' Guild."]
            
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
                    print("No voice found")
                    if settings['no-voice'] == True:
                        if settings['default-voice'] == None:
                            print("Using pyttsx3 \nPlaying sound")
                            engine.say(' '.join(text_l))
                            engine.runAndWait()
                        else:
                            with open(f, 'r') as file:
                                print("Setting voice to default")
                                with open(f"voices/{settings['default-voice'].replace('.yaml', '')}.yaml", 'r') as file:
                                    model = yaml.full_load(file)
                if model != None:
                    print(f"Voice found. Using: {model['Model']}")
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
                    print("Playing sound")
                    subprocess.call(["ffplay", "-loglevel", "quiet", "-nodisp", "-autoexit", result[-1].replace('\\', '\\\\')]) # no playsound because some files have weird bitrate and it won't play lol
            else:
                print("Playing sound")
                engine.say(' '.join(text_l))
                engine.runAndWait()
            
            print("MAIN | STOP")
    
if __name__ == "__main__":
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
        print("Admin mode is required to detect key presses! Please run as administrator and try again.")
        quit()