# -*- coding: utf-8 -*-
##############################################################################
#
# Author: DBit EIRL.
# Copyright (c) 2016 DBit ERIL.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class family_group(models.Model):
	_name = 'family.group'
	_description = 'Family Group'
	_rec_name = 'family_folio'

	################
	# GENERAL DATA #
	################
	family_folio = fields.Char('Unic National Folio', required=True)
	family_sector = fields.Many2one('sector', 'Name of Camp Name, Town, Village, or other indigenous community', required=True)
	family_score = fields.Char('Beneficiary Score')
	family_score_date = fields.Date('Score Date')
	family_informant = fields.Char('Family Authorized Informant')
	family_coord = fields.Char('Geographical Coordinates')

	############################
	# TERRITORIAL LOCALIZATION #
	############################
	family_commune_id = fields.Char('Commune ID')
	family_zone = fields.Selection([('urban','Ciudad'),('rural','Rural')], 'Zone')
	family_neighborhood_unit = fields.Char('Neighborhood Unit')
	family_name_localization = fields.Char('Name of Living Place')
	family_type_housing_gr = fields.Char('Type of Housing Group')
	family_code_housing_gr = fields.Char('ID of Housing Group')
	family_apple_code = fields.Char('Apple ID')
	family_street_code = fields.Char('Street ID')
	family_street_name = fields.Char('Street Name')
	family_address_number = fields.Char('Address Number')
	family_block = fields.Char('Block/House')
	family_department_site = fields.Char('Department/Site')
	family_dwelling_code = fields.Char('Dwelling Code')

	####################
	# DWELLING DETAILS #
	####################
	family_dwelling = fields.Text('Dwelling References')
	family_site_ownership = fields.Char('Site Ownership')
	family_dwelling_ownership = fields.Char('Dwelling Ownership')
	family_dwelling_principal = fields.Char('Principal Family of the Dwelling')
	family_dwelling_water_source = fields.Char('Dwelling Water Source')
	family_dwelling_water_distribution = fields.Char('Water Distribution on Dwelling')
	family_dwelling_excretion_system = fields.Char('Excretions Elimination System')
	family_dwelling_bathroom = fields.Char('Bathroom Use')
	family_dwelling_rooms = fields.Char('Number of Bedrooms')
	family_dwelling_people_number_nonincluded = fields.Char('Number of People non-included on the Social File')

	###################
	# FILE MANAGEMENT #
	###################
	family_income_description = fields.Text('Family Income Descriptions')

	###################
	# FILE MANAGEMENT #
	###################
	family_pollster_code = fields.Char('Pollster Code')
	family_application_date = fields.Date('File Application Date')
	family_supervisor_code = fields.Char('Supervisor Code')
	family_supervision_date = fields.Date('Communal Supervision Date')
	family_inspector_code = fields.Char('Inspector Code')
	family_review_date = fields.Date('Communal Review Date')
	family_last_update_pollster_code = fields.Char('Pollster Code')
	family_last_update_date = fields.Date('Lastest Update Date')

	##################
	# FAMILY MEMBERS #
	##################
	family_members = fields.One2many('family.group.member','member_code','Family Members')
	family_decile = fields.Char('Family Decile')
	family_quintile = fields.Char('Family Quitile')
	family_description = fields.Text('Family Description')
	family_health = fields.Text('Family Health')
	family_references = fields.Text('Family References')
	family_people_folio = fields.Char('Number of Folio People')

	_sql_constraints = [
		('folio_uniq', 'unique(family_folio)', ('This Folios already exist on the table!')),
	]
family_group()

