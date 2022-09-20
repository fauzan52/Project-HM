from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class algoritma_pembelian(models.Model):
    _name = 'algoritma.pembelian'

    # def function_to_approved(self):
    #     if self.status == 'draft':
    #         if self.name == 'New':
    #             seq = self.env['ir.sequence'].next_by_code('algoritma_pembelian') or 'New'
    #             self.name = seq
    #         self.status = 'to_approved'

    @api.model
    def create(self, values):
        res = super(algoritma_pembelian, self).create(values)
        for rec in res:
            tanggal_pembelian = rec.tanggal
            tanggal_sekarang = date.today()
            if tanggal_pembelian < tanggal_sekarang:
                raise ValidationError(('Tanggal yang ada masukkan tidak boleh kurang dari tanggal hari ini'))
        return res

    def write(self, values):
        res = super(algoritma_pembelian, self).write(values)
        if 'tanggal' in values:
            tanggal_pembelian = self.tanggal
            tanggal_sekarang = date.today()
            if tanggal_pembelian < tanggal_sekarang:
                raise ValidationError(('Tanggal yang ada masukkan tidak boleh kurang dari tanggal hari ini'))
        return res

    def function_approved(self):
        if self.status == 'to_approved':
            self.status = 'approved'

    def function_done(self):
        if self.status == 'approved':
            self.status = 'done'

    name = fields.Char(string="Name", default="New")
    tanggal = fields.Date(string="Date")
    status = fields.Selection(
        [('draft', 'Draft'), ('to_approved', 'To Approved'), ('approved', 'Approved'), ('done', 'Done')],
        default='draft')
    algoritma_pembelian_ids = fields.One2many('algoritma.pembelian.line', 'algoritma_pembelian_id',
                                              string="Algoritma Pembelian Ids")
    brand_ids = fields.Many2many('algoritma.brand', 'algoritma_pembelian_brand_rel', 'algoritma_pembelian_id',
                                 'brand_id', string="Brand")


class algoritma_pembelian_line(models.Model):
    _name = 'algoritma.pembelian.line'

    @api.onchange('product_id')
    def func_onchange_product_id(self):
        if not self.product_id:
            return {}
        else:
            self.description = self.product_id.name
        return {}

    def function_amount_total(self):
        for line in self:
            line.sub_total = line.quantity * line.price

    #
    # def function_domain_product_id(self):
    #     product_obj = self.env['product.product'].search([('type', '=', 'product')])
    #     domain = [('id', 'in', product_obj.ids)]
    #     return domain

    algoritma_pembelian_id = fields.Many2one('algoritma.pembelian', string="Pembelian")
    product_id = fields.Many2one('product.product', string="Product ID")
    description = fields.Char(string="Description")
    quantity = fields.Float(string="Quauntity", default=0.0)
    price = fields.Float(strinng="Price", default=0.0)
    sub_total = fields.Float(string="Total", compute=function_amount_total)
    uom_id = fields.Many2one('uom.uom', string="Type")


class algoritma_brand(models.Model):
    _name = 'algoritma.brand'

    name = fields.Char(string="Nama")


class algoritma_pembelian_report_wizard(models.TransientModel):
    _name = 'algoritma.pembelian.report.wizard'

    name = fields.Char(string="Name")
    periode_awal = fields.Date(string="Periode Awal")
    periode_akhir = fields.Date(string="Periode Akhir")


class product_template(models.Model):
    _inherit = 'product.template'

    status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('done', 'Done')], string="Status",
                              default="draft")
