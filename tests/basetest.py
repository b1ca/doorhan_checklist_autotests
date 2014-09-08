#coding=utf-8
from __future__ import unicode_literals
import unittest
import logging
import random
import sys
import os
from datetime import datetime

from testconfig import config

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.remote_connection import LOGGER


URL = 'http://146.185.169.28/doorhan_test/'
LOGIN = config['login']
PASS = config['pass']
ORDER_NAME_1C = config['order_name_1c']
LOGGER.setLevel(logging.WARNING)


class Basetest(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.driver.get(URL)
        cls.driver.find_element_by_css_selector("#LoginForm_username").send_keys(LOGIN)
        cls.driver.find_element_by_css_selector("#LoginForm_password").send_keys(PASS)
        cls.driver.find_element_by_css_selector("input[type=submit]").click()
        cls.driver.implicitly_wait(10)

    def tearDown(self):
        if sys.exc_info()[0]:
            method_name = self._testMethodName
            class_name = type(self).__name__
            time_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            folder = os.path.dirname(os.getcwd())
            directory = "".join([folder, "/test-results/", class_name])

            if not os.path.exists(directory):
                os.makedirs(directory)

            file_name = "%s/%s - %s.png" % (directory, time_now, method_name)

            self.driver.get_screenshot_as_file(file_name)
            # for jenkins integration
            print "[[ATTACHMENT|%s]]" % file_name
            print "current url - %s" % self.driver.current_url

    @classmethod
    def tearDownClass(cls):
        if not 'debug' in config and cls.driver:
            cls.driver.quit()

    def get_element_by_label_text(self, label_text):
        element_id = self.driver.find_element_by_xpath("//label[contains(text(), '"+label_text+"')]").\
            get_attribute("for")
        return self.driver.find_element_by_id(element_id)

    def sendkeys_by_label_text(self, label_text, text_to_type):
        element = self.get_element_by_label_text(label_text)
        element.clear()
        element.send_keys(text_to_type)

    def click_option_by_label_text(self, label_text, option):
        element_id = self.get_element_by_label_text(label_text).get_attribute("id")
        self.driver.find_element_by_xpath("//select[@id='"+element_id+"']/option[text() = '"+option+"']").click()

    def go_next(self):
        self.driver.find_element_by_css_selector("*[id*=ext]").click()

    def wait_until_jquery(self, seconds_to_wait):
        jquery_active = lambda x: self.driver.execute_script("return jQuery.active == 0")
        WebDriverWait(self.driver, seconds_to_wait).until(jquery_active)

    def strings_to_search(self):
        return self.driver.find_elements_by_css_selector("span[style = \"cursor:pointer;\"]")[-1].text

    def click_checkbox_by_label_text(self, label_text):
        element_id = self.get_element_by_label_text(label_text).get_attribute("id")
        element = self.driver.find_element_by_css_selector("input[id='"+element_id+"'][type='checkbox']")
        if not element.is_selected():
            element.click()

    def unclick_checkbox_by_label_text(self, label_text):
        element_id = self.get_element_by_label_text(label_text).get_attribute("id")
        element = self.driver.find_element_by_css_selector("input[id='"+element_id+"'][type='checkbox']")
        if element.is_selected():
            element.click()

    def choose_product(self):
        driver = self.driver
        driver.find_element_by_xpath("//a[text() = \"Заказы\"]").click()
        self.assertIn("Заказы", driver.find_element_by_css_selector(".breadcrumbs").text)
        orders = driver.find_elements_by_css_selector(".link-column:nth-of-type(2) a")
        order = orders[random.randint(0, len(orders)-1)]
        order_text = order.text
        order.click()
        self.assertIn(order_text, driver.find_element_by_css_selector(".breadcrumbs").text)
        driver.find_element_by_xpath("//div[@class = \"nav-order\"]//a[text() = \"Добавить изделие\"]").click()
        self.assertIn("Выбор изделия", driver.find_element_by_css_selector(".breadcrumbs").text)
        driver.find_element_by_xpath("//span[text() = \"Гаражные\"]").click()
        driver.find_element_by_xpath("//span[text() = \"Секционные\"]").click()
        driver.find_element_by_xpath("//a[text() = \"RSD 02\"]").click()

    def do_action(self, act):
        action = act[0]
        label_text = act[1][0]
        text_to_do = ""
        try:
            text_to_do = act[1][1]
        except LookupError:
            pass
        if action == "checkbox":
            self.click_checkbox_by_label_text(label_text)
        elif action == "uncheckbox":
            self.unclick_checkbox_by_label_text(label_text)
        elif action == "option":
            self.click_option_by_label_text(label_text, text_to_do)
        elif action == "input":
            self.sendkeys_by_label_text(label_text, text_to_do)

    def go_next_and_assert_string(self, string_to_assert):
        self.go_next()
        self.assert_string(string_to_assert)

    def assert_string(self, string_to_assert):
        self.wait_until_jquery(30)
        self.assertIn(string_to_assert.lower(), self.strings_to_search().lower())

    def send_size_form(self):
        self.driver.find_element_by_css_selector("span.ui-button-text").click()

    def choose_first_driver(self):
        self.driver.find_element_by_css_selector("#DriveMI_ViewDirectoryDriver").click()
        self.driver.find_element_by_css_selector("#tabSourceDrive_1 a.select").click()

    def choose_first_material(self):
        self.driver.find_element_by_css_selector("#ExtraMaterialsMI_ViewDirectoryMaterials").click()
        self.driver.find_element_by_css_selector("#list_all_materials a.select").click()

    def choose_first_service(self):
        self.driver.find_element_by_css_selector("#ServiceMI_ViewDirectoryService").click()
        self.driver.find_element_by_css_selector("#list_all_service a.select").click()

    def choose_first_complectation(self):
        self.driver.find_element_by_css_selector("#AdditionalComplectationMI_ViewDirectoryComplectation").click()
        self.driver.find_element_by_css_selector("#list_all_complectation a.select").click()

    def go_next_and_assert_edit_page(self):
        self.go_next()
        self.wait_until_jquery(30)
        self.assertIn("/order/update/id/", self.driver.current_url)

    def go_next_and_assert_graphic_cards_view(self):
        self.go_next()
        self.wait_until_jquery(60)
        self.assertIn("constructor/order/graphicCardsView", self.driver.current_url)

    def draw_window(self):
        self.driver.find_element_by_css_selector("rect[id = rpanel1]").click()
        obj_count = self.driver.find_element_by_css_selector('#EmbeddedObjectsMI_ObjectCount')
        obj_count.clear()
        obj_count.send_keys('2')
        self.driver.find_element_by_xpath("//span[@class='ui-button-text'][text()='Добавить']").click()
        self.wait_until_jquery(20)

    def draw_kalitka(self):
        self.draw_window()

    def create_new_order_by_import_from_1c(self, order_id, order_year):
        self.driver.find_element_by_css_selector("a[href$=create]").click()
        self.driver.find_element_by_css_selector("a[href$=createFromSoap]").click()
        self.driver.find_element_by_css_selector("#Order1CForm_number").send_keys(order_id)
        self.driver.find_element_by_css_selector(".minict_wrapper").click()
        self.driver.find_element_by_css_selector("li[data-value='%s']" % order_year).click()
        self.driver.find_element_by_css_selector("#submit").click()

    def navigate_to_product_parameters(self):
        self.driver.find_element_by_css_selector(".popup-list-link").click()
        self.driver.find_element_by_css_selector("a[href*=readProduct]").click()

    def navigate_to_product_specification(self):
        self.driver.find_element_by_css_selector(".popup-list-link").click()
        self.driver.find_element_by_css_selector("a[href*='/order/specification/id/']").click()

    def add_new_section(self, name, code, number):
        self.driver.find_element_by_css_selector("a[onclick*='#specification-add']").click()
        self.driver.find_element_by_css_selector("#add").send_keys(name)
        self.driver.find_element_by_css_selector("input[name='SpecificationModel[code]']").send_keys(code)
        self.driver.find_element_by_css_selector("#SpecificationModel_number_packages").send_keys(number)
        self.driver.find_element_by_css_selector("a[onclick*='#add-specification-form']").click()
        self.wait_until_jquery(30)

    def choose_random_element_from_dict(self, _t):
            # self.wait_until_jquery(10)
            el_from_dict_list = self.driver.find_elements_by_xpath(
                "//ul[@class='treeview']//a[not(contains(., '___')) and not(contains(., 'goods for China'))]"
            )

            # number_to_click = random.randrange(0, len(el_from_dict_list))
            if _t:
                number_to_click = 10  # TODO some categories have no elements
            else:
                number_to_click = 0
            el_from_dict_list[number_to_click].click()
            self.wait_until_jquery(15)

            nomenclature_list = self.driver.find_elements_by_css_selector(".popup-nomenclature-table-container a")
            txt_lst = self.driver.find_elements_by_css_selector(".popup-nomenclature-table-container td:nth-of-type(3)")
            rand_num = random.randrange(0, len(nomenclature_list))
            rand_element = nomenclature_list[rand_num]
            element_text = txt_lst[rand_num].text
            rand_element.click()
            self.wait_until_jquery(10)
            return element_text

    def add_new_element_to_section(self, section_name):
        self.wait_until_jquery(15)
        self.driver.find_element_by_xpath("//a[.='%s']" % section_name).click()
        import time
        time.sleep(3)
        self.driver.find_element_by_css_selector("a.empty-add-elemnt").click()
        time.sleep(3)
        el_text = self.choose_random_element_from_dict("")
        time.sleep(3)
        self.assertTrue(len(self.driver.find_elements_by_xpath("//td[.='%s']" % el_text)) >= 1)

    def change_element_in_section(self, section_name, number_of_pieces):
        self.driver.find_element_by_css_selector("span[class*='popup-list-link']").click()
        self.driver.find_element_by_css_selector("a#specification-edit-elem-link").click()
        self.driver.find_element_by_css_selector('.minict_first').click()
        num_of_pieces = self.driver.find_element_by_css_selector("#OrderProductSpecificationModel_amount")
        num_of_pieces.clear()
        num_of_pieces.send_keys(number_of_pieces)
        self.driver.find_element_by_css_selector("a[onclick*='changeElementParameters']").click()
        self.wait_until_jquery(10)

        self.driver.find_element_by_xpath("//a[.='%s']" % section_name).click()
        self.driver.find_element_by_css_selector("span[class*='popup-list-link']").click()
        self.driver.find_element_by_css_selector("a#specification-edit-elem-link").click()
        self.wait_until_jquery(15)
        self.driver.find_element_by_css_selector('.minict_first').click()
        self.assertTrue(self.driver.find_element_by_css_selector(
            "#OrderProductSpecificationModel_amount").get_attribute("value") == number_of_pieces)

        self.driver.find_element_by_css_selector("a[onclick*='changeElementParameters']").click()

    def change_element_in_section_to_another_element(self):
        self.driver.find_element_by_css_selector("span[class*='popup-list-link']").click()
        self.driver.find_element_by_css_selector("a#specification-change-elem-nomenclature").click()
        el_text = self.choose_random_element_from_dict("1")
        self.assertTrue(len(self.driver.find_elements_by_xpath("//td[.='%s']" % el_text)) >= 1)

    def go_next_and_assert_errors_on_page(self):
        req_num = len(self.driver.find_elements_by_css_selector("span.required"))
        self.go_next()
        self.wait_until_jquery(5)
        error_num = len(
            self.driver.find_elements_by_xpath('//div[@class="errorMessage"][not(contains(@style, "none"))]'))
        self.assertEqual(req_num, error_num)

    def choose_first_analog_element(self):
        self.wait_until_jquery(5)
        element_text = self.driver.find_element_by_css_selector(
            "#specification-analog-elements-grid tr.odd:nth-of-type(1) td:nth-of-type(3)").text
        self.driver.find_element_by_css_selector(
            "#specification-analog-elements-grid tr.odd:nth-of-type(1) td:nth-of-type(5) a").click()
        changed_element = self.driver.find_element_by_css_selector("tr.group-row.constr-modified td:nth-of-type(5)")
        self.assertTrue(changed_element.text.strip() == element_text.strip())

    def delete_order(self, order_name):
        self.driver.find_element_by_css_selector("#OrderModel_number").clear()
        self.driver.find_element_by_css_selector("#OrderModel_number").send_keys(order_name)
        self.driver.find_element_by_xpath("//a[@class='filterSubmit' and .='поиск']").click()
        self.driver.find_element_by_css_selector("#yw0_c0_all").click()
        self.driver.find_element_by_xpath("//a[.='Удалить']").click()
        self.wait_until_jquery(10)
        self.assertTrue(self.driver.find_element_by_css_selector("span.empty").text == "Нет результатов.")