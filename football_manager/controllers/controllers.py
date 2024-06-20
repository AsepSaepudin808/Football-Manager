# -*- coding: utf-8 -*-
# from odoo import http


# class FootballManager(http.Controller):
#     @http.route('/football_manager/football_manager', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/football_manager/football_manager/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('football_manager.listing', {
#             'root': '/football_manager/football_manager',
#             'objects': http.request.env['football_manager.football_manager'].search([]),
#         })

#     @http.route('/football_manager/football_manager/objects/<model("football_manager.football_manager"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('football_manager.object', {
#             'object': obj
#         })
