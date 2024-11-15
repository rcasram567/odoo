from odoo import models, fields, exceptions
from odoo.odoo import api
##from odoo.exceptions import ValidationError


class Presupuesto(models.Model):
    _name="presupuesto"
    _inherit="image.mixin"
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
    puntuacion_vendedor_introducir = fields.Integer(string="Puntuacion_vendedor")
    puntuacion_vendedor = fields.Integer(string="Puntuacion", related="puntuacion_vendedor_introducir")
    persona_ventas = fields.Many2one(comodel_name="res.partner")
    genero_ids = fields.Many2many(comodel_name="clasificacion")
    detalles_venta = fields.Char(string='Detalles venta', required=True)
    Subir_archivo = fields.Binary(string="Archivo")
    nombre_archivo = fields.Char(string="Nombre del archivo")
    link = fields.Char(string="Url")
    categoria_ventas = fields.Many2one(
        comodel_name="res.partner.category",
        string="Categoria contacto",
        default=lambda self: self.env["res.partner.category"].search([('name', '=', 'ventas')], limit=1)
    )

    #@api.constrains('status')
    #def _check_status(self):
    #    for record in self:
    #        if (record.status=='draft'):
    #            self.confirmar_presupuesto()
    #        elif (record.satus=='confirmed'):
    #            record.status.selection(['done'])
    #        else:
    #            record.status.selection([''])

    def confirmar_presupuesto(self):
         if(self.status == "draft"):
            self.status = "confirmed"

    def terminar_presupuesto(self):
        if(self.status == "confirmed"):
            self.status = "done"