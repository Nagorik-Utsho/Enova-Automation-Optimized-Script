from .locators import location_page
from .necessary_packages import *

# def retry(max_attempts=3, delay=2, exceptions=(Exception,)):
#     """Retry decorator for flaky UI actions."""
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             for attempt in range(1, max_attempts + 1):
#                 try:
#                     return func(*args, **kwargs)
#                 except exceptions as e:
#                     print(f"⚠️ Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}")
#                     time.sleep(delay)
#             print(f"❌ All {max_attempts} attempts failed for {func.__name__}")
#             return {"status": "FAILED", "message": f"{func.__name__} failed after {max_attempts} attempts"}
#         return wrapper
#     return decorator

# @retry(max_attempts=3, delay=2)
def scroll_and_click_in_scrollview(driver, element_text, max_scrolls_per_direction=5, max_cycles=5):
    """
    Scroll in a ScrollView and click the element if found.
    Returns a dict with status and message.
    """
    print("Seraching for the server")
    scrollview_xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[5]/android.view.View/android.view.View/android.view.View'

    try:
        wait = WebDriverWait(driver, 60)
        scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, scrollview_xpath)))
    except TimeoutException:
        print("❌ ScrollView container not found.")
        return {"status": "FAILED", "message": "ScrollView container not found"}

    directions = ["down", "up"]

    for cycle in range(max_cycles):
        for direction in directions:
            for attempt in range(max_scrolls_per_direction):
                try:
                    scrollable = driver.find_element(AppiumBy.XPATH, scrollview_xpath)
                    try:
                        element = scrollable.find_element(
                            AppiumBy.XPATH,
                            f'.//*[contains(@content-desc, "{element_text}")]'
                        )
                        element.click()
                        return {"status": "SUCCESS", "message": f"Element '{element_text}' clicked successfully"}
                    except NoSuchElementException:
                        driver.execute_script("mobile: scrollGesture", {
                            "elementId": scrollable.id,
                            "direction": direction,
                            "percent": 0.8
                        })
                        time.sleep(0.5)
                except StaleElementReferenceException:
                    print("⚠️ ScrollView went stale, retrying...")

    print(f"❌ Element '{element_text}' not found.")
    return {"status": "FAILED", "message": f"Element '{element_text}' not found after scrolling"}



def server_list(driver):
    """Go to the Server list to check all the servers"""
    print ("Now in the server list")

    try:
        wait = WebDriverWait(driver, 120)
        server = wait.until(
            EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]'))
        )
        server.click()
        time.sleep(2)
        return {"status": "SUCCESS", "message": "Server list opened successfully"}
    except Exception as e:
        return {"status": "FAILED", "message": f"Server list not found: {e}"}

# @retry(max_attempts=3, delay=2)
def scroll_and_click_country(driver ,country,max_scrolls_per_direction=2, max_cycles=5):
    """
    Scroll in a ScrollView and click the element if found.
    Returns a dict with status and message.
    """

    possible_scrollviews = [
        location_page.scroller_xpath_1,
        location_page.scroller_xpath_2
    ]

    wait = WebDriverWait(driver, 60)
    scrollable = None
    scrollview_xpath = None

    # Try to locate any valid scrollview
    for xpath in possible_scrollviews:
        try:
            scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
            scrollview_xpath = xpath
            break
        except TimeoutException:
            print(f"⚠️ ScrollView not found with xpath: {xpath}")

    if not scrollable:
        print("❌ No valid ScrollView container found.")
        return {"status": "FAILED", "message": "No valid ScrollView container found"}

    try:
        wait = WebDriverWait(driver, 60)
        scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, scrollview_xpath)))
    except TimeoutException:
        print("❌ ScrollView container not found.")
        return {"status": "FAILED", "message": "ScrollView container not found"}

    directions = ["down", "up"]

    for cycle in range(max_cycles):
        for direction in directions:
            for attempt in range(max_scrolls_per_direction):
                try:
                    scrollable = driver.find_element(AppiumBy.XPATH, scrollview_xpath)
                    try:
                        element = scrollable.find_element(
                             AppiumBy.XPATH, f".//android.view.View[contains(@content-desc, '{country}')]"
                        )
                        element.click()
                        return {"status": "SUCCESS", "message": f"Element '{country}' clicked successfully"}
                    except NoSuchElementException:
                        driver.execute_script("mobile: scrollGesture", {
                            "elementId": scrollable.id,
                            "direction": direction,
                            "percent": 0.8,
                            "duration":1000
                        })
                        #time.sleep(0.5)
                except StaleElementReferenceException:
                    print("⚠️ ScrollView went stale, retrying...")

    print(f"❌ Element '' not found.")
    return {"status": "FAILED", "message": f"Element '{country}' not found after scrolling"}



