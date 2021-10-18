from selenium import webdriver

from pages.quotes_page import QuotesPage, InvalidTagForAuthorError

try:
    author = input("Enter the author you would like quotes from: ")
    tag = input("Enter your tag: ")

    chrome = webdriver.Chrome(executable_path="/opt/homebrew/bin/chromedriver")
    chrome.get("http://quotes.toscrape.com/search.aspx")
    page = QuotesPage(chrome)

    print(page.search_for_quotes(author, tag))
except InvalidTagForAuthorError as e:
    print(e)
except Exception as e:
    print(e)
    print("An unknown error has occurred. Please try again.")
