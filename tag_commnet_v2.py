from random import random
from selenium import webdriver
import random
import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore, Style
import ast
from datetime import datetime
from instaloader import instaloader
# driver
driver = webdriver.Firefox(executable_path='geckodriver.exe')
# import files
accounts = open('accounts.txt').read().split('-')
target_users = open('target_users.txt').read().split(',')
post_link = open('post_link.txt').read().split(',')
# urls
login_url = 'https://instagram.com/'
logout_url = 'https://instagram.com/accounts/logout/'

# sections
username_input = '//input[@name="username"]'
password_input = '//input[@name="password"]'
# login_section = '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button'
comment_button = '//textarea[@aria-label="Add a comment…"]'
comment_section = '//textarea[@aria-label="Add a comment…"]'
send_button = '//button[@data-testid="post-comment-input-button"]'
# Go to Instagram
driver.get(login_url)
os.system('cls')
for account in accounts:
    new_account = ast.literal_eval(account)
    username = new_account.get('username')
    password = new_account.get('password')
    # get to instagram login page
    print(f'{Fore.GREEN} Starting ... {Fore.RESET} \n')
    driver.get(login_url)
    time.sleep(5)
    try:
        # driver.find_element(By.XPATH, username_section).click()
        driver.find_element(By.XPATH, username_input).send_keys(username)
        time.sleep(1.5)
        # driver.find_element(By.XPATH, password_section).click()
        driver.find_element(By.XPATH, password_input).send_keys(
            password + Keys.ENTER)
        time.sleep(15)
        driver.get(login_url+username+'/')
        if f'{username}' in driver.page_source:
            print('Oh... Great!! Your Account is not baned')
            print(
                f"{Fore.GREEN} Loginig with {Fore.YELLOW} {username} | accountNumber = {accounts.index(account) + 1} of {len(accounts)} {Fore.RESET} \n")

            for link in post_link:
                try:
                    print(f'Go to link Address: {link} \n')
                    driver.get(link)
                    time.sleep(1.5)
                    driver.refresh()
                    print(
                        f'{Fore.CYAN} Extracting Followers of Target Users {Fore.RESET} \n')
                    L = instaloader.Instaloader()
                    L.login(username, password)
                    for user in target_users:
                        profile = instaloader.Profile.from_username(
                            L.context, f'{user}')

                        follower_list = []
                        # count = 0

                        for follower in profile.get_followers():
                            follower_list.append(follower.username)
                            if len(follower_list) == 2:
                                break
                    print(f'{Fore.GREEN} Extracting is Done! {Fore.RESET} \n')
                    for user in follower_list:
                        print('Sending Commnet!...')
                        try:
                            driver.find_element(
                                By.XPATH, comment_button).click()
                            time.sleep(0.5)
                            driver.find_element(
                                By.XPATH, comment_section).send_keys(f'@{user} ')
                            time.sleep(1)
                            driver.find_element(By.XPATH, send_button).click()
                            if f'@{user}' in driver.page_source:
                                time.sleep(10)
                                print(
                                    f'{Fore.GREEN} {user} --> Sent Successfuly! -- {datetime.now()}  -- {Fore.RESET} \n')
                                x = random.randint(60, 70)
                                print(f'{str(x)} secound sleeped!... \n')
                                time.sleep(x)
                            else:
                                print(f'{username} is Reaport')
                                continue

                        except:
                            continue
                except:
                    print('Logouting... \n')
                    driver.get(logout_url)
            print('Logouting... \n')
            driver.get(logout_url)
        else:
            print(f'{username} is banned!!')
            driver.get(logout_url)
            continue
    except:
        continue
print('Finished')
driver.quit()
