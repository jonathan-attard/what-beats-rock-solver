from selenium import webdriver

# Specify the path to the ChromeDriver executable if it's not in your PATH
# driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

# Otherwise, you can initialize it directly if ChromeDriver is in your PATH
driver = webdriver.Chrome()

# Open a webpage
driver.get('https://www.google.com')

# Print the title of the page
print(driver.title)

# Close the browser
driver.quit()
