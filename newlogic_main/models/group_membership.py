# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
#from odoo.addons.website.models import ir_http

from odoo.exceptions import AccessError, UserError, ValidationError, Warning
#from odoo.tools.misc import formatLang, get_lang
#from odoo.osv import expression
#from odoo.tools import float_is_zero, float_compare

class GroupMembership(models.Model):
    _name = 'nl.group.membership'
    _description = 'Group Membership'
    _order = 'id desc'

    group = fields.Many2one('res.partner','Group')
    individual = fields.Many2one('res.partner','Individual')
    kind = fields.Char('Head of Household')
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')

    def name_get(self):
        res = super(GroupMembership, self).name_get()
        for rec in self:
            name = 'NONE'
            if rec.group:
                name = rec.group.name
            res.append((rec.id, name))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            args = [('group', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
