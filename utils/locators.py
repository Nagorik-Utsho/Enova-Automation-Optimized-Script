class location_type:
    all_location_xpath='//android.view.View[@content-desc="All Tab 1 of 3"]'
    premium_xpath='//android.view.View[@content-desc="Premium\nTab 2 of 3"]'
    recommended_xpath='//android.view.View[@content-desc="Recommended Servers Tab 3 of 3"]'

class location_page:
    scroller_xpath_1='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[5]/android.view.View/android.view.View/android.view.View'
    scroller_xpath_2='//android.widget.ScrollView'


class CountryDropdown:

    @staticmethod
    def close_dropdown(country_name: str) -> str:
        """
        Returns the XPath for a country dropdown element that matches the given country
        and does not contain a '-' (i.e., only the country name, not servers).
        """
        return f'//android.view.View[contains(@content-desc,"{country_name}") and not(contains(@content-desc, "-"))]'




