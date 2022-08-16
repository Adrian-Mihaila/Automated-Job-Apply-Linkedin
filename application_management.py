from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
import time
import os

ACCOUNT_EMAIL = os.environ.get('ACC_KEY')
ACCOUNT_PASSWORD = os.environ.get('ACC_PASS')


class app_management:

    def __init__(self):
        self.driver = webdriver.Chrome("C:/Development/chromedriver")
        self.driver.maximize_window()
        self.driver.implicitly_wait(2)  # make all commands to wait max 2 sec
        self.driver.get("https://www.linkedin.com/")

        delay = 5  # seconds
        email_input = WebDriverWait(self.driver, delay).until(
            ec.presence_of_element_located((By.NAME, 'session_key')))
        email_input.send_keys(ACCOUNT_EMAIL)
        pass_input = WebDriverWait(self.driver, delay).until(
            ec.presence_of_element_located((By.NAME, 'session_password')))
        pass_input.send_keys(ACCOUNT_PASSWORD)
        WebDriverWait(self.driver, delay).until(ec.presence_of_element_located(
            (By.CLASS_NAME, 'sign-in-form__submit-button'))).click()

        self.driver.get('your-job-alert-link')
        time.sleep(3)

    def find_li_elements(self):
        """Identify jobs"""
        the_li = self.driver.find_elements(By.CLASS_NAME,
                                           'ember-view.jobs-search-results__list-item.occludable-update.p0'
                                           '.relative.scaffold-layout__list-item')
        # Scroll and load all jobs
        for li_elem in the_li:
            self.driver.execute_script("arguments[0].scrollIntoView();", li_elem)
        # Get the number of jobs(li) from the page
        the_li = self.driver.find_elements(By.CLASS_NAME,
                                           'ember-view.jobs-search-results__list-item.occludable-update.p0.relative'
                                           '.scaffold-layout__list-item')
        return the_li

    def find_pages(self):
        """Identify pages container and get the number of pages"""
        pages_container = self.driver.find_element(By.CLASS_NAME,
                                                   'artdeco-pagination__pages.artdeco-pagination__pages--number')
        page_elements = pages_container.find_elements(By.CLASS_NAME, 'artdeco-pagination__indicator.artdeco-'
                                                                     'pagination__indicator--number.ember-view')
        return page_elements

    def dismiss_job(self):
        """Exit the application"""
        dismiss = self.driver.find_element(By.CLASS_NAME,
                                           'artdeco-modal__dismiss.artdeco-button.artdeco-button--circle'
                                           '.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary'
                                           '.ember-view')
        dismiss.click()
        time.sleep(1)
        try:
            confirm_dismiss = self.driver.find_element(By.CLASS_NAME,
                                                       'artdeco-modal__confirm-dialog-btn.artdeco-button'
                                                       '.artdeco-button--2.artdeco-button--secondary.ember-view')
            confirm_dismiss.click()
            time.sleep(1)
        except StaleElementReferenceException or NoSuchElementException or ElementNotInteractableException:
            finish_btn = self.driver.find_element(By.CLASS_NAME, 'artdeco-button.artdeco-button--2'
                                                                 '.artdeco-button--primary.ember-view.mlA.block')
            finish_btn.click()
        finally:
            return

    def apply_for_job(self):
        """Apply for job"""
        try:
            simple_apply = self.driver.find_element(By.CLASS_NAME,
                                                    'jobs-apply-button.artdeco-button.artdeco-button--3'
                                                    '.artdeco-button--primary.ember-view')
            simple_apply.click()
            time.sleep(1)

            next_btn = self.driver.find_element(By.CLASS_NAME,
                                                'artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view')
            looped = 0
            while next_btn.is_enabled() and looped < 6:
                job_panel = self.driver.find_element(By.CLASS_NAME, 'artdeco-modal.artdeco-modal--layer-default'
                                                                    '.jobs-easy-apply-modal')
                job_panel.send_keys(Keys.END)
                time.sleep(1)

                next_btn.click()
                looped += 1
                time.sleep(1)
            else:
                self.dismiss_job()
        except StaleElementReferenceException:
            try:
                examine_btn = self.driver.find_element(By.CLASS_NAME, 'artdeco-button.artdeco-button--2'
                                                                      '.artdeco-button--primary.ember-view')

                examine_btn.click()
                time.sleep(1)

                send_btn = self.driver.find_element(By.CLASS_NAME, 'artdeco-button.artdeco-button--2'
                                                                   '.artdeco-button--primary.ember-view')

                send_btn.click()
                time.sleep(1)

                self.dismiss_job()
                return
            except StaleElementReferenceException:
                self.dismiss_job()
                return
            except ElementNotInteractableException:
                return
        except NoSuchElementException:  # when there is no apply btn
            return
        finally:
            return

    def iterate_jobs(self):
        jobs_elem_list = self.find_li_elements()
        for li_element in jobs_elem_list:  # Iterate through each job
            li_element.click()
            time.sleep(2)
            self.apply_for_job()
        return

    def apply_for_all_jobs(self):
        self.find_li_elements()
        all_pages = self.find_pages()
        for _ in range(0, len(all_pages)):  # Iterate through pages
            all_pages = self.find_pages()
            try:
                all_pages[_].click()
                print(f"clicked page {_}")
                time.sleep(1)
                self.iterate_jobs()
            except StaleElementReferenceException:
                continue
        return
