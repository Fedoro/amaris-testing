# -*- coding: utf-8 -*-
####################################################################
#	APPLICATION FORM FOR STOCK ON SOCIAL HELP MANAGEMENT, CHILE.
#		Created and Designed by:
#			David Acevedo (dacevedo@stratanet.cl)
#			Diego Cantos (dcantos@stratanet.cl)
#	 	www.stratanet.cl
####################################################################
# Se modifican los campos a la version odoo12
# Se eliminan los default que se encontraban aparte y se agregan al campo que les corresponde
# Se reemplazan los pool.get por el nuevo formato de odoo12 Self.env[].
#




import datetime, addons
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class social_help_voucher_item(models.Model):
	_name = 'social.help.voucher.item'
	_description = 'Social Report Item Reference'
	_rec_name = 'company_id'


	table_id = fields.Integer('Id', required=True, readonly=False)
	company_id = fields.Many2one('res.company', 'Name', required=True, readonly=False, default=lambda self: self.env.user.company_id)
	item_id = fields.Many2one('social.help.stock.items', 'Item Id', required=True, readonly=False)

	amount = fields.Integer('Requested Amount', required=True, readonly=False)
	def create(self, cr, user, vals, context=None):
		if 'item_id' in vals:
			amount = vals['amount']
			item_id = vals['item_id']

			virtual_amount = self.env['social.help.stock.items'].browse(cr, user, item_id, context=context).virtual_amount
			virtual_amount -= amount

			if virtual_amount < 0:
				raise ValidationError(_('Error!'),_('You do not have the number of items requested to be delivered'))
			else:
				self.env['social.help.stock.items'].write(cr, user, item_id, {'virtual_amount': virtual_amount})

			res = super(social_help_voucher_item, self).create(cr, user, vals, context=context)
			return res
		else:
			res = super(social_help_voucher_item, self).create(cr, user, vals, context=context)
			return res


social_help_voucher_item()

class social_sector(models.Model):
	_name = 'social.sector'
	_descripcion = 'Sectors of the Place'


	name = fields.Char('Sector Name', size=64, required=True)
	code = fields.Char('Sector Code', size=5, default=0, required=True)
	count = fields.Char('Amount of helps', size=20, default=0, required=True, readonly=False)


	def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=80):
		if not args:
			args = []
		if not context:
			context = {}
		ids = self.search(cr, user, [('code', operator, name)] + args, limit=limit, context=context)

		if not ids:
			ids = self.search(cr, user, [('name', operator, name)] + args, limit=limit, context=context)
		return self.name_get(cr, user, ids, context)

social_sector()

class social_family_group(models.Model):
	_name = 'social.family.group'
	_descripcion = 'Family Group'
	_rec_name = 'family_folio'


	family_folio = fields.Char('Unic National Folio', size=30, required=True, readonly=False)
	family_jjvv = fields.Char('JJ.VV', size=60, required=False, readonly=False)
	family_sector = fields.Many2one('social.sector', 'Sector', required=True, readonly=False)
	family_score = fields.Char('Beneficiary Score', size=25, required=False, readonly=False)
	family_coord = fields.Char('Geographical Coordinates', size=10, required=False, readonly=False)
	family_total_income = fields.Integer('Total Income', size=10, required=False, readonly=False)
	family_percapita_income = fields.Integer('Percapita Income', size=10, required=False, readonly=False)
	family_dwelling = fields.Text('Beneficiary Dwelling', required=False, readonly=False)
	family_income_description = fields.Text('Income', required=False, readonly=False)
	family_num_men = fields.Integer('Men', required=False, readonly=False)
	family_num_women = fields.Integer('Women', required=False, readonly=False)
	family_num_children = fields.Integer('Children', required=False, readonly=False)
	family_total_num = fields.Integer('Total', required=False, readonly=False)
social_family_group()

