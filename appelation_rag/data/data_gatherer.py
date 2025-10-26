import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def _fetch_inao_cdc(driver:webdriver, appellation:str, loading_time = 30, max_tries_to_find_correct_page = 3):
    """
    Private method to download the pdf rulebook for a named appellation off the INAO appellation research page.
    Super redneck engineered, uses a lot of sleep times to map the exact clicking path to download the pdf rulebook.

    Used within the get_multiple_search_results function.
    For the exact steps done, check the inline comments
    :param driver: the selenium webdriver
    :param appellation: the administrative name of the INAO appellation, passed as a string
    :return:
    """
    tries_to_find_correct_page = 1
    #Click track starts on the research page of the INAO website, allowing to search for specific appellations
    wait = WebDriverWait(driver, loading_time)

    #Click on the search bar and enter the appellation name to search for details
    search_bar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="edit-search-api-fulltext--2"]')))
    #search_bar = driver.find_element(By.XPATH, '//*[@id="sb_form_q"]')
    search_bar.send_keys(appellation)
    search_bar.send_keys(Keys.ENTER)

    #When finding the search results, a list of possible appellation rulebooks are clickable.
    #Tries different results multiple times if the given element doesn't work
    while tries_to_find_correct_page <= max_tries_to_find_correct_page:
        wait = WebDriverWait(driver, loading_time)

        result_element=wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id=\"block-views-block-products-search-block-1\"]/div/div/div[3]/div[{tries_to_find_correct_page}]/article/div[1]")))
        result_element.click()
        time.sleep(5)

    #When entering the details page about the appellation, one can open a menu to get to the rulebook.
    # Clicks the button to open this menu
        wait=WebDriverWait(driver, loading_time)
        button_to_open_cdc = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"block-inao-content\"]/article/div/div[4]/div/section[1]/h3/button")))
        button_to_open_cdc.click()
        time.sleep(5)

    #Once the menu is opened, another button must be clicked to find the details of the appellation rulebook.
    # Clicks on this button
        wait = WebDriverWait(driver, loading_time)
        acceder_au_cdc = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"accordion-cdc\"]/div/div/button")))
        acceder_au_cdc.click()
        time.sleep(5)

    #When the details of the appellation rulebook are available, one can click on a link to download the rulebook
    # Click on this button
    #wait = WebDriverWait(driver, loading_time)
        cdc_download_xpath = "//*[@id=\"modal-1-cdc\"]/div/div/div[2]/div/article/div[2]/div/a"
        #download_cdc = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"modal-1-cdc\"]/div/div/div[2]/div/article/div[2]/div/a")))
        try:
            download_cdc = driver.find_element(By.XPATH, cdc_download_xpath)
            download_cdc.click()
            break
        except:
            close_page_xpath = '//*[@id="modal-1-cdc"]/div/div/div[3]/button'
            close_page = driver.find_element(By.XPATH, close_page_xpath)
            close_page.click()
            back_button_xpath = '/html/body/div[1]/div/main/div/div[2]/div/button[1]'
            back_button = driver.find_element(By.XPATH, back_button_xpath)
            back_button.click()
            tries_to_find_correct_page = tries_to_find_correct_page + 1


def get_multiple_search_results(driver:webdriver, appellation_list:list, homepage='https://www.inao.gouv.fr/rechercher-un-produit'):
    """
    Gets the appellation rulebooks for a list of appellations.
    Uses the INAO search page function to find details on all appellations.
    Also print
    :param driver: the selenium webdriver
    :param appellation_list: A list of appellation to fetch the rulebooks of
    :param homepage: The homepage used, in this case the search page on the INAO website
    :return: A dictionary with the download status for every appellation used
    """
    driver.get(homepage)
    status_dict = {"success": [], "error": []}

    for i in range(0, len(appellation_list)):
        appellation = appellation_list[i]
        print(f'Trying to fetch data for appellation {i+1}/{len(appellation_list)}, appellation: {appellation}')
        try:
            _fetch_inao_cdc(driver, appellation)
            status_dict['success'].append(appellation)
            print('\tAppellation CDC downloaded successfully')
            time.sleep(5)
        except:
            status_dict['error'].append(appellation)
            print('\tAppellation CDC failed to download')
        driver.get(homepage)

    driver.close()
    #print(f"The following appellations couldn't be downloaded: {', '.join(status_dict["error"])}. Please check them individually")
    return status_dict

def setup_driver_options(driver_exe:str, download_path:str):
    """
    Sets up the selenium driver to download the files from the browser to the desired path
    :param driver_exe: the executable driver file
    :param download_path: The path to download the files to
    :return: a configured selenium driver
    """
    options = Options()
    prefs = {
        "download.default_directory": os.path.join(os.getcwd(), download_path),  # <-- your desired folder
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)


    service = Service(f'./{driver_exe}')
    driver = webdriver.Edge(service=service, options=options)
    return driver
