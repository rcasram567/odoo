from sys import api_version

from odoo import models, fields, api

import logging

from odoo.tools.populate import compute

_logger = logging.getLogger('RaulCasado')


class Presupuesto(models.Model):
    _name="inventario.presupuesto"
    _inherit="image.mixin"
    name=fields.Char(string='Nombre',required=True)
    description = fields.Text(string="Description")
    price = fields.Float(string='Precio', digits=(10,2), compute="_calculate_total_price", store="True")
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

    genero_ids = fields.Many2many(comodel_name="inventario.clasificacion",
                                  relation='registros_productos',
                                  column1='presupuesto_id',
                                  column2='clasificacion_id')

    detalles_venta = fields.Char(string='Detalles venta', required=True)
    Subir_archivo = fields.Binary(string="Archivo")
    nombre_archivo = fields.Char(string="Nombre del archivo")
    link = fields.Char(string="Url")
    categoria_ventas = fields.Many2one(
        comodel_name="res.partner.category",
        string="Categoria contacto",
        default=lambda self: self.env["res.partner.category"].search([('name', '=', 'ventas')], limit=1)
    )
    unidades_producto = fields.Integer(string="Unidades del producto")
    precio_unitario = fields.Float(string='Precio unitario', digits=(10, 2))

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

    all_specific_products = fields.Char(string="Producto Específico", compute="get_array_products")

    all_specific_products_selection = fields.Selection(string="Producto Específico",
                                                       selection="give_selection_products")

    @api.depends()
    def get_array_products(self):
        productos = self.env["inventario.clasificacion"].search([])
        conjunto = set()
        for registro in productos:
            conjunto.add(registro.producto_especifico)
        lista_string=str(list(conjunto))
        for registro in self:
            registro.all_specific_products=lista_string

    def give_selection_products(self):
        productos=self.env["inventario.clasificacion"].search([]) #Busca todos los registros de la tabla. Select * ES UN RECORDSET
        conjunto=set()
        _logger.info(str(productos))
        for registro in productos:
            conjunto.add(registro.producto_especifico) #Añado en un conjunto todos los productos especificos
            _logger.info(" este es mi producto "+str(registro.producto_especifico))
        lista=list(conjunto) #"['Ryzen7']"

        ###########################
        array_duplas=[]
        for elem in lista:
            array_duplas.append((elem,elem)) #[(False,False),(Ryzen7.Ryzen7)]
        return array_duplas

    #def give_selection_products(self):
    #    productos = self.env["inventario.clasificacion"].search([])
    #    conjunto = set()
    #    for registro in productos:
    #        conjunto.add(registro.producto_especifico)
    #    lista=list(conjunto)
    #    array_duplas=[]
    #    for elem in lista:
    #        array_duplas.append((elem,elem))
    #    return array_duplas

    price_with_tax = fields.Float(string="Precio con IVA (21%)", compute="_compute_price_with_tax", digits=(10,2))

    @api.depends("price")
    def _compute_price_with_tax(self):
        for record in self:
            record.price_with_tax = record.price*1.21


#Apartado c

    @api.depends("unidades_producto","precio_unitario")
    def _calculate_total_price(self):
        for record in self:
            if not record.unidades_producto or not record.precio_unitario:
                record.price = 0.0
            else:
                record.price= record.unidades_producto * record.precio_unitario