# Just playing with code . This code is experimental and may contain bugs. Bunch of stupid funtion and code just for fun
import os
import pyautogui
import numpy as np
import time
import win32gui
import win32con
import time
import pyperclip
# Constants
# WAIT_DICT = {
#     'whatsapp_open': 5,
#     'smile_wait': 1,
#     'prompt_write': 4,
#     'respose_wait': 6,
#     'max_try':3
# }


# Configuration
# WHATSAPP_PATH = r'C:\Program Files\WindowsApps\5332543A.WhatsAppDesktop_2.2450.6.0_x64__sdgasdrewgase\WhatsApp.exe'
# CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
# PLATFORM = 'WhatsApp Desktop' 
# # PLATFORM = 'WhatsApp Web'

# theme='dark' # 'dark'

chatgpt_icon = 'icons/chatgpt_icon.png'
upload_logo = f'./icons/attach_windows_{theme}.png' if PLATFORM == 'WhatsApp Desktop' else f'./icons/attach_web_{theme}.png'




first_time=True
old_chatgpt_x, old_chatgpt_y, old_smile_x, old_smile_y, old_coords = None, None, None, None, None




def find_window_by_title(partial_title):
    """Find a window whose title contains the given partial string."""
    def window_enum_callback(hwnd, result):
        window_text = win32gui.GetWindowText(hwnd)
        if partial_title.lower() in window_text.lower():
            result.append(hwnd)
    
    windows = []
    win32gui.EnumWindows(window_enum_callback, windows)
    return windows[0] if windows else None

def bring_window_to_foreground(hwnd):
    """Bring the specified window to the foreground."""
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore if minimized
    win32gui.SetForegroundWindow(hwnd)

def focus_whatsapp_tab():
    """Focus the WhatsApp Web tab in Chrome."""
    hwnd = find_window_by_title("WhatsApp")
    if hwnd:
        # Bring the Chrome window with WhatsApp to the foreground
        bring_window_to_foreground(hwnd)
        time.sleep(1)  # Wait for the window to come to the foreground
        
        # Simulate a mouse click on the tab bar or send Ctrl+Tab
        pyautogui.hotkey('ctrl', '1')  # Assumes WhatsApp Web is the first tab
        return True
    return False





def open_whatsapp():
    """Open WhatsApp based on the platform."""
    global first_time
    if PLATFORM == 'WhatsApp Desktop':
        os.system(f'start "" "{WHATSAPP_PATH}"')
        if first_time:
            time.sleep(WAIT_DICT['whatsapp_open'])
            first_time=False
        else:
            time.sleep(2)
    elif PLATFORM == 'WhatsApp Web':
        import webbrowser
        webbrowser.open("https://web.whatsapp.com")
        webbrowser.get(CHROME_PATH).open("https://web.whatsapp.com")
        time.sleep(15)
        # if focus_whatsapp_tab():
        #     print("WhatsApp Web tab is now in focus.")
        # else:
        #     import webbrowser
        #     webbrowser.open("https://web.whatsapp.com")
        #     webbrowser.get(CHROME_PATH).open("https://web.whatsapp.com")
        #     time.sleep(15)
        


def button_location(icon_path, confidence=0.7):
    try:
        # Locate the icon on the screen
        icon_location = pyautogui.locateOnScreen(icon_path, confidence=confidence)
        if icon_location:
            # Get the center point of the located icon
            x, y = pyautogui.center(icon_location)
            return x, y
        else:
            print(f"Icon '{icon_path}' not found on the screen.")
            return (None, None)
    except Exception as e:
        print(f"Error finding icon '{icon_path}': {e}")
        return (None, None)



    
def copy_response(x,y):
    # Copy the response to the clipboard
    pyautogui.click(x, y)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    print("Response copied to clipboard")
    chtgpt_answer = pyperclip.paste()
    print(chtgpt_answer)
    return chtgpt_answer
    
    
    
    
