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

#	'count':fields.function(count_helps, method=True, type='integer', string='Amount of helps', store=True)
	count = fields.Char('Amount of helps', default='0', required=True)
social_users()
