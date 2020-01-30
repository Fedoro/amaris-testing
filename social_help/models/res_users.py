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

class social_users(models.Model):
	_inherit = 'res.users'

#	def count_helps(self, cr, uid, ids, field_name, arg, context=None):
#		""" Count the helps registry by caseworker
#			@param cr: the current row, from the database cursor,
#			@param uid: the current user’s ID for security checks,
#			@param ids: List of create menu’s IDs
#			@param context: A standard dictionary for contextual values """

#		if not ids:
#			return {}

#		else:
#			cr.execute("SELECT r.id, count(s.voucher_code) from social_voucher as s \
#				inner join res_users as r on (s.caseworker_name = r.id)\
#				where r.id IN %s AND r.id=s.caseworker_name group by r.id;",(tuple(ids),))

#			value = dict(cr.fetchall())

#			for id in ids:
#				if id not in value:
#					value[id]= 0

#			return value


#		'count':fields.function(count_helps, method=True, type='integer', string='Amount of helps', store=True)



# Se modifica los campos actualizando a la version 12
# _columns = {
# }

count = fields.Char('Amount of helps', size=20, default=0, required=True)

social_users()
