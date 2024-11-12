from odoo import models, fields

class Generos(models.Model):
    _name="clasificacion"
    name = fields.Char(string='Nombre', required=True)
