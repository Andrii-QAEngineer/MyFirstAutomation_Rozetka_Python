import unittest  # Модуль для написання тестів
import time  # Модуль для пауз (щоб ви встигали бачити кроки)
from selenium import webdriver  # Керування браузером
from selenium.webdriver.firefox.options import Options  # Налаштування для Firefox
from selenium.webdriver.common.by import By  # Для використання By замість рядків
from selenium.webdriver.support.ui import WebDriverWait  # Явні очікування
from selenium.webdriver.support import expected_conditions as EC  # Умови очікування


class TestRozetkaAuth(unittest.TestCase):

    def setUp(self):
        firefox_options = Options()
        # Потужне маскування під звичайного користувача, щоб сайт не блокував робота
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
        firefox_options.set_preference("general.useragent.override", user_agent)

        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.maximize_window()  # Розгортаємо вікно на весь екран
        self.driver.implicitly_wait(15)  # Чекаємо елементи до 15 секунд

    def test_invalid_login_error_validation(self):
        """Позитивний тест перевірки помилки при введенні невалідного номера телефона."""

        # ===== ARRANGE =====
        base_url = "https://rozetka.com.ua"
        invalid_phone = "1234567890"

        # ===== ACT =====
        # Крок 1: Відкриваємо головну сторінку Розетки
        self.driver.get(base_url)
        time.sleep(5)

        # Крок 2: Натискаємо на кнопку профілю (Увійти) за вашим перевіреним data-testid
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='header-auth-btn']"))
            )
            self.driver.execute_script("arguments[0].click();", login_button)
            time.sleep(4)
        except Exception as e:
            self.driver.save_screenshot("error_step2_login_button.png")
            raise Exception(f"Не знайдено кнопку входу: {e}")

        # Крок 3: Знаходимо поле для введення телефону
        try:
            phone_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel']"))
            )
            phone_field.clear()
            phone_field.send_keys(invalid_phone)
            time.sleep(2)
        except Exception as e:
            self.driver.save_screenshot("error_step3_phone_field.png")
            raise Exception(f"Не знайдено поле телефону: {e}")

        # Крок 4: Натискаємо кнопку підтвердження (універсальний селектор для будь-якої форми входу)
        try:
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit'], button.auth-modal__submit"))
            )
            self.driver.execute_script("arguments[0].click();", submit_button)
            time.sleep(4)
        except Exception as e:
            self.driver.save_screenshot("error_step4_submit_button.png")
            raise Exception(f"Не знайдено кнопку підтвердження: {e}")

        # ===== ASSERT =====
        # Зчитуємо текст помилки, яка з'явилася під полем
        try:
            error_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".validation-message, p.error-message, .form__row_state_error"))
            )
            actual_error_text = error_element.text

            # Головна перевірка: тест пройде успішно, якщо сайт вивів вимогу вказати правильний номер
            self.assertTrue(len(actual_error_text) > 0, "Червона помилка валідації не з'явилася на екрані!")
            print(f"\n[УСПІХ] Тест зафіксував помилку сайту: '{actual_error_text}'")
        except Exception as e:
            self.driver.save_screenshot("error_assert_no_error.png")
            raise Exception(f"Помилка валідації не з'явилася: {e}")

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()
