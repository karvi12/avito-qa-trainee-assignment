from playwright.sync_api import sync_playwright

def test_open_site():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://cerulean-praline-8e5aa6.netlify.app")

        page.wait_for_timeout(3000)

        page.screenshot(path="avito_home.png")

        browser.close()


if __name__ == "__main__":
    test_open_site()