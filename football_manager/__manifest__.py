{
    'name': 'Football League',
    'version': '1.0',
    'summary': 'Manage football league with club data, match scores, and standings',
    'category': 'Sports',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/football_league_views.xml',
        'views/football_league_menu.xml',
    ],
    'installable': True,
    'application': True,
}