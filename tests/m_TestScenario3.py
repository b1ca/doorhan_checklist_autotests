# coding=utf-8
from __future__ import unicode_literals
import random
import unittest
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoAlertPresentException
from basetest import Basetest, PRODUCT_TYPE
import time


class TestScenario3(Basetest):

    def test(self):

        do_action = self.do_action
        #step01

        #step02
        self.driver.find_element_by_css_selector("a[href$='order/create']").click()

        #step03
        order_name = 'NewOrder' + str(random.randrange(0, 10000))
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
        self.driver.find_element_by_xpath("//span[text() = \"Гаражные\"]").click()
        self.driver.find_element_by_xpath("//span[text() = \"Секционные\"]").click()
        self.driver.find_element_by_xpath("//a[text() = '%s']" % PRODUCT_TYPE).click()
        self.go_next_and_assert_string("Проем")

        #step05
        do_action(["input", ["Ширина проема", "2000"]])
        do_action(["input", ["Высота проема", "2000"]])
        do_action(["input", ["Притолока", "500"]])
        do_action(["input", ["Расстояние слева", "300"]])
        do_action(["input", ["Расстояние справа", "300"]])
        do_action(["input", ["Глубина гаража", "5000"]])
        do_action(["input", ["Максимальная притолока", "5000"]])
        do_action(["option", ["Тип подъема", "Стандартный наклонный"]])
        do_action(["option", ["Установка профиля для щита", "Калитка v2"]])
        self.go_next_and_assert_string("Дополнительные параметры проема")

        #step06
        do_action(["option", ["Ввод угла/размеров наклона", "Угла"]])
        self.go_next_and_assert_string("Тип панелей и цвет Щита")

        #step07
        do_action(["checkbox", ["Алюминиевая облицовка"]])
        do_action(["option", ["Выберите тип панелей", "Без защиты от защемления"]])
        do_action(["option", ["Выберите дизайн панелей", "Стандартная"]])
        do_action(["option", ["Выберите 2-ой дизайн панелей", "Без волны"]])
        do_action(["option", ["Выберите структуру панелей", "Нстукко - Нстукко"]])
        do_action(["option", ["Выберите внешний цвет панелей", "RAL8014"]])
        do_action(["option", ["Выберите внутренний цвет панелей", "RAL9003"]])
        do_action(["option", ["Выберите типоразмеры", "500"]])
        self.send_size_form()
        do_action(["option", ["Обрезать как", "Обрезаем обе панели"]])
        do_action(["option", ["Способ задания цвета снаружи", "вручную"]])
        do_action(["option", ["Способ задания цвета внутри", "вручную"]])
        self.go_next_and_assert_string("Параметры облицовки")

        #step08
        do_action(["option", ["Вариант облицовки", "Вариант 1"]])
        do_action(["option", ["Расположение рисунка", "По центру"]])
        self.wait_until_jquery(5)
        self.go_next_and_assert_string("Встраиваемые объекты")

        #step09
        do_action(["option", ["Тип объекта", "Окна"]])
        do_action(["option", ["Объект", "DH 452x302 белое"]])
        self.draw_window()
        self.go_next_and_assert_string("Фальшпанель")

        #step10
        do_action(["checkbox", ["Наличие фальшпанели"]])
        do_action(["option", ["Окантовка", "Профиль 80043 + Швеллер 50х40"]])
        self.go_next_and_assert_string("Привод")

        #step11
        self.choose_first_driver()
        self.driver.find_elements_by_css_selector('.check_drive_enabled')[-1].click()
        self.go_next_and_assert_string("Комплектация")

        #step12
        time.sleep(3)
        self.go_next_and_assert_string("Дополнительно")

        #step13
        do_action(["option", ["Тип будущей установки привода", "На вал"]])
        do_action(["option", ["Тип амортизаторов", "Укороченные"]])
        do_action(["option", ["Механизм защиты пружин", "Давать"]])
        do_action(["option", ["Механизм защиты троса", "Устройство безопасности"]])
        do_action(["uncheckbox", ["Использовать облегченные профили"]])
        do_action(["option", ["Услуги по проему", "Формирование"]])
        do_action(["checkbox", ["Принудительно резать вал"]])
        do_action(["option", ["Сторона установки привода", "Слева"]])
        do_action(["option", ["Приоритет выбора пружин", "Слева"]])
        do_action(["checkbox", ["Уплотнение проема"]])
        do_action(["uncheckbox", ["Выдавать только средние крышки"]])
        do_action(["uncheckbox", ["Использовать \"короткие изгибы\""]])
        do_action(["uncheckbox", ["Использовать соединительные пластины под клепатель"]])
        do_action(["uncheckbox", ["Использовать соединительные пластины"]])
        # self.go_next_and_assert_string("Расчет пружин и барабанов")
        self.go_next()
        try:
            self.wait_until_alert(10)
            self.driver.switch_to.alert.accept()
        except TimeoutException:
            pass
        self.assert_string("Расчет пружин и барабанов")
        #step14
        try:
            do_action(["option", ["Выбранные барабаны", "M102 H3250 (OMI 12)"]])
            do_action(["option", ["Количество пружин", "2"]])
            do_action(["option", ["Количество циклов", "12500"]])
        except (NoSuchElementException, ValueError):
            print "Пружин или барабанов нет."
        try:
            springs = self.driver.find_elements_by_css_selector(
                "#DrumsAndSpringsCalculationMI_formSelectedSprings option")
            springs[-1].click()
        except ValueError:
            print "can't choose last spring."
        do_action(["option", ["Число валов", "1"]])
        do_action(["option", ["Выбранные валы", "25x25516"]])
        # self.go_next_and_assert_string("Дополнительные материалы")

        self.wait_until_jquery(10)
        self.go_next()
        try:
            self.driver.implicitly_wait(2)
            self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
            self.driver.implicitly_wait(10)
        except NoSuchElementException:
            self.driver.implicitly_wait(10)
        self.assert_string("Дополнительные материалы")

        #step15
        self.go_next_and_assert_string("Услуги")

        #step16
        self.go_next_and_assert_string("Информация о месте монтажа")

        #step17
        do_action(["option", ["Материал притолоки", "бетон"]])
        do_action(["option", ["Материал потолка", "металл"]])
        do_action(["option", ["Материал стен", "кирпич"]])
        self.go_next_and_assert_string("Опции")

        #step18
        self.go_next_and_assert_graphic_cards_view()

        #step19
        self.driver.find_element_by_css_selector("a[href*='order/update/id']").click()
        self.driver.find_element_by_css_selector("a[onclick*='#saveOrder']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        self.wait_until_jquery(5)
        #self.driver.find_element_by_css_selector("a[href*='order/graphicCardsView/id/']").click()
        #try:
           #self.driver.switch_to.alert.accept()
        #except NoAlertPresentException:
            #pass
        #self.wait_until_alert(120)
        #self.driver.switch_to.alert.accept()

        #self.driver.find_element_by_css_selector("a[onclick*='#saveOrder']").click()
        #self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        #self.wait_until_jquery(5)

        #step20
        self.driver.find_element_by_css_selector("a[onclick*='#outOrder']").click()
        self.driver.find_elements_by_xpath("//span[@class='ui-button-text' and .='Да']")[-1].click()

        #step21
        self.driver.find_element_by_css_selector("#OrderModel_number").send_keys(order_name)
        self.driver.find_element_by_xpath("//a[@class='filterSubmit' and .='поиск']").click()

        self.driver.find_element_by_xpath('//a[.="%s"]' % order_name).click()
        self.driver.find_element_by_css_selector("span[class*=popup-list-link]").click()
        self.driver.find_element_by_css_selector("a[onclick*='#deleteProduct']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        self.driver.find_element_by_css_selector("a[onclick*='#saveOrder']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        self.driver.find_element_by_css_selector("a[onclick*='#outOrder']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()

        self.delete_order(order_name)

if __name__ == '__main__':
    unittest.main()