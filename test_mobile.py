import pytest

BASE_URL = "https://cerulean-praline-8e5aa6.netlify.app/"


@pytest.fixture
def mobile_page(browser):
    context = browser.new_context(
        viewport={"width": 390, "height": 844},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    )
    page = context.new_page()
    yield page
    context.close()


def test_dark_light_theme(mobile_page):
    mobile_page.goto(BASE_URL)

    toggle = mobile_page.locator("._themeToggle_127us_1")

    get_theme = "document.documentElement.getAttribute('data-theme')"
    initial_theme = mobile_page.evaluate(get_theme)
    print(f"Initial theme: {initial_theme}")

    toggle.click()

    mobile_page.wait_for_function(
        f"document.documentElement.getAttribute('data-theme') !== '{initial_theme}'"
    )

    new_theme = mobile_page.evaluate(get_theme)
    assert new_theme != initial_theme, "Тема не переключилась"

    toggle.click()
    mobile_page.wait_for_function(
        f"document.documentElement.getAttribute('data-theme') === '{initial_theme}'"
    )

    final_theme = mobile_page.evaluate(get_theme)
    assert final_theme == initial_theme, "Тема не вернулась в исходное состояние"
