#-*- coding: utf-8 -*-

import datetime
from string import upper
from report import report_sxw
from report.report_sxw import rml_parse

class Parser(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		super(Parser, self).__init__(cr, uid, name, context)
		
		#Obtenemos id del formulario a imprimir
		#self.formulario = uid
		
		self.localcontext.update({
			'schooling': self.schooling,
#			'kinship': self.kinship,
			'dates': self.dates,
			'uppercase': self.uppercase,
			'none': self.none,
#			'gender': self.gender,
			'marital': self.marital,
#			'mark': self.mark,
		})
	
	def none(self):
		return 'Ninguno/a'
		
	def kinship(self, value):
		if 'spouse' in value:
			return 'Conyuge'
		elif 'son' in value:
			return 'Hijo'
		elif 'daugther' in value:
			return 'Hija'
		elif 'cohabitant' in value:
			return 'Conviviente'
		elif 'father' in value:
			return 'Padre'
		elif 'mother' in value:
			return 'Madre'
		elif 'grandfather' in value:
			return 'Abuelo'
		elif 'grandmother' in value:
			return 'Abuela'
		elif 'grandchildren' in value:
			return 'Nieto'
		elif 'others' in value:
			return 'Otro'
		
	
	def schooling(self, level):
		o = unicode('\xc3\xb3','utf8')
		a = unicode('\xc3\xa1','utf8')
		e = unicode('\xc3\xa9','utf8')

		if 'primary_com' in level:
#			return 'Educaci'+o+'n B'+a+'sica Completa'
			return 'Educacion Basica Completa'
		elif 'primary_unc' in level:
#			return 'Educaci'+o+'n B'+a+'sica Incompleta'
			return 'Educacion Basica Incompleta'
		elif 'secondary_com' in level:
#			return 'Educaci'+o+'n Media Completa'
			return 'Educacion Media Completa'
		elif 'secondary_unc' in level:
#			return 'Educaci'+o+'n Media Incompleta'
			return 'Educacion Media Incompleta'
		elif 'college_com' in level:
#			return 'Educaci'+o+'n Superior Completa'
			return 'Educacion Superior Completa'
		elif 'college_unc' in level:
#			return 'Educaci'+o+'n Superior Incompleta'
			return 'Educacion Superior Incompleta'
		elif 'technical_com' in level:
#			return 'Estudios T'+e+'cnicos Completos'
			return 'Estudios Tecnicos Completos'
		elif 'technical_unc' in level:
#			return 'Estudios T'+e+'cnicos Incompletos'
			return 'Estudios Tecnicos Incompletos'
		elif 'none' in level:
			return 'Sin Estudios'

	def marital(self, status):
		if 'married' == status:
			return 'Casado (a)'
		elif 'single' == status:
			return 'Soltero (a)'
		elif 'divorced' == status:
			return 'Divorciado (a)'
		elif 'widow' == status:
			return 'Viudo (a)'
		elif 'cohabitant' == status:
			return 'Conviviente'

	def mark(self, label, record):
		if int(record) == int(label):
			return 'X'

	def uppercase(self, record):
		return upper(record)

	def dates(self, option, date):
		if date:
			if int(option) == 0:
				return date
			elif int(option) == 1:
				today = datetime.date.today().strftime("%d/%m/%Y")
				return today

	def gender(self, gender):
		if gender == 'masculino':
			return 'M'
		else:
			return 'F'

