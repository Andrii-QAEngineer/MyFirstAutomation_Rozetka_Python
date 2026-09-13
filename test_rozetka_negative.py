import unittest  # Модуль для написання тестів
import time  # Модуль для пауз
from selenium import webdriver  # Керування браузером
from selenium.webdriver.firefox.options import Options  # Налаштування для Firefox


class TestRozetkaE2E(unittest.TestCase):

    def setUp(self):
        firefox_options = Options()
        # Маскування під звичайного користувача, щоб сайт не блокував робота
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
        firefox_options.set_preference("general.useragent.override", user_agent)

        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.maximize_window()  # Розгортаємо вікно на весь екран
        self.driver.implicitly_wait(15)  # Чекаємо елементи до 15 секунд

    def test_notebook_purchase_flow(self):
        """Великий E2E квест за точними кроками вашого Selenium IDE запису."""

        # ===== ACT =====
        # Крок 1: Відкриваємо головну сторінку Розетки (Запис: open /)
        self.driver.get("https://rozetka.com.ua")
        time.sleep(5)

        # Крок 2: Клікаємо на категорію "Ноутбуки та комп'ютери" (Запис: linkText=Ноутбуки та комп'ютери)
        menu_item = self.driver.find_element("link text", "Ноутбуки та комп’ютери")
        self.driver.execute_script("arguments[0].click();", menu_item)
        time.sleep(4)

        # Крок 3: Клікаємо на плитку категорії "Ноутбуки" (Запис: крок №4 вашого скріншоту)
        notebooks_category = self.driver.find_element("css selector",
                                                      ".rz-widget-tiles-list:nth-child(4) .border-r-1:nth-child(1) .object-contain")
        self.driver.execute_script("arguments[0].click();", notebooks_category)
        time.sleep(5)

        # Крок 4: Клікаємо на іконку кошика першого ноутбука прямо в каталозі! (Запис: крок №9)
        buy_icon = self.driver.find_element("css selector", "rz-catalog-tile:nth-child(1) .toOrder svg")
        self.driver.execute_script("arguments[0].click();", buy_icon)
        time.sleep(4)

        # Крок 5: Натискаємо "Оформити замовлення" у вікні кошика (Запис: крок №13 linkText=Оформити замовлення)
        checkout_button = self.driver.find_element("link text", "Оформити замовлення")
        self.driver.execute_script("arguments[0].click();", checkout_button)
        time.sleep(6)

        # Крок 6: Ми на сторінці оформлення! Шукаємо поле телефону та вводимо 1234567890
        phone_field = self.driver.find_element("css selector", "input[type='tel']")
        phone_field.clear()
        phone_field.send_keys("1234567890")
        time.sleep(2)

        # Крок 7: Натискаємо кнопку "Продовжити" (наш фінальний data-qaid кнопка)
        submit_button = self.driver.find_element("css selector", "button[data-qaid='submit-phone']")
        self.driver.execute_script("arguments[0].click();", submit_button)

        # Залишаємо паузу 5 секунд, щоб ви побачили успішний результат
        time.sleep(5)

        # ===== ASSERT =====
        self.assertIn("checkout", self.driver.current_url.lower(), "Робот не зміг дійти до сторінки оформлення!")

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()
