import PySimpleGUI as sg
from web_driver import *
import random
import time
import threading

projectName = 'JKLM.fun-Bot'
words = str(open('dict.txt', 'r').read()).split('\n')
    
layout = [[sg.Text('Current Status: Not Running', key='_STATUS_')],
          [sg.Text('JKLM Room Code:'), sg.Input(key='_LINK_'), sg.Button('GO')],
          [sg.Button('Start Bot'), sg.Button('Stop Bot')]
        ]
window = sg.Window(projectName, layout, resizable=True)
runBot = False
botRunning = False


def realisticTyping(word: str, maxDelay: int):
    #max delay is in milliseconds

    inputElement = driver.find_element(By.XPATH, '// input[@autocorrect="off"]')

    for a in range(len(word)):
        delay = random.randint(0, maxDelay)/1000

        time.sleep(delay)
        inputElement.send_keys(word[a])
    
    inputElement.send_keys(Keys.ENTER)


def bot():
    global runBot, botRunning, words
    botRunning = True

    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)

    while runBot == True:
        turn = driver.find_element(By.CLASS_NAME, 'selfTurn')
        if turn.get_attribute("hidden") == None:
            syllable = driver.find_element(By.CLASS_NAME, "syllable").text

            potential_words = []
            for a in range(len(words)):
                if syllable.lower() in words[a].lower():
                    potential_words.append(words[a].lower())
            
            word = random.choice(potential_words)

            try:
                realisticTyping(word, 221)
            except:
                print('fuck')
        
        time.sleep(.5)
    
    botRunning = False


while True:
    event, values = window.read()
    if event == "GO":
        driver.get(f"https://jklm.fun/{values['_LINK_']}")

    elif event == "Start Bot":
        window.Element('_STATUS_').update('Current Status: Running')
        runBot = True
        try:
            threading.Thread(target=bot).start()
        except:
            botRunning = False
            window.Element('_STATUS_').update('Current Status: Not Running')
            driver.switch_to.default_content()

    elif event == "Stop Bot":
        driver.switch_to.default_content()
        window.Element('_STATUS_').update('Current Status: Not Running')
        runBot = False
        botRunning = False

    if event == sg.WIN_CLOSED:
        break

driver.quit()
window.close()