class social_family_group_member(models.Model):
	_name = 'social.family.group.member'
	_description = 'Family Members'
	_rec_name = 'member_rut'


	member_rut = fields.Char('RUT', size=32, readonly=False, required=True)
	member_folio = fields.Many2one('social.family.group','Unic National Folio', required=True, readonly=False)
	member_full_name = fields.Char('Full Name', size=32, readonly=False, required=True)
	member_gender = fields.Selection([('masculino','Male'),('femenino','Female')], 'Gender', required=True, readonly=False)
	member_age = fields.Integer('Age', required=True, readonly=False)
	member_date_birth = fields.Date('Date of Birth', required=True, readonly=False)
	member_address = fields.Char('Address', size=60, required=True, readonly=False)
	member_phone = fields.Char('Phone Number', size=25, required=True, readonly=False)
	member_kinship = fields.Char('Kinship', size=15, required=False, readonly=False)
	member_marital_status = fields.Selection([
			('married','Married'),
			('single','Single'),
			('divorced','Divorced'),
			('widow','Widow/er'),
			('cohabitant','Cohabitant')], 'Marital Status', required=True, readonly=False)
	member_schooling = fields.Selection([
			('primary_com','Primary School Complete'),
			('primary_unc','Primary School Uncomplete'),
			('secondary_com','High School Complete'),
			('secondary_unc','High School Uncomplete'),
			('college_com','College Complete'),
			('college_unc','College Uncomplete'),
			('technical_com','Technical Degree Complete'),
			('technical_unc','Technical Degree Uncomplete'),
			('none','None')], 'Schooling', required=True, readonly=False)
	member_activity = fields.Char('Current Activity', size=25, required=False, readonly=False)
	member_income = fields.Integer('Income', size=10, required=True, readonly=False)
	member_health = fields.Text('Beneficiary Health', required=False, readonly=False)
	member_health_insurance = fields.Selection([
			('fonasa','FONASA'),
			('isapre','ISAPRE'),
			('none','None')], 'Health Insurance', required=True, readonly=False)
	member_suf = fields.Char('SUF', size=25, required=False, readonly=False) #Subsidio Unico Familiar
	member_pension = fields.Selection([
			('afp','AFP'),
			('state','State'),
			('isp','ISP'),
			('none','None')], 'Pension Assistance', required=True, readonly=False)
	member_situation_eva = fields.Text('Situation and Professional Evaluation', required=False, readonly=False)
	member_observations = fields.Text('Observations', required=False, readonly=False)


	def check_run(self, body, vdig):
		try:
			operar = (range(10) + ['k'])[11-sum([int(digit)*factor for digit,factor in zip(body[::-1],2*range(2,8))])%11]
			try:
				if operar == int(vdig):
					return True
				else:
					return False
			except ValueError:
				if operar == vdig.lower():
					return True
				else:
					return False
		except IndexError:
			return False

	def _check(self, cr, uid, ids):
		obj = self.browse(cr, uid, ids)

		for record in obj:
			if record.member_rut:
				try:
					body, vdig = record.member_rut.split('-')
					if not self.check_run(body, vdig):
						raise osv.ValidationError(_('Error!'),_("Insert a valid RUT in the field 'RUT'"))
				except ValueError:
					raise ValidationError(_('Error!'),_("Insert a valid RUT in the field 'RUT'"))

				return True

	_sql_constraints = [('rut_uniq', 'unique (member_rut)', _('The Rut is already in the records!'))]

	_constraints = [
		(_check, '', ['']),
	]
social_family_group_member()


class social_help_voucher(models.Model):
	_name = 'social.help.voucher'
	_description = 'Social Report Form'
