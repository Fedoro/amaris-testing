
{
	'name': 'Social Help Management',
	'version': '0.1',
	'author': 'Fedoro, Cantos, Stratanet',
	'category': 'others',
	'website': 'http://www.stratanet.cl',
	'depends': ['base','l10n_cl_toponym'],
	'data': [
#		'security/social_help_security.xml',
#		'security/ir.model.access.csv',
		'views/stock_view.xml',
		'views/social_assistance_view.xml',
#		'views/social_board.xml',
		'report/social_help_reports.xml',
		'data/data.xml'
	],
	'installable': True,
	'active': False
	#       'certificate': 'certificate',
}
