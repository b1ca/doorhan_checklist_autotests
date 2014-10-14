# coding=utf-8
from __future__ import unicode_literals
import random
import unittest
from selenium.common.exceptions import NoSuchElementException
from basetest import Basetest
import time


class TestScenario2(Basetest):

    def test(self):

        do_action = self.do_action
        #step01

        #step02
        self.driver.find_element_by_css_selector("a[href$='order/create']").click()
        self.driver.find_element_by_css_selector("#submit").click()
        self.assertTrue(
            len(self.driver.find_elements_by_xpath(
                "//div[@class='errorMessage' and not(contains(@style, 'display'))]")) == 6
        )

        #step03
        order_name = 'NewOrder' + str(random.randrange(0, 10000))
        print 'order_name = %s' % order_name
        self.driver.find_element_by_xpath(
            '//span[contains(text(),"Менеджер")]/..//div[@class="minict_wrapper"]').click()
        self.driver.find_element_by_xpath('//span[contains(text(),"Менеджер")]/..//li[.="Anders A.A."]').click()
        self.driver.find_element_by_css_selector("#OrderModel_number").send_keys(order_name)
        self.driver.find_element_by_css_selector("#CustomerModel_name").send_keys('Фамилия')
        self.driver.find_element_by_css_selector("#CustomerModel_phone").send_keys('1111111')
        self.driver.find_element_by_css_selector("#CustomerModel_address").send_keys('Адрес')

        time.sleep(3)

        self.driver.find_element_by_css_selector("#OrderModel_measurementDate").click()
        self.driver.find_element_by_css_selector(".ui-datepicker-calendar tr:nth-of-type(2) td:nth-of-type(4)").click()

        self.driver.find_element_by_css_selector("#OrderModel_productionDate").click()
        self.driver.find_element_by_css_selector(".ui-datepicker-calendar tr:nth-of-type(2) td:nth-of-type(4)").click()

        self.driver.find_element_by_css_selector("#OrderModel_installationDate").click()
        self.driver.find_element_by_css_selector(".ui-datepicker-calendar tr:nth-of-type(2) td:nth-of-type(4)").click()

        self.driver.find_element_by_css_selector("#submit").click()

        #step04
        self.driver.find_element_by_css_selector('a[href*="addProduct"]').click()
        self.wait_until_jquery(5)
        self.driver.find_element_by_css_selector("#next").click()
        alert = self.driver.switch_to.alert
        self.assertTrue(alert.text == 'Необходимо выбрать изделие!')
        alert.accept()

        #step05
        self.driver.find_element_by_xpath("//span[text() = \"Гаражные\"]").click()
        self.driver.find_element_by_xpath("//span[text() = \"Секционные\"]").click()
        self.driver.find_element_by_xpath("//a[text() = \"RSD 02\"]").click()
        self.go_next_and_assert_string("Проем")

        #step06
        self.go_next_and_assert_errors_on_page()

        #step07
        do_action(["input", ["Ширина проема", "2000"]])
        do_action(["input", ["Высота проема", "2000"]])
        do_action(["input", ["Притолока", "1000"]])
        do_action(["input", ["Расстояние слева", "500"]])
        do_action(["input", ["Расстояние справа", "500"]])
        do_action(["input", ["Глубина гаража", "10000"]])
        do_action(["option", ["Тип подъема", "Стандартный"]])
        do_action(["option", ["Будущая установка калитки", "Hет"]])
        self.go_next_and_assert_string("Тип панелей и цвет Щита")

        #step08

        #step09
        do_action(["option", ["Выберите тип панелей", "Без защиты от защемления"]])
        do_action(["option", ["Выберите дизайн панелей", "Стандартная"]])
        do_action(["option", ["Выберите 2-ой дизайн панелей", "Волна"]])
        do_action(["option", ["Выберите структуру панелей", "Гладкая - Нстукко"]])
        do_action(["option", ["Выберите внешний цвет панелей", "ALDER"]])
        self.send_size_form()
        do_action(["option", ["Обрезать как", "Обрезаем обе панели"]])
        do_action(["option", ["Способ задания цвета снаружи", "белый"]])
        do_action(["option", ["Способ задания цвета внутри", "белый"]])
        self.go_next_and_assert_string("Облицовка молдингами")

        #step10
        do_action(["checkbox", ["Облицовка молдингом"]])
        self.driver.switch_to.alert.accept()
        do_action(["checkbox", ["Автоматический подбор шага"]])
        do_action(["option", ["Вариант облицовки", "вариант 2"]])
        do_action(["option", ["Цвет облицовки", "металлик"]])
        self.go_next_and_assert_string("Встраиваемые объекты")

        #step11
        self.go_next_and_assert_string("Фальшпанель")

        #step12
        do_action(["checkbox", ["Наличие фальшпанели"]])
        self.go_next_and_assert_string("Привод")

        #step13
        self.choose_first_driver()
        self.driver.find_elements_by_css_selector('.check_drive_enabled')[-1].click()
        self.go_next_and_assert_string("Комплектация")

        #step14
        time.sleep(3)
        self.go_next_and_assert_string("Дополнительно")

        #step15
        do_action(["option", ["Тип будущей установки привода", "Потолочный"]])
        do_action(["option", ["Тип амортизаторов", "Удлиненные"]])
        do_action(["option", ["Механизм защиты пружин", "Давать"]])
        do_action(["option", ["Механизм защиты троса", "Защита от разрыва"]])
        do_action(["option", ["Услуги по проему", "Окантовка"]])
        do_action(["option", ["Сторона установки привода", "Справа"]])
        do_action(["option", ["Приоритет выбора пружин", "Справа"]])

        self.go_next_and_assert_string("Расчет пружин и барабанов")

        #step16
        try:
            do_action(["option", ["Выбранные барабаны", "M102 H2250 (OMI 8)"]])
            do_action(["option", ["Количество пружин", "2"]])
            do_action(["option", ["Количество циклов", "10000"]])
            springs = self.driver.find_elements_by_css_selector(
                "#DrumsAndSpringsCalculationMI_formSelectedSprings option")
            # springs[random.randrange(1, len(springs))].click()
            springs[-1].click()
        except (NoSuchElementException, ValueError):
            print "Пружин или барабанов нет."
        do_action(["option", ["Число валов", "1"]])
        do_action(["option", ["Выбранные валы", "25x25018"]])

        self.go_next()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        self.assert_string("Дополнительные материалы")

        #step17
        self.go_next_and_assert_string("Услуги")

        #step18
        self.go_next_and_assert_string("Информация о месте монтажа")

        #step19
        do_action(["option", ["Материал притолоки", "бетон"]])
        do_action(["option", ["Материал потолка", "бетон"]])
        do_action(["option", ["Материал стен", "бетон"]])
        self.go_next_and_assert_string("Опции")

        #step20
        self.go_next_and_assert_graphic_cards_view()

        #step21
        self.driver.find_element_by_css_selector("a[href*='order/graphicCardsView/id/']").click()
        self.driver.switch_to.alert.accept()
        self.wait_until_alert(120)
        self.driver.switch_to.alert.accept()
        self.driver.find_element_by_css_selector("a[onclick*='#saveOrder']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        self.wait_until_jquery(5)
        self.driver.find_element_by_css_selector("a[href*='/order/update/id/']").click()

        #step22
        self.driver.find_element_by_css_selector("span[class*=popup-list-link]").click()
        self.driver.find_element_by_css_selector('a[href*="/specification/"]').click()
        self.driver.find_element_by_css_selector("span[class*=popup-list-link]").click()
        self.driver.find_element_by_css_selector("a[onclick*='#specification-analog-elements']").click()
        self.choose_first_analog_element()

        #step23
        self.wait_until_jquery(5)
        self.driver.find_element_by_css_selector("a[onclick*='#saveOrder']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        self.wait_until_jquery(15)
        self.driver.find_element_by_css_selector("#outSavePager").click()
        self.driver.find_element_by_css_selector("span[class*=popup-list-link]").click()
        self.driver.find_element_by_css_selector('a[href*="/specification/"]').click()

        #step24
        self.driver.find_element_by_css_selector('.breadcrumbs a[href*="update"]').click()

        #step25
        # self.driver.find_element_by_css_selector("span[class*=popup-list-link]").click()
        # self.driver.find_element_by_css_selector("a[href*=readProduct]").click()
        #
        # while 'steps' in self.driver.current_url:
        #     self.go_next()
        #     self.wait_until_jquery(30)
        #     try:
        #         self.driver.switch_to.alert.accept()
        #     except NoAlertPresentException:
        #         print 'alert'

        #step26
        #TODO waste step.

        #step27
        #TODO waste step.

        #step28
        #TODO broken.

        #step29
        self.driver.find_element_by_css_selector("span[class*=popup-list-link]").click()
        self.driver.find_element_by_css_selector("a[onclick*='#deleteProduct']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        self.driver.find_element_by_css_selector("a[onclick*='#saveOrder']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()

        #step30
        self.driver.find_element_by_css_selector("a[onclick*='#outOrder']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()

        #step31
        self.driver.find_element_by_css_selector("#OrderModel_number").send_keys(order_name)
        self.driver.find_element_by_xpath("//a[@class='filterSubmit' and .='поиск']").click()
        self.driver.find_element_by_xpath('//a[.="%s"]' % order_name).click()

        #step32
        self.driver.find_elements_by_css_selector('a.select2-choice')[0].click()
        self.driver.find_element_by_xpath("//div[@class='select2-result-label' and .='Смирнов Р.В.']").click()
        self.driver.find_elements_by_css_selector('a.select2-choice')[1].click()
        self.driver.find_element_by_xpath("//div[@class='select2-result-label' and .='Говоров Д.С.']").click()
        self.driver.find_elements_by_css_selector('a.select2-choice')[2].click()
        self.driver.find_element_by_xpath("//div[@class='select2-result-label' and .='2013']").click()
        new_order_name = 'NewOrder' + str(random.randrange(0, 10000))
        print 'new_order_name = %s' % new_order_name
        self.driver.find_element_by_css_selector("#OrderModel_number").clear()
        self.driver.find_element_by_css_selector("#OrderModel_number").send_keys(new_order_name)

        self.driver.find_element_by_css_selector("#CustomerModel_name").send_keys('2')
        self.driver.find_element_by_css_selector("#CustomerModel_phone").clear()
        self.driver.find_element_by_css_selector("#CustomerModel_phone").send_keys('2222222')
        self.driver.find_element_by_css_selector("#CustomerModel_address").send_keys('2')
        self.driver.find_element_by_css_selector("#datekeeper1").click()
        self.driver.find_element_by_css_selector(".ui-datepicker-calendar tr:nth-of-type(3) td:nth-of-type(4)").click()
        self.driver.find_element_by_css_selector("#datekeeper2").click()
        self.driver.find_element_by_css_selector(".ui-datepicker-calendar tr:nth-of-type(3) td:nth-of-type(4)").click()
        self.driver.find_element_by_css_selector("#datekeeper3").click()
        self.driver.find_element_by_css_selector(".ui-datepicker-calendar tr:nth-of-type(3) td:nth-of-type(4)").click()

        #step33
        self.driver.find_element_by_css_selector("a[onclick*='#saveOrder']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        self.driver.find_element_by_css_selector("a[onclick*='#outOrder']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()

        self.driver.find_element_by_css_selector('#OrderModel_number').clear()
        self.driver.find_element_by_css_selector('#OrderModel_number').send_keys(new_order_name)
        self.driver.find_element_by_xpath("//a[@class='filterSubmit' and .='поиск']").click()
        self.driver.find_element_by_xpath('//a[.="%s"]' % new_order_name).click()

        self.assertTrue(
            self.driver.find_elements_by_css_selector('span.select2-chosen')[0].text == 'Смирнов Р.В.'
        )
        self.assertTrue(
            self.driver.find_elements_by_css_selector('span.select2-chosen')[1].text == 'Говоров Д.С.'
        )
        self.assertTrue(
            self.driver.find_elements_by_css_selector('span.select2-chosen')[2].text == '2013'
        )
        self.assertTrue(
            self.driver.find_element_by_css_selector('#OrderModel_number').get_attribute('value') == new_order_name
        )
        self.assertTrue(
            self.driver.find_element_by_css_selector('#CustomerModel_name').get_attribute('value') == 'Фамилия2'
        )
        self.assertTrue(
            self.driver.find_element_by_css_selector('#CustomerModel_phone').get_attribute('value') == '2222222'
        )
        self.assertTrue(
            self.driver.find_element_by_css_selector('#CustomerModel_address').get_attribute('value') == 'Адрес2'
        )

        #step34
        self.driver.find_element_by_css_selector('.breadcrumbs a').click()

        #step35
        self.delete_order(new_order_name)


if __name__ == '__main__':
    unittest.main()