from .necessary_packages import WebDriverWait, EC, AppiumBy, TimeoutException, NoSuchElementException, StaleElementReferenceException, time, wraps

def retry(max_attempts=3, delay=2, exceptions=(Exception,)):
    """Retry decorator for flaky UI actions."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"⚠️ Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}")
                    time.sleep(delay)
            print(f"❌ All {max_attempts} attempts failed for {func.__name__}")
            return {"status": "FAILED", "message": f"{func.__name__} failed after {max_attempts} attempts"}
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def scroll_and_click_in_scrollview(driver, element_text, max_scrolls_per_direction=5, max_cycles=5):
    """
    Scroll in a ScrollView and click the element if found.
    Returns a dict with status and message.
    """
    scrollview_xpath = '//android.widget.FrameLayout[@resource-id="android:id/content"]//android.view.View[5]//android.view.View'

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
