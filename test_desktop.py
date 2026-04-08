import re
import pytest

BASE_URL = "https://cerulean-praline-8e5aa6.netlify.app"


def test_price_filter(page):
    page.goto(BASE_URL)

    page.wait_for_selector("input[placeholder='От']")

    page.fill("input[placeholder='От']", "10000")
    page.fill("input[placeholder='До']", "50000")

    page.wait_for_timeout(1500)

    assert page.locator("._card_15fhn_2").count() > 0

    price_elements = page.locator("._card_15fhn_2  ._card__price_15fhn_241")
    prices_text = price_elements.all_text_contents()

    for price_str in prices_text:
        price = int(re.sub(r"[^\d]", "", price_str))
        assert 10000 <= price <= 50000, f"Цена {price} вне диапазона [10000, 50000]"


def test_price_filter_negative_input(page):
    page.goto(BASE_URL)
    page.wait_for_selector("input[placeholder='От']")

    price_from = page.locator("input[placeholder='От']")
    price_to = page.locator("input[placeholder='До']")

    price_from.fill("-5000")

    page.wait_for_timeout(300)

    actual_value = price_from.input_value()
    assert (
        actual_value == "" or actual_value == "5000"
    ), f"Поле приняло минус: {actual_value}"

    price_to.fill("-1000")
    page.wait_for_timeout(300)
    actual_value_to = price_to.input_value()
    assert actual_value_to == "" or actual_value_to == "1000"

    assert "minPrice=-" not in page.url


def test_price_filter_zero_values(page):
    page.goto(BASE_URL)
    page.wait_for_selector("input[placeholder='От']")

    price_from = page.locator("input[placeholder='От']")
    price_to = page.locator("input[placeholder='До']")

    price_from.fill("0")
    price_to.fill("0")
    page.wait_for_timeout(500)

    from_value = price_from.input_value()
    to_value = price_to.input_value()

    if from_value == "0" and to_value == "0":
        page.wait_for_function("window.location.search.includes('minPrice=0') && window.location.search.includes('maxPrice=0')")
        assert page.locator("._card_15fhn_2").count() == 0 or page.locator("text=не найдены").is_visible()
    else:
        min_attr = price_from.get_attribute("min")
        assert min_attr == "1", f"Ожидалось ограничение min=1, но min={min_attr}"


def test_price_filter_letters_input(page):
    page.goto(BASE_URL)
    page.wait_for_selector("input[placeholder='От']")

    price_from = page.locator("input[placeholder='От']")
    assert price_from.get_attribute("type") == "number"


def test_price_filter_swap_on_invalid_range(page):
    page.goto(BASE_URL)
    page.wait_for_selector("input[placeholder='От']")

    page.fill("input[placeholder='От']", "5000")
    page.fill("input[placeholder='До']", "1000")
    page.wait_for_function("window.location.search.includes('minPrice=')")

    assert "minPrice=1000" in page.url and "maxPrice=5000" in page.url
    assert page.locator("input[placeholder='От']").input_value() == "1000"
    assert page.locator("input[placeholder='До']").input_value() == "5000"


def test_price_sort(page):
    page.goto(BASE_URL)

    page.wait_for_selector("select[class='_filters__select_1iunh_21']")

    page.get_by_role("combobox").first.select_option("price")
    page.wait_for_function("window.location.search.includes('sortBy=price')")

    page.wait_for_timeout(1500)

    prices_text = page.locator(
        "._card_15fhn_2 ._card__price_15fhn_241"
    ).all_text_contents()
    prices = [int(re.sub(r"[^\d]", "", p)) for p in prices_text]

    assert prices == sorted(prices, reverse=True), "Цены не отсортированы по возрастанию"


def test_sort_by_price_asc(page):
    page.goto(BASE_URL)
    page.wait_for_selector("._card_15fhn_2")

    page.get_by_role("combobox").first.select_option("price")
    page.get_by_role("combobox").nth(1).select_option("asc")

    page.wait_for_function(
        "window.location.search.includes('sortBy=price') && window.location.search.includes('sortOrder=asc')"
    )
    page.wait_for_timeout(1500)

    prices_text = page.locator(
        "._card_15fhn_2 ._card__price_15fhn_241"
    ).all_text_contents()
    prices = [int(re.sub(r"[^\d]", "", p)) for p in prices_text]

    assert prices == sorted(prices), "Цены не отсортированы по возрастанию"


def test_filter_by_category(page):
    page.goto(BASE_URL)
    page.wait_for_selector("._card_15fhn_2")

    page.get_by_role("combobox").nth(2).select_option("3")
    page.wait_for_function("window.location.search.includes('categoryId=3')")

    page.wait_for_timeout(1500)

    assert page.locator("._card_15fhn_2").count() > 0

    expected_category = "Работа"
    category_locator = page.locator("._card_15fhn_2 ._card__category_15fhn_259")
    for i in range(category_locator.count()):
        assert expected_category in category_locator.nth(i).text_content()


def test_filter_by_high_priority(page):
    page.goto(BASE_URL)
    page.wait_for_selector("._card_15fhn_2")

    page.locator("label").filter(has_text="🔥 Только срочные").click()
    page.wait_for_function("window.location.search.includes('priority=urgent')")

    page.wait_for_timeout(1500)

    assert page.locator("._card_15fhn_2").count() > 0

    cards_text = page.locator("._card_15fhn_2").all_text_contents()
    for text in cards_text:
        assert "Срочно" in text, f"В карточке нет пометки 'Срочно'"


def test_stats_timer(page):
    page.goto("https://cerulean-praline-8e5aa6.netlify.app/stats")

    page.get_by_role("button", name="Обновить сейчас").click()
    text_to_update = page.text_content("._timeValue_ir5wu_112")
    assert 5 in text_to_update, "Кнопка не работает!"

    page.get_by_role("button", name="Стоп").click()
    time_before = page.text_content("._timeValue_ir5wu_112")
    page.wait_for_timeout(3000)
    time_after = page.text_content("._timeValue_ir5wu_112")
    assert time_before == time_after, "Таймер не остановился"

    page.get_by_role("button", name="Старт").click()
    page.wait_for_timeout(3000)
    assert time_before != page.text_content(
        "_timeValue_ir5wu_112"
    ), "Таймер не запустился"
