from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from time import sleep


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    ###########################################################################
    # Helper methods
    ###########################################################################

    def assert_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('table_to-do_list')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    ###########################################################################
    # Functional Tests
    ###########################################################################

    # Despite the use of unittest module, these are functional tests,
    # not unit tests.

    def test_can_start_a_new_list_and_retrieve_it_later(self):

        # Edith has heard about an online app for managing to-do lists.
        # She goes to check out its home page.
        web_root = "http://localhost:8000"
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
        sleep(2)
        self.assert_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('new_item_input')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        sleep(2)

        # The page updates again, and now shows both items on her list
        self.assert_row_in_list_table('1: Buy peacock feathers')
        self.assert_row_in_list_table('2: Use peacock feathers to make a fly')

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        self.fail("Finish the test!")

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep


if __name__ == '__main__':
    unittest.main()
