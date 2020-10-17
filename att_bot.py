from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import schedule
from datetime import date, timedelta, time, datetime
from time import sleep

from secret import friends, service_date, check


class AttBot():
    def __init__(self, username, pw, service_type):
        print("Opening browser...")
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.username = username
        self.pw = pw
        self.service_type = service_type
        self.error = False

    def login(self, count=0):
        print("Accessing login page...")
        self.driver.get("https://att.lmu.edu.ng/log/login")
        sleep(2)

        if count < 5:
            try:
                print("Trying to login "+self.username+"...")
                uname = self.driver.find_element_by_xpath("//*[@id='name']")
                uname.send_keys(self.username)

                password = self.driver.find_element_by_xpath(
                    "//*[@id='content-inner']/div/div/form/fieldset/div[2]/input")
                password.send_keys(self.pw)

                submit = self.driver.find_element_by_xpath(
                    "//*[@id='content-inner']/div/div/form/fieldset/input[1]")
                submit.click()
                try:
                    login_error = self.driver.find_element_by_xpath(
                        "//*[@id='content-inner']/div/div/form/fieldset/div[1]/div")
                    if login_error.text == "Wrong Username or Password!":
                        print("Wrong Username or Password!")
                        self.error = True
                except:
                    print("Logged in successfully")
                    count = 0
                    self.error = False
            except:
                print("Couldn't login "+self.username+" trying again...")
                self.error = True
                self.login(count+1)
        else:
            print("We tried to login "+self.username+" 5times but it failed")
            self.error = True

    def book(self, count=0):
        print("Automating "+self.username+" chapel service...")
        self.driver.get("https://att.lmu.edu.ng/check/serveChoice")
        sleep(2)
        if count < 5:
            # Get element with tag name 'tbody'
            tbody = self.driver.find_element_by_tag_name('tbody')

            # Get all the elements available with tag name 'tr'
            tr = tbody.find_elements_by_tag_name('tr')
            confirm = False
            for e in tr:
                tds = e.find_elements_by_tag_name('td')
                for td in tds:
                    if service_date in td.text:
                        confirm = True

            select_error = False
            selects_check = self.driver.find_elements_by_xpath(
                "//*[@id='page']/form/div/div[2]/select")
            for select_check in selects_check:
                if "You have missed Roll Call last week!" in select_check.text:
                    print("You have missed Roll Call last week!")
                    select_error = True
                elif "Chapel Service Closed for the Semester" in select_check.text:
                    print("Chapel Service Closed for the Semester")
                    select_error = True

            if not confirm:
                if not select_error:
                    try:
                        print(
                            "Booking your prefered service, make sure you didn't miss roll call")

                        if self.service_type == "first":
                            service_choice = self.driver.find_element_by_xpath(
                                '//*[@id="page"]/form/div/div[2]/select/option[1]')
                            if "" in service_choice.text:
                                print("First service has ended")
                            else:
                                service_choice.click()
                        else:
                            service_choice = self.driver.find_element_by_xpath(
                                '//*[@id="page"]/form/div/div[2]/select/option[2]')
                            service_choice.click()

                        agree = self.driver.find_element_by_xpath(
                            '//*[@id="confirm_remove_original"]')
                        agree.click()

                        # Wait for the alert to be displayed
                        self.wait.until(expected_conditions.alert_is_present())

                        # Store the alert in a variable for reuse
                        alert = self.driver.switch_to.alert

                        # Press the Cancel button
                        alert.accept()

                        self.driver.find_element_by_css_selector(
                            "input[type='submit']").click()
                    except:
                        print("Couldn't book service for " +
                              self.username+", something went wrong")
                        print("Trying again...")
                        self.book(count+1)
                    else:
                        print("Automatation was successful for " + self.username +
                              " check it booked the prefered service")
            else:
                print("You have booked chapel service already")
        else:
            print("We tried to book service " +
                  self.username+" 5times but it failed")

    def logout(self):
        self.driver.get("https://att.lmu.edu.ng/log/logout")
        sleep(2)


# def main_task():
# if check():
for friend in friends:
    bot = AttBot(friend["username"], friend["pw"], friend["service_type"])
    bot.login()
    if bot.error == False:
        bot.book()
        bot.logout()
    bot.driver.close()
# else:
#     print("Can't not book chapel service now")

# schedule.every().tuesday.at("18:00").do(main_task)
# schedule.every().wednesday.do(main_task)
# schedule.every().thursday.do(main_task)

# while True:
#     schedule.run_pending()
#     sleep(1)
