from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from locators.quotes_page_locators import QuotesPageLocators
from parsers.quote import QuoteParser


class QuotesPage:
    def __init__(self, browser):
        self.browser = browser

    @property
    def quotes(self):
        return [
            QuoteParser(e)
            for e in self.browser.find_elements_by_css_selector(
                QuotesPageLocators.QUOTE
            )
        ]

    @property
    def author_dropdown(self):
        element = self.browser.find_element_by_css_selector(
            QuotesPageLocators.AUTHOR_DROPDOWN
        )
        return Select(element)

    @property
    def tags_dropdown(self):
        element = self.browser.find_element_by_css_selector(
            QuotesPageLocators.TAG_DROPDOWN
        )
        return Select(element)

    @property
    def search_button(self):
        return self.browser.find_element_by_css_selector(
            QuotesPageLocators.SEARCH_BUTTON
        )

    def select_author(self, author_name):
        self.author_dropdown.select_by_visible_text(author_name)

    def get_available_tags(self):
        return [option.text.strip() for option in self.tags_dropdown.options]

    def select_tag(self, tag_name):
        self.tags_dropdown.select_by_visible_text(tag_name)

    def search_for_quotes(self, author_name, tag_name):
        self.select_author(author_name)

        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, QuotesPageLocators.TAG_DROPDOWN_VALUE_OPTION)
            )
        )

        try:
            self.select_tag(tag_name)
        except NoSuchElementException:
            raise InvalidTagForAuthorError(
                f"Author '{author_name}' does not have any quotes tagged with '{tag_name}'"
            )
        self.search_button.click()
        return self.quotes


class InvalidTagForAuthorError(ValueError):
    pass
