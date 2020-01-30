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

{
	'name': 'Family Management',
	'version': '1.0',
	'author': '[DBit EIRL]',
	'website': '',
	'category': 'Others',
	'depends': [
		'base',
		'sectors',
		'stock',
		'sale'
	],
	'data': [
		'security/family_security.xml',
		'security/ir.model.access.csv',
		'views/menu_views.xml',
		'views/family_view.xml',
#		'views/social_help.xml'
#		'data/FPS_grupos_freire.csv',
#		'data/FPS_miembros_freire.csv'
	],
	'contributors': [
		'David Acevedo Toledo <soporte.acevedo@gmail.com>'
	]
}
