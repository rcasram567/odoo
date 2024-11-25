from odoo import models, fields

class Generos(models.Model):
    _name="inventario.clasificacion"
    name = fields.Char(string='Nombre', required=True)
    producto_especifico = fields.Char(string="Nombre del producto", required=True)
    cantidad = fields.Float(string="Cantidad del producto", required=True)
    precio_unitario = fields.Float(string="Precio por unidad", required=True)
