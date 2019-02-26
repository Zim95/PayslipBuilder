# Headless selenium firefox setup


from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

# setting headless options
opts = Options()
opts.set_headless()

# asserting to run in headless mode
assert opts.headless

# creating headless browser
browser = Firefox(options=opts)

#getting browser details: Functional Test 1
browser.get('http://localhost:8002')
assert 'Django' in browser.title