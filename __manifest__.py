{
    'name': "movies",

    'summary': "Mòdul de gestió de pel·lícules - Ampliació Part 3",

    'description': """
        Mòdul personalitzat per a la gestió de pel·lícules, 
        incloent taxes de canvi de moneda i informes PDF.
    """,

    'author': "SantiS2002",
    'website': "https://github.com/santiS2002/odooMoviesPractica2",

    'category': 'Uncategorized',
    'version': '0.1',

    # 'base' és necessari per al model res.country 
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/movies_menus.xml',
        'views/movies_movie_views.xml',
        'views/movies_view_views.xml',
      
        'reports/movie3_report.xml',
        'reports/movie3_report_template.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}