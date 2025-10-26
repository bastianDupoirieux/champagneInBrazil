import os
import yaml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

url_for_appellation_search = 'www.google.fr'
base_str_for_google_search = """Cahier des charges de l'appellation d'origine contrôlée
                                « <nom_de_l_appellation> » \"pdf\""""

def main(driver:webdriver, appellations:list):
    """

    :param driver:
    :param appellations:
    :return:
    """

    #open google
    driver.get(url_for_appellation_search)

    #reject cookies
    reject_cookies = driver.find_element(By.XPATH, '//*[@id="W0wltc"]/div')
    reject_cookies.click()



