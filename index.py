import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

import json

import threading
import random
import time

# Read config file
JSON_CONFIG = open('config.json')
data = json.load(JSON_CONFIG)

email = data["emails"]
password = data["passwords"]
stream = data["stream_links"]
phrases = data["phrases"]


def openChannel(stream_link, email, password):
    browser = webdriver.Firefox()
    browser.get("https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    time.sleep(2)
    print("--- Opened browser to login ---")
    email_box = browser.find_element(By.ID, 'identifierId')
    email_box.send_keys(email)
    next_btn_email = browser.find_element(By.CLASS_NAME, "VfPpkd-vQzf8d")
    next_btn_email.click()
    time.sleep(2)
    password_box = browser.find_element(By.CLASS_NAME, "whsOnd")
    password_box.send_keys(password)
    next_btn_pass = browser.find_element(By.CLASS_NAME, "VfPpkd-vQzf8d")
    next_btn_pass.click()
    print("--- Logged in ---")
    time.sleep(2)
    browser.get(stream_link)
    print("--- Channel loaded ---")
    time.sleep(4)
    browser.switch_to.frame(browser.find_element(By.TAG_NAME, "iframe"))

    def sendMessage():
        wait = WebDriverWait(browser, 10)
        chat_box = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div#input.style-scope.yt-live-chat-text-input-field-renderer.style-scope.yt-live-chat-text-input-field-renderer")))
        message = random.choice(phrases)
        chat_box.send_keys(message)
        send_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'yt-icon-button.style-default > button:nth-child(1)')))
        send_button.click()
        print("\n--- Message Sent: " + message + " ---")
        threading.Timer(1, sendMessage).start()

    sendMessage()


for i in range(0, len(email)):
    openChannel(stream, email[i], password[i])

input('\nPress ENTER to exit')