def scroll_and_collect_elements_countries(driver, max_scrolls_per_direction=2, max_cycles=2):
    """
    Scrolls through a ScrollView and collects all element names
    whose XPath matches //android.view.View[contains(@content-desc, "")].
    Returns a dict with status and collected element names.
    """
    print("🔍 Collecting android.view.View elements (with content-desc) from ScrollView...")

    possible_scrollviews = [
        location_page.scroller_xpath_1,
        location_page.scroller_xpath_2
    ]

    wait = WebDriverWait(driver, 60)
    scrollable = None
    scrollview_xpath = None

    # Try to locate any valid scrollview
    for xpath in possible_scrollviews:
        try:
            scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
            scrollview_xpath = xpath
            break
        except TimeoutException:
            print(f"⚠️ ScrollView not found with xpath: {xpath}")

    if not scrollable:
        print("❌ No valid ScrollView container found.")
        return {"status": "FAILED", "message": "No valid ScrollView container found"}

    collected_elements = set()
    directions = ["down", "up"]

    for cycle in range(max_cycles):
        for direction in directions:
            for attempt in range(max_scrolls_per_direction):
                try:
                    scrollable = driver.find_element(AppiumBy.XPATH, scrollview_xpath)

                    # 🔹 Collect elements with the desired XPath shape
                    visible_elements = scrollable.find_elements(
                        AppiumBy.XPATH, ".//android.view.View[contains(@content-desc, '')]"
                    )

                    for el in visible_elements:
                        try:
                            name = el.get_attribute("content-desc")
                            if name and name.strip():
                                collected_elements.add(name.strip())
                        except Exception:
                            pass

                    # 🔹 Scroll further
                    driver.execute_script("mobile: scrollGesture", {
                        "elementId": scrollable.id,
                        "direction": direction,
                        "percent": 0.8,
                        "duration":1000
                    })
                    #time.sleep(0.5)

                except StaleElementReferenceException:
                    print("⚠️ ScrollView went stale, retrying...")

    print(f"✅ Collected {len(collected_elements)} unique android.view.View elements.")
    return {
        "status": "SUCCESS",
        "elements": list(collected_elements)
    }



def scroll_and_collect_all_servers(driver,max_scrolls_per_direction=2, max_cycles=2):
    """
    Scrolls through a ScrollView and collects all element names
    whose XPath matches //android.view.View[contains(@content-desc, "")].
    Returns a dict with status and collected element names.
    """
    print("🔍 Collecting android.view.View elements (with content-desc) from ScrollView...")

    possible_scrollviews = [
        location_page.scroller_xpath_1,
        location_page.scroller_xpath_2
    ]

    wait = WebDriverWait(driver, 60)
    scrollable = None
    scrollview_xpath = None

    # Try to locate any valid scrollview
    for xpath in possible_scrollviews:
        try:
            scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
            scrollview_xpath = xpath
            break
        except TimeoutException:
            print(f"⚠️ ScrollView not found with xpath: {xpath}")

    if not scrollable:
        print("❌ No valid ScrollView container found.")
        return {"status": "FAILED", "message": "No valid ScrollView container found"}

    collected_elements = set()
    directions = ["down", "up"]

    for cycle in range(max_cycles):

        for direction in directions:
            for attempt in range(max_scrolls_per_direction):
                try:
                    scrollable = driver.find_element(AppiumBy.XPATH, scrollview_xpath)

                    # 🔹 Collect elements with the desired XPath shape
                    visible_elements = scrollable.find_elements(
                        AppiumBy.XPATH, ".//android.view.View[contains(@content-desc, '-')] | .//android.widget.ImageView"
                    )

                    for el in visible_elements:
                        try:
                            name = el.get_attribute("content-desc")
                            if name and name.strip():
                                collected_elements.add(name.strip())
                        except Exception:
                            pass

                    # 🔹 Scroll further
                    driver.execute_script("mobile: scrollGesture", {
                        "elementId": scrollable.id,
                        "direction": direction,
                        "percent": 0.6,
                        "duration":1000
                    })
                    #time.sleep(0.5)

                except StaleElementReferenceException:
                    print("⚠️ ScrollView went stale, retrying...")

    print(f"✅ Collected {len(collected_elements)} unique android.view.View elements.")
    return {
        "status": "SUCCESS",
        "elements": list(collected_elements)
    }

def scroll_and_click_server(driver ,server_name,max_scrolls_per_direction=2, max_cycles=5):
    """
    Scroll in a ScrollView and click the element if found.
    Returns a dict with status and message.
    """

    possible_scrollviews = [
        location_page.scroller_xpath_1,
        location_page.scroller_xpath_2
    ]

    wait = WebDriverWait(driver, 60)
    scrollable = None
    scrollview_xpath = None

    # Try to locate any valid scrollview
    for xpath in possible_scrollviews:
        try:
            scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
            scrollview_xpath = xpath
            break
        except TimeoutException:
            print(f"⚠️ ScrollView not found with xpath: {xpath}")

    if not scrollable:
        print("❌ No valid ScrollView container found.")
        return {"status": "FAILED", "message": "No valid ScrollView container found"}

    try:
        wait = WebDriverWait(driver, 60)
        scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, scrollview_xpath)))
    except TimeoutException:
        print("❌ ScrollView container not found.")
        return {"status": "FAILED", "message": "ScrollView container not found"}

    directions = ["down", "up"]

    for cycle in range(max_cycles):
        for direction in directions:
            for attempt in range(max_scrolls_per_direction):
                try:
                    scrollable = driver.find_element(AppiumBy.XPATH, scrollview_xpath)
                    try:
                        element = scrollable.find_element(
                            AppiumBy.XPATH,
                            f".//android.view.View[contains(@content-desc, '{server_name}')] | .//android.widget.ImageView[contains(@content-desc,'{server_name}')]"
                        )
                        element.click()
                        return {"status": "SUCCESS", "message": f"Element '{server_name}' clicked successfully"}
                    except NoSuchElementException:
                        driver.execute_script("mobile: scrollGesture", {
                            "elementId": scrollable.id,
                            "direction": direction,
                            "percent": 0.7,
                            "duration":1000
                        })
                        #time.sleep(0.5)
                except StaleElementReferenceException:
                    print("⚠️ ScrollView went stale, retrying...")

    print(f"❌ Element '' not found.")
    return {"status": "FAILED", "message": f"Element '{server_name}' not found after scrolling"}