def chatGPT(prompt):
    """Generate chatgpt response based on the prompt."""
    max_try = WAIT_DICT['max_try']
    global old_chatgpt_x, old_chatgpt_y, old_smile_x, old_smile_y, old_coords
    # Detect and click the Meta logo to open the chatbox
    for i in range(max_try):
        chatgpt_x, chatgpt_y = button_location(chatgpt_icon)
        if chatgpt_x is not None and chatgpt_y is not None:
            break
    old_chatgpt_x, old_chatgpt_y = chatgpt_x, chatgpt_y
    if chatgpt_x is None or chatgpt_y is None:
        print('ChatGPT Icon not found')
        try:
            pyautogui.click(old_chatgpt_x, old_chatgpt_y)
            print('Clicked on the old ChatGPT icon')
        except:
            # exit()   
            return   
    else:
        pyautogui.click(chatgpt_x, chatgpt_y)
        print('Clicked on the ChatGPT icon')
    
    
    
    
    # Clear the chatbox
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'x')
    print('Cleared the chatbox')
    # Type the prompt and send it 
    # pyautogui.typewrite(prompt)
    pyperclip.copy(str(prompt))
    pyautogui.hotkey('ctrl', 'v')
    print('Typed the prompt')
    print(f'Sleeping for {WAIT_DICT["prompt_write"]} seconds')
    time.sleep(WAIT_DICT['prompt_write'])
    pyautogui.press('enter')
    print('Sent the prompt')
    print(f'Sleeping for {WAIT_DICT["respose_wait"]} seconds')
    time.sleep(WAIT_DICT['respose_wait'])
    
    #find x,y for rectangle
    for i in range(max_try):
        next_x, next_y = button_location(upload_logo)
        if next_x is not None and next_y is not None:
            old_smile_x, old_smile_y = next_x, next_y
            break
    
    if next_x is None or next_y is None:
        if old_smile_x is not None and old_smile_y is not None:
            print('Upload logo not found')
            print('Using the old coordinates')
            x, y = old_smile_x, old_smile_y
        print('Upload logo not found')
    else:
        x, y = next_x, next_y
    result=copy_response(x,y-95)
    return result
from microsoft_tts import edge_tts_pipeline
import shutil
import re 
from lang_data import languages
import simpleaudio as sa
import speech_recognition as sr

def tts(text,Language='English',Gender='Female',speed=1.0,translate_text_flag=False, no_silence=True, long_sentence=True,tts_save_path=''):
    voice_name=None
    text=text.strip()
    text=text.replace('\n',' ')        
    edge_save_path = edge_tts_pipeline(text, Language,voice_name, Gender, translate_text_flag=translate_text_flag, 
                                        no_silence=no_silence, speed=speed, tts_save_path=tts_save_path, 
                                        long_sentence=long_sentence)
    return edge_save_path


def notification_sound(fname="okay.wav"):
    filename=f"./notification/{fname}"
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()






def remove_emojis(text):
    # This regex pattern matches all emoji characters
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F700-\U0001F77F"  # Alchemical Symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed Characters
        "]+", 
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def play_audio(text,Language='English'):
    filename='temp.wav'
    text=remove_emojis(text)
    tts_path=tts(text,Language=Language,tts_save_path=filename)
    print(tts_path) 
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    
def main(input_lang="English"):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 2000
    recognizer.pause_threshold = 1
    recognizer.phrase_threshold = 0.1
    recognizer.dynamic_energy_threshold = True
    calibration_duration=1
    timeout=10
    phrase_time_limit=None
    while True:	
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
                print("Listening...")
                notification_sound()
                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                MyText =recognizer.recognize_google(audio_data,language=languages[input_lang])
                prompt = MyText.lower()
                print("Recognized text: "+prompt)
                reply=chatGPT(prompt)
                if reply:
                    play_audio(reply,Language=input_lang)            
                else:
                    print("No reply from ChatGPT") 
        except Exception as e:
            print("Error: "+str(e))
            continue


WAIT_DICT = {
    'whatsapp_open': 5,
    'smile_wait': 1,
    'prompt_write': 4,
    'respose_wait': 6,
    'max_try':3
}
WHATSAPP_PATH = r'C:\Program Files\WindowsApps\5332543A.WhatsAppDesktop_2.2450.6.0_x64__sdgasdrewgase\WhatsApp.exe'
CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
theme='dark' # 'dark'
PLATFORM = 'WhatsApp Desktop' #'WhatsApp Web'
theme='dark' # 'light'
input_lang = "English"
open_whatsapp()
main(input_lang)
