# coding=utf-8
from __future__ import unicode_literals
from basetest import Basetest, ORDER_NAME_1C
import random
import unittest
import time
from testconfig import config
from selenium.common.exceptions import NoSuchElementException


class TestScenario1(Basetest):

    def test(self):

        order_name = ORDER_NAME_1C
        if 'debug' in config:
            order_name = "MSВДВ096701"
        print order_name
        year = "2014"

        do_action = self.do_action
        #step01

        #step02
        self.create_new_order_by_import_from_1c(order_name, year)

        #step03
        self.navigate_to_product_parameters()

        #step04
        opts = self.driver.find_elements_by_css_selector("#GateFrameMI_WicketFutureInstallation option")
        opts[random.randrange(1, len(opts))].click()
        self.go_next_and_assert_string("Тип панелей и цвет Щита")

        #step05
        do_action(["option", ["Выберите тип панелей", "Без защиты от защемления"]])
        do_action(["option", ["Выберите дизайн панелей", "Стандартная"]])
        do_action(["option", ["Выберите 2-ой дизайн панелей", "Без волны"]])
        do_action(["option", ["Выберите структуру панелей", "Нстукко - Нстукко"]])
        do_action(["option", ["Выберите внешний цвет панелей", "RAL5005"]])
        do_action(["option", ["Выберите внутренний цвет панелей", "RAL9003"]])
        do_action(["option", ["Выберите типоразмеры", "475+500+525+550+575"]])
        try:
            only_one_size_btn = self.driver.find_element_by_css_selector("#TypePanelsColorShieldMI_OnlyOneSizeSelected")
            if not only_one_size_btn.is_selected():
                only_one_size_btn.click()
            self.send_size_form()
        except NoSuchElementException:
            pass
        do_action(["option", ["Обрезать как", "Обрезаем обе панели"]])
        do_action(["option", ["Способ задания цвета снаружи", "белый"]])
        do_action(["option", ["Способ задания цвета внутри", "белый"]])
        self.go_next_and_assert_string("Облицовка молдингами")

        #step06
        # do_action(["checkbox", ["Облицовка молдингом"]])
        # self.driver.switch_to.alert.accept()
        # do_action(["checkbox", ["Автоматический подбор шага"]])
        self.go_next_and_assert_string("Встраиваемые объекты")

        #step07
        self.go_next_and_assert_string("Фальшпанель")

        #step08
        do_action(["checkbox", ["Наличие фальшпанели"]])
        self.go_next_and_assert_string("Привод")

        #step09
        self.choose_first_driver()
        self.go_next_and_assert_string("Комплектация")

        #step10
        time.sleep(3)
        self.go_next_and_assert_string("Дополнительно")

        #step11
        do_action(['option', ['Тип будущей установки привода', 'На вал']])
        # do_action(["checkbox", ["Крепление к потолку старое"]])
        # do_action(["option", ["Механизм защиты пружин", "Давать"]])
        # do_action(["option", ["Механизм защиты троса", "Защита от разрыва"]])
        # do_action(["checkbox", ["Использовать облегченные профили"]])
        # do_action(["option", ["Услуги по проему", "Формирование"]])
        # do_action(["checkbox", ["Новый торсионный механизм(если возможно)"]])
        # do_action(["checkbox", ["Комплект направляющих и угловых стоек"]])
        # do_action(["option", ["Приоритет выбора пружин", "Справа"]])
        # do_action(["checkbox", ["Выдавать только средние крышки"]])
        # do_action(["option", ["Боковая крышка", "RAL 9003"]])

        self.wait_until_jquery(15)
        self.go_next()
        # self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        # self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        self.assert_string("Расчет пружин и барабанов")

        #step12
        try:
            do_action(["option", ["Выбранные барабаны", "M203 H9570 (OMI 32)"]])
        except (NoSuchElementException, ValueError):
            print "Пружин или барабанов нет."

        do_action(["option", ["Количество пружин", "2"]])
        do_action(["option", ["Количество циклов", "10000"]])
        self.wait_until_jquery(15)
        springs = self.driver.find_elements_by_css_selector(
            "#DrumsAndSpringsCalculationMI_formSelectedSprings option")
        springs[-1].click()
        do_action(["option", ["Число валов", "1"]])
        do_action(["option", ["Выбранные валы", "25x25018"]])

        self.go_next()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        self.assert_string("Дополнительные материалы")

        #step13
        self.go_next_and_assert_string("Услуги")

        #step14
        self.go_next_and_assert_string("Информация о месте монтажа")

        #step15
        do_action(["option", ["Материал притолоки", "бетон"]])
        do_action(["option", ["Материал потолка", "бетон"]])
        do_action(["option", ["Материал стен", "бетон"]])
        self.go_next_and_assert_string("Опции")

        #step16
        self.go_next_and_assert_graphic_cards_view()

        #step17
        self.driver.find_element_by_css_selector("a[href*='/graphicCardsView/id/']").click()
        self.wait_until_jquery(30)

        #step18
        self.driver.switch_to.alert.accept()
        self.wait_until_alert(120)
        self.driver.switch_to.alert.accept()
        self.driver.find_element_by_css_selector("a[href*='/order/update/id/']").click()
        self.wait_until_jquery(30)
        self.assertIn("/order/update/id/", self.driver.current_url)

        #step19
        self.navigate_to_product_specification()

        #step20
        order_specification_url = self.driver.current_url
        section_name = "test_section"
        self.add_new_section(section_name, "00087", "2")

        #step21
        self.add_new_element_to_section(section_name)

        #step22
        self.change_element_in_section(section_name, "2")

        #step23
        # self.change_element_in_section_to_another_element()
        # TODO element doesn't changed

        # #step24
        # section = "Привод"
        # self.driver.find_element_by_xpath("//a[.='%s']" % section).click()
        # self.wait_until_jquery(15)
        # menus = self.driver.find_elements_by_css_selector("span[class*=popup-list-link]")
        # el_num = len(menus)
        # num_to_choose = random.randrange(0, el_num)
        # menus[num_to_choose].click()
        # self.driver.find_element_by_css_selector(".spec-table-nom-link.element.add-element").click()
        # name = "abcdef"
        # number = "12321"
        # type_of = "material"
        # note = "abc123"
        # checkbox_text = "Цех"
        # self.driver.find_element_by_css_selector("#OrderProductSpecificationModel_title").send_keys(name)
        # self.driver.find_element_by_css_selector(
        #     "#add-comment-forms #OrderProductSpecificationModel_amount").send_keys(number)
        # self.driver.find_elements_by_css_selector('#specification-add-comments .minict_wrapper')[0].click()
        # self.driver.find_elements_by_css_selector("li[data-value='%s']" % type_of)[-1].click()
        # self.driver.find_elements_by_css_selector('#specification-add-comments .minict_wrapper')[1].click()
        # self.driver.find_elements_by_xpath("//li[.='%s']" % section)[-1].click()
        # time.sleep(5)
        # self.driver.find_element_by_css_selector("#OrderProductSpecificationModel_notation").send_keys(note)
        # self.driver.find_elements_by_css_selector('.ui-multiselect')[-1].click()
        # self.driver.find_element_by_xpath("//label/span[.='%s']/../input" % checkbox_text).click()
        # self.driver.find_element_by_css_selector("a#Ajax").click()
        # self.wait_until_jquery(30)
        #
        # self.assertTrue(len(self.driver.find_elements_by_xpath("//td[contains(text(), '%s')]" % name)) == 1)
        # self.assertTrue(len(self.driver.find_elements_by_xpath("//td[contains(text(), '%s')]" % number)) == 1)

        # step25
        from download_file_req import check_csv_file
        self.assertTrue(check_csv_file(order_specification_url))

        #step26
        self.driver.find_element_by_css_selector("a[onclick*='#saveOrder']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        time.sleep(1)

        #step27
        self.driver.find_element_by_css_selector("#transferTo1C").click()
        # TODO unexpected alert
        time.sleep(1)

        #step28
        self.driver.find_element_by_css_selector("#outSavePager").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Уйти со страницы']").click()
        time.sleep(1)
        self.driver.find_element_by_css_selector("#transferTo1C").click()
        time.sleep(1)

        #step29
        self.driver.find_element_by_css_selector("span[class*=popup-list-link]").click()
        self.driver.find_element_by_css_selector("a[onclick*='#deleteProduct']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()
        self.driver.find_element_by_css_selector("a[onclick*='#saveOrder']").click()
        self.driver.find_element_by_xpath("//span[@class='ui-button-text' and .='Да']").click()

        #step30
        self.driver.find_element_by_css_selector("a[onclick*='#outOrder']").click()
        self.driver.find_elements_by_xpath("//span[@class='ui-button-text' and .='Да']")[-1].click()

        #step31
        self.delete_order(order_name)


if __name__ == '__main__':
    unittest.main()