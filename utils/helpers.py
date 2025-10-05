from .necessary_packages import *

def wait_and_click(driver, xpath, timeout=60):
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    element.click()