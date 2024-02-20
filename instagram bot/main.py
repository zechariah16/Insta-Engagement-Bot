from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time
from selenium.common.exceptions import ElementClickInterceptedException

instagram_username = os.environ.get("instagram_username")
instagram_password = os.environ.get("instagram_password")
SIMILAR_ACCOUNT = os.environ.get("SIMILAR_ACCOUNT")
URL = "https://www.instagram.com/"


#we are creating a class to hold our details

class InstaFollower:

    def __init__(self):
        self.chrome_option = webdriver.ChromeOptions()
        self.chrome_option.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(self.chrome_option)

    def login(self):
        self.driver.get(URL + "accounts/login/")
        time.sleep(4)
        # Check if the cookie warning is present on the page
        decline_cookies_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]"
        cookie_warning = self.driver.find_elements(By.XPATH, decline_cookies_xpath)
        if cookie_warning:
            # Dismiss the cookie warning by clicking an element or button
            cookie_warning[0].click()

        username = self.driver.find_element(By.NAME, value='username')
        password = self.driver.find_element(By.NAME, value='password')

        username.send_keys(instagram_username)
        password.send_keys(instagram_password, Keys.ENTER)

        time.sleep(6)
        # Click "Not now" and ignore Save-login info prompt
        save_login_prompt = self.driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Not now')]")
        time.sleep(4)
        if save_login_prompt:
            save_login_prompt.click()

        time.sleep(5)
        # Click "not now" on notifications prompt
        notifications_prompt = self.driver.find_element(by=By.XPATH, value="// button[contains(text(), 'Not Now')]")
        if notifications_prompt:
            notifications_prompt.click()

    def find_follower(self):
        time.sleep(5)
        # Show followers of the selected account.
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/followers")

        time.sleep(5.5)
        # The xpath of the modal that shows the followers will change over time. Update yours accordingly.
        modal_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]"
        modal = self.driver.find_element(by=By.XPATH, value=modal_xpath)
        for i in range(10):
            # In this case we're executing some Javascript, that's what the execute_script() method does.
            # The method can accept the script as well as an HTML element.
            # The modal in this case, becomes the arguments[0] in the script.
            # Then we're using Javascript to say: "scroll the top of the modal (popup) element by the height of the modal (popup)"
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(3)

    def follow(self):
        # Check and update the (CSS) Selector for the "Follow" buttons as required.
        time.sleep(4)
        all_button = self.driver.find_elements(By.CSS_SELECTOR, value='._aano button')

        for buttons in all_button:
            try:
                time.sleep(1)
                buttons.click()
                time.sleep(2)
                # Clicking button for someone who is already being followed will trigger dialog to Unfollow/Cancel
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Cancel')]")
                cancel_button.click()



bot = InstaFollower()
bot.login()
bot.find_follower()
bot.follow()
