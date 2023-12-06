# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class ProductPricelistReport(models.AbstractModel):
    _inherit = 'report.product.report_pricelist'

    def _get_product_data(self, is_product_tmpl, product, pricelist, quantities):
        data = {
            'id': product.id,
            'name': '[%s] %s'%(product.default_code,is_product_tmpl and product.name or product.display_name),
            'price': dict.fromkeys(quantities, 0.0),
            'uom': product.uom_id.name,
        }
        for qty in quantities:
            data['price'][qty] = pricelist.get_product_price(product, qty, False)

        if is_product_tmpl and product.product_variant_count > 1:
            data['variants'] = [
                self._get_product_data(False, variant, pricelist, quantities)
                for variant in product.product_variant_ids
            ]

        return data
