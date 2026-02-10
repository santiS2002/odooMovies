# from odoo import http


# class Movies(http.Controller):
#     @http.route('/movies/movies', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/movies/movies/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('movies.listing', {
#             'root': '/movies/movies',
#             'objects': http.request.env['movies.movies'].search([]),
#         })

#     @http.route('/movies/movies/objects/<model("movies.movies"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('movies.object', {
#             'object': obj
#         })

