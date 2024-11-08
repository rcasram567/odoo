from odoo import models, fields

class Presupuesto(models.Model):
    _name="presupuesto"
    name=fields.Char(string='Nombre',required=True)
    description = fields.Text(string="Description")
    price = fields.Float(string='Precio', digits=(10,2))
    status = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('done', 'Hecho')
    ], string='Estado', default='draft')
    is_active = fields.Boolean(string='Activo', default=False)
    start_date = fields.Date(string='Fecha de Inicio')
    persona_ventas = fields.Many2one(comodel_name="res.partner")