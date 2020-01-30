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

class sector(models.Model):
	_name = 'sector'
	_descripcion = 'Sectors of the Place'

	name = fields.Char('Sector Name', required=True)
	code = fields.Char('Sector Code', required=True)
	sector_type = fields.Char('Sector Type', required=True)
	count = fields.Char('Amount of helps', default='0', required=True)

	@api.model
	def name_search(self, name='', args=None, operator='ilike', limit=80):
		args = args or []
		ids = self.search([('code', operator, name)] + args, limit=limit)

		if not ids:
			ids = self.search([('name', operator, name)] + args, limit=limit)
		return self.name_get()
sector()
