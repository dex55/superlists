from selenium import webdriver

browser = webdriver.Firefox()
home_page = "http://localhost:8000"
browser.get(home_page)

assert "Django" in browser.title
