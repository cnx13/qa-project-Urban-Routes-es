import time
import timeit

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR, '.button.round')
    comfort_icon = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')

    np_number_field = (By.XPATH, '//div[@class="np-text" and text()="Número de teléfono"]')
    np_number_field_full = (By.XPATH, '//div[@class="np-text" and text()="+1 123 123 12 12"]') #<div class="np-text">+1 123 123 12 12</div>
    phone_number_popup = (By.XPATH, '/html/body/div/div/div[1]/div[2]/div[1]/form/div[1]/div/label')
    phone_number_popup_write = (By.XPATH, '/html/body/div/div/div[1]/div[2]/div[1]/form/div[1]/div/input')
    phone_number_submit_button = (By.XPATH, '/html/body/div/div/div[1]/div[2]/div[1]/form/div[2]/button')
    sms_code_field_label = (By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[2]/form/div[1]/div[1]/label')
    sms_code_field_input = (By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[2]/form/div[1]/div[1]/input')
    sms_code_submit_button = (By.XPATH, '/html/body/div/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
    phone_number_popup_close = (By.XPATH, '//div[@class="close-button section-close"]')

    payment_method_main_button = (By.XPATH, '//div[@class="pp-text" and text()="Método de pago"]')
    payment_method_popup_add_card_button = (By.XPATH, '//div[@class="pp-title" and text()="Agregar tarjeta"]')
    payment_method_popup_add_card_field = (By.XPATH, '//input[@id="number"]')
    payment_method_popup_add_card_code = (By.XPATH, '//input[@placeholder="12"]') #<input type="text" id="code" name="code" placeholder="12" class="card-input" value="">
    payment_method_popup_final_add_button = (By.XPATH, '//button[@class="button full" and contains(text(), "Agregar")]') #<button type="submit" class="button full">Agregar</button>
    payment_method_popup_click_to_focus = (By.XPATH, '//div[@class="head" and text()="Agregar tarjeta"]') #<div class="head">Agregar tarjeta</div>
    payment_method_popup_close = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button') #<button class="close-button section-close"></button>
    payment_method_main_button_full = (By.XPATH, '//div[@class="pp-value-text" and text()="Tarjeta"]') #<div class="pp-value-text">Tarjeta</div>

    message_driver_label = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[3]/div/label')
    message_driver_input = (By.XPATH, '//*[@id="comment"]')

    requests_blanket_tissues = (By.XPATH, '//div[contains(text(), "Manta y pañuelos")]/following::span[@class="slider round"][1]')
    requests_blanket_tissues_color = (By.XPATH, '//span[@class="slider round"]')#<span class="slider round"></span>

    requests_icecream = (By.XPATH, '//div[@class="counter-plus"]')  # <div class="counter-plus">+</div>  '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    requests_icecream_counter = (By.XPATH, '//div[@class="counter-value"]') #<div class="counter-value">0</div>

    confirm_taxi_request_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')
    searching_driver_popup = (By.XPATH, '//div[@class="order-header-title" and contains(text(), "Buscar automóvil")]') #<div class="order-header-title">Buscar automóvil</div>

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def get_request_taxi_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.request_taxi_button)
        )

    def set_request_taxi_button(self):
        self.get_request_taxi_button().click()

    def get_comfort_icon(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.comfort_icon)
        )

    def set_comfort_icon(self):
        self.get_comfort_icon().click()

    def get_np_number_field(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.np_number_field)
        )

    def set_np_number_field(self):
        self.get_np_number_field().click()

    def get_np_number_field_full(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.np_number_field_full)
        )

    def get_phone_number_popup(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.phone_number_popup_write)
        )

    def set_phone_number_popup(self, phone_number):
        input_field = self.get_phone_number_popup()
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.phone_number_popup_write)
        )
        input_field.clear()  # Limpia el campo antes de escribir
        input_field.send_keys(phone_number)

    def get_phone_number_submit_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.phone_number_submit_button)
            )

    def set_phone_number_submit_button(self):
        self.get_phone_number_submit_button().click()

    def get_sms_code_field_label(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.sms_code_field_label)
        )

    def set_sms_code_field_label(self, sms_code):
        input_field = WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.sms_code_field_input)
        )
        input_field.clear()
        input_field.send_keys(sms_code)

    def get_sms_code_submit_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.sms_code_submit_button)
        )

    def set_sms_code_submit_button(self):
        self.get_sms_code_submit_button().click()

    def get_payment_method_main_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.payment_method_main_button)
        )

    def set_payment_method_main_button(self):
        self.get_payment_method_main_button().click()

    def get_payment_method_popup_add_card_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.payment_method_popup_add_card_button)
        )

    def set_payment_method_popup_add_card_button(self):
        self.get_payment_method_popup_add_card_button().click()

    def get_payment_method_popup_add_card_field(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.payment_method_popup_add_card_field)
        )

    def set_payment_method_popup_add_card_field(self, card_number):
        input_field = WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.payment_method_popup_add_card_field)
        )
        input_field.click()
        input_field.clear()
        input_field.send_keys(card_number)

    def get_payment_method_popup_add_card_code(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.payment_method_popup_add_card_code)
        )

    def set_payment_method_popup_add_card_code(self, card_code):
        input_field = WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.payment_method_popup_add_card_code)
        )
        input_field.click()
        input_field.clear()
        input_field.send_keys(card_code)


    def get_payment_method_popup_click_to_focus(self):
        return WebDriverWait(self.driver, 5).until(
        expected_conditions.element_to_be_clickable(self.payment_method_popup_click_to_focus)
    )

    def set_payment_method_popup_click_to_focus(self):
         self.get_payment_method_popup_click_to_focus().click()

    def get_payment_method_popup_final_add_button(self):
        return WebDriverWait(self.driver, 5).until(
        expected_conditions.element_to_be_clickable(self.payment_method_popup_final_add_button)
    )

    def set_payment_method_popup_final_add_button(self):
         self.get_payment_method_popup_final_add_button().click()

    def get_payment_method_popup_close(self):
        return WebDriverWait(self.driver, 10).until(
        expected_conditions.visibility_of_element_located(self.payment_method_popup_close)
        )

    def set_payment_method_popup_close(self):
         self.get_payment_method_popup_close().click()

    def get_payment_method_main_button_full(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.payment_method_main_button_full)
        )

    def get_message_driver_label(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.message_driver_label)
        )

    def set_message_driver_label(self, message):
        input_field = WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.message_driver_input)
        )
        input_field.clear()
        input_field.send_keys(message)

    def get_message_driver_input(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.message_driver_input)
        )

    def get_requests_blanket_tissues(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.requests_blanket_tissues)
        )

    def set_requests_blanket_tissues(self):
         self.get_requests_blanket_tissues().click()

    def get_requests_icecream(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.requests_icecream)
        )

    def set_requests_icecream(self):
        element = self.get_requests_icecream()
        element.click()
        element.click()

    def get_requests_icecream_counter(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.requests_icecream_counter)
        )

    def get_confirm_taxi_request_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.confirm_taxi_request_button)
        )

    def set_confirm_taxi_request_button(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.confirm_taxi_request_button)
        ).click()

    def get_searching_driver_popup(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.searching_driver_popup)
        )

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(), options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver) #OBJETO. Vinculo entre la prueba y la página. Siempre debe crearse de la clase de interés, en este caso UrbanRoutes.
        address_from = data.address_from #variable direccion desde. se convierte una en otra para interactuar con ella mas abajo.
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_request_taxi(self):
        self.test_set_route()
        routes_page = UrbanRoutesPage(self.driver) #OBJETO para acceder a métodos
        routes_page.set_request_taxi_button()
        routes_page.set_comfort_icon()
        assert WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(routes_page.np_number_field)
        )

    def test_phone_number(self):
        self.test_request_taxi()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_np_number_field()
        routes_page.set_phone_number_popup(data.phone_number)
        routes_page.set_phone_number_submit_button()
        sms_code = retrieve_phone_code(self.driver)
        routes_page.set_sms_code_field_label(sms_code)
        routes_page.set_sms_code_submit_button()
        assert routes_page.get_np_number_field_full().text == data.phone_number


    def test_add_card(self):
        self.test_request_taxi()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_payment_method_main_button()
        routes_page.set_payment_method_popup_add_card_button()
        card_number = data.card_number
        card_code = data.card_code
        routes_page.set_payment_method_popup_add_card_field(card_number)
        routes_page.set_payment_method_popup_add_card_code(card_code)
        routes_page.set_payment_method_popup_click_to_focus()
        routes_page.set_payment_method_popup_final_add_button()
        routes_page.set_payment_method_popup_close()
        assert WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(routes_page.payment_method_main_button_full)
        )

    def test_message_driver(self):
        self.test_request_taxi()
        routes_page = UrbanRoutesPage(self.driver)
        message = data.message_for_driver
        routes_page.set_message_driver_label(message)
        assert routes_page.get_message_driver_input().get_property('value') == message

    def test_add_blanket(self):
        self.test_request_taxi()
        routes_page = UrbanRoutesPage(self.driver)
        color_before = routes_page.get_requests_blanket_tissues().value_of_css_property("background-color")
        routes_page.set_requests_blanket_tissues()
        WebDriverWait(self.driver, 5).until(
        lambda driver: routes_page.get_requests_blanket_tissues().value_of_css_property("background-color") != color_before
    )
        color_after = routes_page.get_requests_blanket_tissues().value_of_css_property("background-color")
        assert color_before != color_after

    def test_add_icecream(self):
        self.test_request_taxi()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_requests_icecream()
        assert routes_page.get_requests_icecream_counter().text == '2'

    def test_request_ride_confirmation(self):
        self.test_request_taxi()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_confirm_taxi_request_button()
        assert WebDriverWait(self.driver, 5).until(
             expected_conditions.visibility_of_element_located(routes_page.searching_driver_popup)
        )



    @classmethod
    def teardown_class(cls):
        cls.driver.quit()