#	_rec_name = 'voucher_code'

	def _search_family_group(self, cr, uid, ids, field_name, arg, context=None):
		"""
		@param cr: the current row, from the database cursor,
		@param uid: the current user’s ID for security checks,
		@param ids: List of create menu’s IDs
		@param context: A standard dictionary for contextual values """

		res = {}

		for id in ids:
			res[id] = {
				'family_jjvv': False,
				'family_score': False,
				'family_sector': False,
				'family_total_income': False,
				'family_percapita_income': False,
				'family_dwelling': False,
				'family_income_description': False,
				'family_num_men': False,
				'family_num_women': False,
				'family_num_children': False,
				'family_total_num': False
			}

		if not ids:
			return res
		else:
			cr.execute("SELECT v.id, g.family_jjvv, g.family_score, s.name, g.family_total_income, g.family_percapita_income, \
					g.family_dwelling, g.family_income_description, g.family_num_men, g.family_num_women, \
					g.family_num_children, g.family_total_num from social_family_group as g \
					inner join social_help_voucher as v on (g.id = v.family_id) \
					inner join social_sector as s on (s.id = g.family_sector) \
					where v.id IN %s \
					order by v.id;",(tuple(ids),))

			for id, family_jjvv, family_score, name, family_total_income, family_percapita_income, family_dwelling,\
				family_income_description, family_num_men, family_num_women, family_num_children,\
				family_total_num in cr.fetchall():
				res[id]['family_jjvv'] = family_jjvv
				res[id]['family_score'] = family_score
				res[id]['family_sector'] = name
				res[id]['family_total_income'] = family_total_income
				res[id]['family_percapita_income'] = family_percapita_income
				res[id]['family_dwelling'] = family_dwelling
				res[id]['family_income_description'] = family_income_description
				res[id]['family_num_men'] = family_num_men
				res[id]['family_num_women'] = family_num_women
				res[id]['family_num_children'] = family_num_children
				res[id]['family_total_num'] = family_total_num
			return res

	def _search_family_member(self, cr, uid, ids, field_name, arg, context=None):
		"""
		@param cr: the current row, from the database cursor,
		@param uid: the current user’s ID for security checks,
		@param ids: List of create menu’s IDs
		@param context: A standard dictionary for contextual values """

		res = {}

		for id in ids:
			res[id] = {
				'member_full_name': False,
				'member_address': False,
				'member_phone': False,
				'member_health': False,
				'member_situation_eva': False,
				'member_age': False,
			}

		if not ids:
			return res
		else:
			cr.execute("SELECT v.id, m.member_full_name, m.member_address, m.member_phone, m.member_health, \
					m.member_situation_eva, m.member_age from social_family_group_member as m \
					inner join social_help_voucher as v on (m.id = v.member_id) \
					where v.id IN %s \
					order by v.id;",(tuple(ids),))

			for id, member_full_name, member_address, member_phone, member_health, member_situation_eva, member_age in cr.fetchall():
				res[id]['member_full_name'] = member_full_name
				res[id]['member_address'] = member_address
				res[id]['member_phone'] = member_phone
				res[id]['member_health'] = member_health
				res[id]['member_situation_eva'] = member_situation_eva
				res[id]['member_age'] = member_age
			return res

		company_id = fields.Many2one('res.company', 'Company', required=False, readonly=False, default=lambda self: self.env.user.company_id)
		voucher_code = fields.Integer('Social Report Code', readonly=True, required=True, compute='_value')
		statement = fields.Integer('Statement Code', readonly=False, required=True,
			help="0 if the social help don't have statement ")
			# Estos son campos calculados a refactorizar
			# family_income_description = fields.Function(_search_family_group, method=True, type='text', string='Income', multi='family_group')
		family_id = fields.Many2one('social.family.group','Search Unic National Folio', required=True, readonly=False)
		family_jjvv = fields.Char(compute='_search_family_group', method=True, size=60, string='JJ.VV')
		family_score = fields.Char(compute='_search_family_group', method=True, size=25, string='Beneficiary Score')
		family_sector = fields.Char(compute='_search_family_group', method=True, type='char', size=64, string='Sector', store=True)
		family_total_income = fields.Integer(compute='_search_family_group', method=True, string='Total Income')
		family_percapita_income = fields.Integer(compute='_search_family_group', method=True, string='Percapita Income')
		family_dwelling = fields.Text(compute='_search_family_group', method=True, string='Beneficiary Dwelling')
		family_income_description = fields.Text(compute='_search_family_group', method=True, string='Income')
		family_num_men = fields.Integer(compute='_search_family_group', method=True, string='Men')
		family_num_women = fields.Integer(compute='_search_family_group', method=True, string='Women')
		family_num_children = fields.Integer(compute='_search_family_group', method=True, string='Children')
		family_total_num = fields.Integer(compute='_search_family_group', method=True, string='Total')
		member_id = fields.Many2one('social.family.group.member', 'Search Beneficiary', required=True, readonly=False,
			domain="[('member_folio','=',family_id)]")
		member_full_name = fields.Char(compute='_search_family_member', method=True, size=32, string='Full Name', store=True)
		member_address = fields.Char(compute='_search_family_member', method=True, size=60, string='Address')
		member_phone = fields.Char(compute='_search_family_member', method=True, type='char', size=25, string='Phone Number')
		member_health = fields.Text(compute='_search_family_member', method=True, type='text', string='Beneficiary Health')
		member_situation_eva = fields.Text(compute='_search_family_member', method=True, type='text',
			string='Situation and Professional Evaluation')
		member_age = fields.Integer(compute='_search_family_member', method=True, string='Age')
		caseworker_name = fields.Many2one('res.users', 'Caseworker Name', required=True, readonly=True, default=lambda self: uid)
		date = fields.Datetime('Social Report Date', required=True, readonly=False)
		ben_family_members = fields.Many2many('social.family.group.member', 'voucher_member_rel', 'voucher_code','member_rut',
			'Family Members', domain="[('member_folio','=',family_id),('id','!=',member_id)]")
		ben_description = fields.Text('Description of the Help', required=False, readonly=False)
		ben_observations = fields.Text('Observations of the Help', required=False, readonly=False)
		state = fields.Selection([
			('1','In Demand - With Act'),
			('2','In Demand - Without Act'),
			('3','Delivered - With Act'),
			('4','Delivered - Without Act')], 'Help State', required=True, readonly=False,  default='1')
		ben_requested_items = fields.One2many('social.help.voucher.item','table_id','Requested Items')


	def state_delivered_without_act(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state':'4'})

	def state_delivered_with_act(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state':'3'})

	def state_in_demand_without_act(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state':'2'})

	def state_in_demand_with_act(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state':'1'})

	# def _date(self, cr, uid, ids, context=None):
	#	'date' : datetime.today()

	def complete_folio_data(self, cr, uid, ids, folio, rut, context=None):
		send = []
		if folio and rut:
			obj_group = self.env['social.family.group'].browse(cr, uid, folio, context=context)
			obj_member = self.env['social.family.group.member'].browse(cr, uid, rut, context=context)

			return {
				'value': {
					'family_jjvv': obj_group.family_jjvv,
					'family_score': obj_group.family_score,
					'family_sector': obj_group.family_sector.name,
					'family_total_income': obj_group.family_total_income,
					'family_percapita_income': obj_group.family_percapita_income,
					'family_dwelling': obj_group.family_dwelling,
					'family_income_description': obj_group.family_income_description,
					'family_num_men': obj_group.family_num_men,
					'family_num_women': obj_group.family_num_women,
					'family_num_children': obj_group.family_num_children,
					'family_total_num': obj_group.family_total_num,
					'member_full_name': obj_member.member_full_name,
					'member_rut': obj_member.member_rut,
					'member_address': obj_member.member_address,
					'member_phone': obj_member.member_phone,
					'member_health': obj_member.member_health,
					'member_situation_eva': obj_member.member_situation_eva,
		            'member_age': obj_member.member_age
				}
			}
		else:
			return {
				'value': {}
			}
#pool.get ?
	def create(self, cr, user, vals, context=None):
		sector = self.env['social.family.group'].browse(cr, user, vals['family_id'], context=context)
		count = self.env['social.help.voucher'].search(cr, user, [('family_sector','=',sector.family_sector.name)],count=True)+1
		self.env['social.sector'].write(cr, user, sector.family_sector.id, {'count': str(count)})

		count = self.env['social.help.voucher'].search(cr, user, [('caseworker_name','=',user)],count=True)+1
		self.env['res.users'].write(cr, user, user, {'count': str(count)})

		res = super(social_help_voucher, self).create(cr, user, vals, context=context)
		return res

	def unlink(self, cr, user, ids, context=None):
		sectorDel = []
		usersDel = []
		for id in ids:
			sectorDel.append(self.env['social.help.voucher'].browse(cr, user, id, context=context).family_id.family_sector)
			usersDel.append(self.env['social.help.voucher'].browse(cr, user, id, context=context).caseworker_name)

		for sector in sectorDel:
			sector_aux = int(sector.count)-1
			if sector_aux < 0:
				self.env['social.sector'].write(cr, user, sector.id, {'count': '0'})
			else:
				self.env['social.sector'].write(cr, user, sector.id, {'count': str(sector_aux)})

		for users in usersDel:
			users_aux = int(users.count)-1
			if users_aux < 0:
				self.env['res.users'].write(cr, user, users.id, {'count': '0'})
			else:
				self.env['res.users'].write(cr, user, users.id, {'count': str(users_aux)})


		res = super(social_help_voucher, self).unlink(cr, user, ids, context=context)
		return res

	def _value(self, cr, uid, ids, context=None):
		#count = self.pool.get('social.help.voucher').search(cr, uid, [('id','>=','0')],count=True)
		ide = self.env['social.help.voucher'].search(cr, uid, [('id','>=','0')])
		if ide:
			count = self.env['social.help.voucher'].browse(cr, uid, ide[len(ide)-1]).voucher_code
			return count + 1
		else:
			return 1


social_help_voucher()
