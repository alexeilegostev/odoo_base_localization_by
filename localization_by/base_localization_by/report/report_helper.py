# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2018 iCode (<http://icode.by>).
#
##############################################################################

import logging
from datetime import datetime
import re
import pytils
from petrovich.main import Petrovich
from petrovich.enums import Case, Gender

_logger = logging.getLogger(__name__)


class QWebHelper(object):

    def img(self, img, type='png', width=0, height=0):
        if width:
            width = "width='%spx'" % (width)
        else:
            width = " "
        if height:
            height = "height='%spx'" % (height)
        else:
            height = " "
        to_return = "<img %s %s src='data:image/%s;base64,%s' />" % (width, height, type, str(img))
        return to_return

    def number(self, name):
        if name:
            numeration = re.findall('\d+$', name)
            if numeration: return numeration[0]
        return ''

    def ru_date(self, date):
        if date and date != 'False':
            return pytils.dt.ru_strftime(u'"%d" %B %Y года', date=datetime.strptime(date, "%Y-%m-%d"), inflected=True)
        return ''

    def ru_date_short(self, date):
        if date and date != 'False':
            return pytils.dt.ru_strftime(u'"%d" %B %Y г.', date, inflected=True)
        return ''

    def ru_date2(self, date):
        if date and date != 'False':
            return pytils.dt.ru_strftime(u'%d %B %Y г.', date=datetime.strptime(date, "%Y-%m-%d %H:%M:%S"), inflected=True)
        return ''

    def calc_weight(self, invoice_line_ids=None):
        weight = 0
        for line in invoice_line_ids:
            weight += (line.product_id.weight * line.quantity)
        if weight > 0:
            return self.str_weight(weight)
        else:
            return ''

    def sheets_from_goods(self, invoice_line_ids=None):
        return '1 листе'

    def str_weight(self, weight):
        pytils.utils.check_positive(weight)
        pts = []

        if weight // 1000 > 0:
            pts.append(pytils.numeral.sum_string(int(weight // 1000), 2,
                                                 (u"тонна", u"тонны", u"тонн")))
            weight -= (weight // 1000) * 1000

        pts.append(pytils.numeral.sum_string(int(weight), 1,
                                             (u"килограмм", u"килограмма", u"килограммов")))
        remainder = pytils.numeral._get_float_remainder(weight, 3)
        iremainder = int(remainder)

        if iremainder != 0:
            # если 3.1, то это 100 грамм, а не один
            if iremainder < 10:
                iremainder *= 100
            # если 3.12, то это 120 грамм, а не двеннадцать
            if iremainder >= 10 and iremainder < 100:
                iremainder *= 10

        if iremainder != 0:
            pts.append(pytils.numeral.sum_string(iremainder, 1, (u"грамм", u"грамма", u"граммов")))

        return u" ".join(pts)

    def in_words(self, number, gender=None):
        #проверка сделана именно таким образом, чтобы в общем случае не трогать math и уйти вот остаточных артефектов при возможных float и Decimal
        if number-int(number) > 0.000001:
            return pytils.numeral.in_words(number, None)
        else:
            return pytils.numeral.in_words(int(number), None)

    def convert_name(self, name, lower=False):
        if name:
            if lower:
                employee_arr = name.lower().split()
            else:
                employee_arr = name.split()
            cased_lname = []
            p = Petrovich()
            for e in employee_arr:
                cased_lname.append(p.lastname(e, Case.GENITIVE, Gender.MALE))
            return ' '.join(map(str, cased_lname))
        else:
            return ''

    def euros(self, amount, decimal_part_digitized=False, EUR=True):
        pytils.utils.check_positive(amount)
        pts = []
        amount = round(amount, 2)
        if EUR:
            pts.append(pytils.numeral.sum_string(int(amount), 1,
                                                 (u"евро", u"евро", u"евро")))
        remainder = pytils.numeral._get_float_remainder(amount, 2)
        iremainder = int(remainder)
        if iremainder != 0:
            # если 3.1, то это 10 центов, а не один
            if iremainder < 10 and len(remainder) == 1:
                iremainder *= 10

        if decimal_part_digitized:
            if iremainder != 0:
                pts.append(str(iremainder))
            else:
                pts.append('00')
            pts.append(u"центов")
        else:
            pts.append(pytils.numeral.sum_string(iremainder, 2,
                              (u"цент", u"цента", u"центов")))

        return u" ".join(pts)

    def rubles(self, amount, decimal_part_digitized=False, BYN=False):
        pytils.utils.check_positive(amount)
        pts = []

        amount = round(amount, 2)
        if BYN:
            pts.append(pytils.numeral.sum_string(int(amount), 1,
                                                 (u"белорусский рубль", u"белорусских рубля", u"белорусских рублей")))
        else:
            pts.append(pytils.numeral.sum_string(int(amount), 1, (u"российский рубль", u"российских рубля", u"российских рублей")))
        remainder = pytils.numeral._get_float_remainder(amount, 2)
        iremainder = int(remainder)

        if iremainder != 0:
            # если 3.1, то это 10 копеек, а не одна
            if iremainder < 10 and len(remainder) == 1:
                iremainder *= 10

        if decimal_part_digitized:
            if iremainder != 0:
                pts.append(str(iremainder))
            else:
                pts.append('00')
            pts.append(u"коп.")
        else:
            pts.append(pytils.numeral.sum_string(iremainder, 2,
                              (u"копейка", u"копейки", u"копеек")))

        return u" ".join(pts)

    def rubles_BYN(self, amount, decimal_part_digitized=False):
        return self.rubles(amount, decimal_part_digitized, True)

    def in_words_with_currency(self, lang, amount, unit_name, unit_label=None, subunit_label=None, decimal_part_digitized=False):
        if unit_name == 'BYN':
            return self.rubles_BYN(amount, decimal_part_digitized)
        if unit_name == 'EUR':
            return self.euros(amount, decimal_part_digitized)
        elif unit_name == 'RUB':
            return self.rubles(amount, decimal_part_digitized)
        pts = [pytils.numeral.in_words(amount), unit_name or '']
        return u" ".join(pts)

    def initials(self, fio):
        if fio:
            return (fio.split()[0]+' '+''.join([fio[0:1]+'.' for fio in fio.split()[1:]])).strip()
        return ''

    def address(self, partner, reverse=False):
        repr = []
        address_keys = ['zip', 'state_id', 'city', 'street', 'street2', ]
        for key in address_keys if not reverse else address_keys.reverse():
            if getattr(partner, key, None) and '_id' not in getattr(partner, key, None):
                repr.append(getattr(partner, key))
            else:
                repr.append(getattr(partner, key).name)
        return ', '.join(repr)

    def bank(self, partner):
        bank = partner.env['res.partner.bank'].search([('partner_id', '=', partner.id)], limit=1)
        return bank

    def representation(self, partner):
        repr = []
        if partner.name: repr.append(partner.name)
        repr.append(self.address(partner))
        return ', '.join(repr)

    def full_representation(self, partner):
        repr = [self.representation(partner)]
        if partner.phone: repr.append(u"тел.: " + partner.phone)
        elif partner.parent_id.phone: repr.append(u"тел.: " + partner.parent_id.phone)
        bank = None
        if partner.bank_ids: bank = partner.bank_ids[0]
        elif partner.parent_id.bank_ids: bank = partner.parent_id.bank_ids[0]
        if bank and bank.acc_number: repr.append(u"р/сч " + bank.acc_number)
        if bank and bank.bank_name: repr.append(u"в банке " + bank.bank_name)
        if bank and bank.bank_bic: repr.append(u"БИК " + bank.bank_bic)
        return ', '.join(repr)