class family_group_member(models.Model):
	_name = 'family.group.member'
	_description = 'Family Members'
	_rec_name = 'member_rut'
	_order = 'member_order, id'


	@api.model
	@api.constrains('member_rut')
	def _check_unique_rut(self):
		if self.member_rut and self.search([('id','not in',self._ids),('member_rut','=',self.member_rut)]):
			raise ValidationError(_('The Rut is already set in the system, please check it.'))

	@api.model
	def check_rut(self, rut):
		format = '%s.%s.%s-%s'

		if len(rut) < 9:
			raise ValidationError(_('The Rut isn\'t valid, please check it.'))
		if not '-' in rut:
			raise ValidationError(_('The Rut format is xxxxxxxx-x, please check it.'))

		base, vdig = rut.replace(' ','').replace('.','').split('-')
		if vdig == 'k':
			vdig = 'K'

		operar = str( 11 - sum([int(digit) * factor for digit, factor in zip(base[::-1], 2 * list(range(2,8)))]) % 11 )
		if operar == '11':
			operar = '0'
		elif operar == '10':
			operar = 'K'
		if operar != vdig:
			raise ValidationError(_('The Rut base an verification digit doesn\'t match, please check it.'))

		return format % (base[:-6], base[-6:-3], base[-3:], vdig)

	member_code = fields.Integer('code', default=0)
	member_rut = fields.Char('RUT', required=True)
	member_folio = fields.Many2one('family.group','Unic National Folio', required=True)
	member_order = fields.Integer('Family Order', required=True)
	member_head = fields.Selection([('1','uno'),
					('2','dos'),
					('3','tres'),
					('4','cuatro'),
					('5','cinco'),
					('6','seis'),
					('7','siete')], 'Head of Family', required=True)
	member_full_name = fields.Char('Full Name', required=True)
	member_date_birth = fields.Date('Date of Birth', required=True)
	member_age = fields.Integer('Age', required=True)
	member_gender = fields.Selection([('1','Male'),('2','Female')], 'Gender', required=True)
	member_nationality = fields.Char('Nationality', required=True)
	member_kinship = fields.Selection([('1','Head of Household'),\
					('2','Spounse or Partner'),\
					('3','Their Son/Daughter'),\
					('4','Only Son/Daughter of the Household Head'),\
					('5','Only Son/Daughter of the Spouse or Partner'),\
					('6','Parent'),\
					('7','Father-in-Law or Mother-in-Law'),\
					('8','Son-in-law or daughter-in-law'),\
					('9','Grandson or Granddaughter'),\
					('10','Great-Grandson or Great-Granddaughter'),\
					('11','Brother or Sister'),\
					('12','Brother-in-law or Sister-in-law'),\
					('13','Grandfather or Grandmother'),\
					('14','Another Relative'),\
					('15','Not Relative')], 'Kinship', required=True)
	member_couple = fields.Char('Couple')
	member_I1 = fields.Char('I1')
	member_I2 = fields.Char('I2')
	member_I3 = fields.Char('I3')
	member_date_of_death = fields.Date('Date of Death')

	member_hours = fields.Char('Hours', required=True)
	member_mins = fields.Char('Minutes', required=True)
	member_transport = fields.Char('Transport', required=True)

	member_S1 = fields.Char('S1')
	member_S2 = fields.Char('S2')
	member_S3 = fields.Char('S3')
	member_S4 = fields.Char('S4')
	member_S5a = fields.Char('S5a')
	member_S5b = fields.Char('S5b')
	member_S5c = fields.Char('S5c')
	member_S5d = fields.Char('S5d')
	member_S5e = fields.Char('S5e')
	member_S5f = fields.Char('S5f')
	member_S6 = fields.Char('S6')
	member_S7 = fields.Char('S7')
	member_S8a = fields.Char('S8a')
	member_S8b = fields.Char('S8b')
	member_S8c = fields.Char('S8c')
	member_S8d = fields.Char('S8d')
	member_S8e = fields.Char('S8e')

	member_E1 = fields.Char('E1')
	member_E2 = fields.Char('E2')
	member_E3 = fields.Char('E3')
	member_E4 = fields.Char('E4')

	member_O1 = fields.Char('O1')
	member_O2 = fields.Char('O2')
	member_O3 = fields.Char('O3')
	member_O4 = fields.Char('O4')
	member_O5 = fields.Char('O5')
	member_O6 = fields.Char('O6')
	member_O7 = fields.Char('O7')
	member_O8 = fields.Char('O8')
	member_O9 = fields.Char('O9')
	member_O10a = fields.Char('O10a')
	member_O10b = fields.Char('O10b')
	member_O10c = fields.Char('O10c')
	member_O10d = fields.Char('O10d')
	member_O10e = fields.Char('O10e')
	member_O10f = fields.Char('O10f')
	member_O10g = fields.Char('O10g')
	member_O11a = fields.Char('O11a')
	member_O11b = fields.Char('O11b')
	member_O11c = fields.Char('O11c')
	member_O11d = fields.Char('O11d')
	member_O11e = fields.Char('O11e')
	member_O11f = fields.Char('O11f')
	member_O11g = fields.Char('O11g')
	member_O12 = fields.Char('O12')

	member_anual_income_working = fields.Char('Anual Income Working')
	member_retirement_pension = fields.Char('Retirement or Pension')
	member_other_incomes = fields.Char('Other Incomes')
	member_administrative_pension = fields.Char('Administrative Pension')

	member_phone = fields.Char('Phone Number')
	member_marital_status = fields.Selection([('married','Married'),\
						('single','Single'),\
						('divorced','Divorced'),\
						('widow','Widow/er'),\
						('cohabitant','Cohabitant')], 'Marital Status')
	member_schooling = fields.Selection([('iliterate','Iliterate'),\
					('primary_1','1 Primary School'),\
					('primary_2','2 Primary School'),\
					('primary_3','3 Primary School'),\
					('primary_4','4 Primary School'),\
					('primary_5','5 Primary School'),\
					('primary_6','6 Primary School'),\
					('primary_7','7 Primary School'),\
					('primary_8','8 Primary School'),\
					('primary_com','Primary School Complete'),\
					('primary_unc','Primary School Uncomplete'),\
					('secondary_1','1 High School'),\
					('secondary_2','2 High School'),\
					('secondary_3','3 High School'),\
					('secondary_4','4 High School'),\
					('secondary_com','High School Complete'),\
					('secondary_unc','High School Uncomplete'),\
					('college_com','College Complete'),\
					('college_unc','College Uncomplete'),\
					('technical_com','Technical Degree Complete'),\
					('technical_unc','Technical Degree Uncomplete'),\
					('none','None')], 'Schooling')
	member_activity = fields.Selection([('student','Student'),\
					('unemployed','Unemployed'),\
					('hostess','Hostess'),\
					('in_well-child','In Well-Child'),\
					('casual_worker','Casual Worker'),\
					('stable_worker','Stable Worker')], 'Current Activity')
	member_income = fields.Integer('Income')
	member_health_insurance = fields.Selection([('fonasa_a','FONASA A'),\
						('fonasa_b','FONASA B'),\
						('fonasa_c','FONASA C'),\
						('fonasa_d','FONASA D'),\
						('fonasa_e','FONASA E'),\
						('isapre','ISAPRE'),\
						('none','None')], 'Health Insurance')
	member_suf = fields.Selection([('0','None'),\
				('1','Causante de SUF'),\
				('2','No es Causante de SUF')],'SUF') #Subsidio Unico Familiar
	member_pension = fields.Selection([('afp','AFP'),
					('state','State'),\
					('ips','IPS'),\
					('none','None')], 'Pension Assistance')
	member_situation_eva = fields.Text('Situation and Professional Evaluation')
	member_observations = fields.Text('Observations')
	member_out_of_dwelling = fields.Boolean('Sleeps Outside the Family Dwelling')
	member_reasons_outsleeping = fields.Text('Reasons of why Sleeps Outside')
	member_indigen = fields.Boolean('Belongs to an Indigen Heritage')

	@api.model
	def create(self, vals):
		if 'member_rut' in vals:
			vals.update({'member_rut':  self.check_rut(vals['member_rut'])})
		return super(family_group_member, self).create(vals)

	@api.multi
	def write(self, vals):
		rut = vals['member_rut'] if 'member_rut' in vals else self.member_rut

		if rut:
			vals.update({'member_rut': self.check_rut(rut)})
		return super(family_group_member, self).write(vals)
family_group_member()
