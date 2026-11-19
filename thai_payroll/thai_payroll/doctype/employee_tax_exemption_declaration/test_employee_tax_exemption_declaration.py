# Copyright (c) 2026, Kitti U. and Contributors
# See license.txt

from frappe.tests.utils import FrappeTestCase

from thai_payroll.custom.employee_tax_exemption_declaration import get_joining_month_adjustment


class TestYearlySalaryMidMonthJoiner(FrappeTestCase):
	"""Issue #8: a mid month joiner loses part of a month in the ctc projection.

	Nov 2026 has 21 working days. 16 Nov to 30 Nov is 11 of them, 10 Nov to 30 Nov is 15.
	A monthly salary of 10,000 gives 476.19 per working day.
	"""

	def test_join_16_nov_out_of_30_day_style_structure(self):
		# ctc counted a whole joining month (10,000), rem rounds down and drops December
		adjustment = get_joining_month_adjustment(
			month_full=10000,
			prorated_current=10000,
			share=11 / 21,
			remaining_sub_periods=1.4,
		)
		self.assertAlmostEqual(10000 + adjustment, 15238.10, places=2)

	def test_join_10_nov_out_of_30_day_style_structure(self):
		# ctc counted joining month plus December, rem rounds up so no month is lost
		adjustment = get_joining_month_adjustment(
			month_full=10000,
			prorated_current=10000,
			share=15 / 21,
			remaining_sub_periods=1.6,
		)
		self.assertAlmostEqual(20000 + adjustment, 17142.86, places=2)

	def test_payment_day_based_structure_only_gets_the_lost_month(self):
		# the joining month is already prorated by Frappe HR, only December is missing
		adjustment = get_joining_month_adjustment(
			month_full=10000,
			prorated_current=10000 * 11 / 21,
			share=11 / 21,
			remaining_sub_periods=1.4,
		)
		self.assertAlmostEqual(10000 * 11 / 21 + adjustment, 15238.10, places=2)

	def test_no_adjustment_when_the_fraction_does_not_round_down(self):
		adjustment = get_joining_month_adjustment(
			month_full=10000,
			prorated_current=10000,
			share=11 / 21,
			remaining_sub_periods=2.0,
		)
		self.assertAlmostEqual(adjustment, 10000 * (11 / 21) - 10000, places=2)

	def test_full_year_employee_is_untouched(self):
		adjustment = get_joining_month_adjustment(
			month_full=10000,
			prorated_current=10000,
			share=1,
			remaining_sub_periods=12,
		)
		self.assertEqual(adjustment, 0)
