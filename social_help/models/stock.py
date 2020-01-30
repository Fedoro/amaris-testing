# -*- coding: utf-8 -*-
####################################################################
#	APPLICATION FORM FOR STOCK ON SOCIAL HELP MANAGEMENT, CHILE.
#		Created and Designed by:
#			David Acevedo (dacevedo@stratanet.cl)
#			Diego Cantos (dcantos@stratanet.cl)
#	 	www.stratanet.cl
####################################################################


from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import time, datetime, addons

class social_help_stock_out_forms(models.Model):
	_name = 'social.help.stock.out.forms'
	_description = 'Stock Registration for Items Output'

	def _voucher(self, cr, uid, ids, field_name, arg, context=None):
		if not ids:
			return {}
		else:
			res = {}

			for id in ids:
				res[id] = {
					'items': [],
					'withdrawn_by': False
				}

			cr.execute("SELECT o.id, i.item_id, vi.amount, v.member_full_name from social_help_voucher as v \
					inner join social_help_stock_out_forms as o on (v.id = o.voucher_code) \
					inner join social_help_voucher_item as vi on (vi.table_id = v.id) \
					inner join social_help_stock_items as i on (vi.item_id = i.id) \
					where o.id IN %s order by o.id;",(tuple(ids),))

			for id, item_id, amount, member in cr.fetchall():
				res[id]['withdrawn_by'] = member
				res[id]['items'].append([0,False,{'item_id':int(item_id),'amount':amount}])

			return res


		company_id = fields.Many2one('res.company', 'Warehouse', required=True, readonly=False, default=lambda self: self.env.user.company_id)
		voucher_code = fields.Many2one('social.help.voucher', 'Social Report Code', size=32, required=True, readonly=False)
		warehouse_number = fields.Integer('Warehouse Number', size=10, required=True, readonly=False)
		date = fields.Datetime('Output Date', required=True, readonly=False)
		withdrawn_by = fields.Char(compute='_voucher', method=True, size=100, string='Withdrawn By', store=True)
		type_action = fields.Selection([('delivery_act','Delivery Act')],'Action Type', required=True, readonly=False, default='delivery_act')
		items = fields.One2many(compute='_voucher', obj='social.help.stock.out.registration', string='Items')


	def create(self, cr, user, vals, context=None):
		if len(str(vals['warehouse_number'])) > 10:
			raise ValidationError(_('Error!'),_("The Warehouse Number is to long, (10 numbers max)!"))
		obj = []
		voucher = vals['voucher_code']
		ides = self.env['social.help.voucher.item'].search(cr, user, [('table_id','=',voucher)], context=context)
		for num in ides:
			obj.append(self.env['social.help.voucher.item'].browse(cr, user, num, context=context))

		if obj:
			for item in obj:
				if item.item_id.item_id and item.amount and item.item_id.total_amount:
					amount = int(item.amount)
					virtual_amount = int(item.item_id.virtual_amount)
					total_amount = int(item.item_id.total_amount)
					item_id = int(item.item_id.item_id)

					total = virtual_amount
					total = total_amount
					total -= amount

					if total >= 0:
						self.env['social.help.stock.items'].write(cr, user, item_id, {'virtual_amount': total})
						self.env['social.help.stock.items'].write(cr, user, item_id, {'total_amount': total})
					else:
						raise ValidationError(_('Error!'),_("You do not have the number of items required!"))
				else:
					raise ValidationError(_('Error!'),\
						_("You have some problem with the items, please contact your system administrator!"))


			status = self.env['social.help.voucher'].browse(cr, user, voucher, context=context).state

			if status == '1':
				self.env['social.help.voucher'].write(cr, user, voucher, {'state': '3'})
			elif status == '2':
				self.env['social.help.voucher'].write(cr, user, voucher, {'state': '4'})

			res = super(social_help_stock_out_forms, self).create(cr,user,vals,context=None)
			return res
		else:
			res = super(social_help_stock_out_forms, self).create(cr,user,vals,context=None)
			return res


	def complete(self, cr, uid, ids, code, context=None):
		send = []
		if code:
			withdrawn = self.env['social.help.voucher'].browse(cr, uid, code, context=context).member_full_name
			ides = self.env['social.help.voucher'].search(cr, uid, [('table_id','=',code)], context=context)
			for num in ides:
				obj = self.env['social.help.voucher'].browse(cr, uid, num, context=context)
				send.append([0,False,{'item_id':int(obj.item_id.item_id),'amount':obj.amount}])

			return {
				'value': {
					'withdrawn_by': withdrawn,
					'items': send
				}
			}
		else:
			return {
					'value': {}
			}

	# def _date(self, cr, uid, ids, context=None):
	#	today = time.strftime("%Y-%m-%d %H:%M:%S")
	#	return today

social_help_stock_out_forms()
