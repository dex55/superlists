import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from time import sleep, time

from superlists import settings


MAX_WAIT = 5


class AutoBrowser:

    @staticmethod
    def configure():
        brand = settings.AUTO_BROWSER['BRAND']
        headless = settings.AUTO_BROWSER['IS_HEADLESS']

        if brand == 'Firefox':
            if headless:
                os.environ['MOZ_HEADLESS'] = '1'
            browser = webdriver.Firefox()

        elif brand == 'Chrome':
            chrome_cfg = webdriver.ChromeOptions()
            if headless:
                chrome_cfg.add_argument('headless')
            browser = webdriver.Chrome(chrome_options=chrome_cfg)

        else:
            raise Exception("Unsupported browser brand: " + str(brand))

        return browser


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = AutoBrowser.configure()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    ###########################################################################
    # Helper methods
    ###########################################################################

    def wait_for_row_in_list_table(self, row_text):
        start_time = time()
        while True:
            try:
                table = self.browser.find_element_by_id('table_to-do_list')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time() - start_time > MAX_WAIT:
                    raise e
                sleep(0.25)

    ###########################################################################
    # Functional Tests
    ###########################################################################

    # Despite the use of unittest module, these are functional tests,
    # not unit tests.

    def test_can_start_a_new_list_and_retrieve_it_later(self):

        # Edith has heard about an online app for managing to-do lists.
        # She goes to check out its home page.
        web_root = self.live_server_url
        self.browser.get(web_root)

        # She notices that the page title and header mention to-do lists.
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away.
        inputbox = self.browser.find_element_by_id('new_item_input')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('new_item_input')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_lists_at_different_URLs(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('new_item_input')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/\d+/')

        # Now a new user, Francis, comes along to the site.

        # *** Note to programmers:
        # We use a new browser session to make sure that no information
        # of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = AutoBrowser.configure()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        # Francis starts a new list by entering a new item. He is less
        # interesting than Edith...
        inputbox = self.browser.find_element_by_id('new_item_input')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/\d+/')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again there is no trace of Edith's list
        self.browser.get(francis_list_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # In the meantime, Edith takes a last look at her list...
        # ... and there is no trace of Francis' list here.
        self.browser.get(edith_list_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Buy peacock feathers', page_text)
        self.assertNotIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep

    def test_layout_and_styling(self):

        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices that the input box is nicely centered
        inputbox = self.browser.find_element_by_id('new_item_input')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # She starts a new list...
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: testing')

        # ... and sees that the input is nicely centered there as well.
        inputbox = self.browser.find_element_by_id('new_item_input')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
