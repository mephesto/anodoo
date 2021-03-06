from odoo import models, fields, api
from odoo.exceptions import ValidationError


    
    
class CustomerType(models.Model):
    _name = "anodoo.customer.type"
    _description = '客户性质'
    
    name = fields.Char('名称', required=True)
    
    sequence = fields.Integer('序号', default=1)
    
    key = fields.Selection([('company', '公司客户'), ('person', '个人客户'), ('family', '家庭客户'), ('government', '政府客户'), ('organization', '组织客户')], 
                            string='类型', default='company', help='客户类型定义，可扩展')
    
    is_active = fields.Boolean('是否启动', default=True)
    
    description = fields.Text('描述', translate=False)
    
class CustomerSize(models.Model):
    _name = "anodoo.customer.size"
    _description = '客户规模'
    
    name = fields.Char('名称', required=True)
    
    sequence = fields.Integer('序号', default=1)
    
    key = fields.Selection([('KA', '大客户'), ('SMB', '中小客户')], 
                            string='类型', default='KA', help='客户规模定义，可扩展')
    
    is_active = fields.Boolean('是否启动', default=True)
    
    description = fields.Text('描述', translate=False)
    

    
class CustomerLabelCategory(models.Model):
    _name = "anodoo.customer.label.category"
    _description = '客户标签分类'
    _parent_store = True
    
    name = fields.Char(string='分类名称', required=True)
    
    parent_id = fields.Many2one('anodoo.customer.label.category', string='父分类', index=True, ondelete='cascade')
    child_ids = fields.One2many('anodoo.customer.label.category', 'parent_id', string='子分类')

    parent_path = fields.Char(index=True)
    
    description = fields.Text('描述', translate=False)
    
    #display_name = fields.Char(string='Display Name') 
    
    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You can not create recursive tags.'))

    def name_get(self):
        """ Return the categories' display name, including their direct
            parent by default.

            If ``context['partner_category_display']`` is ``'short'``, the short
            version of the category name (without the direct parent) is used.
            The default is the long version.
        """
        if self._context.get('partner_category_display') == 'short':
            return super(CustomerLabelCategory, self).name_get()

        res = []
        for category in self:
            names = []
            current = category
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((category.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        partner_category_ids = self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(partner_category_ids).with_user(name_get_uid))


    
class CustomerLabel(models.Model):
    _name = "anodoo.customer.label"
    _description = "客户标签"
    
    name = fields.Char(string='标签名称', required=True)
    
    category_id = fields.Many2one('anodoo.customer.label.category', string='标签分类')
    
    color = fields.Integer(string='颜色')
    
    description = fields.Text('描述', translate=False)
    
class CustomerSegment(models.Model):
    _name = "anodoo.customer.segment"
    _description = '客户细分，客户群，客户分群'
    
    name = fields.Char(string='客户细分名称', required=True)
    
    label_ids = fields.Many2many('anodoo.customer.label', string='客户标签', help='客户细分对应的客户标签，根据标签批判客户')
    
    sequence = fields.Integer('序号', default=10, help="客户细分的序号")
    
    description = fields.Text('描述', translate=False)
    
    dynamic_customer_ids = fields.Many2many('res.partner', 'anodoo_customer_segment_dynamic', 'segment_id', 'customer_id', string='动态客户列表', help='客户细分下的动态客户列表，根据标签动态计算并刷新',
                                    compute='_compute_dynamic_customer_ids')
    
    static_customer_ids = fields.Many2many('res.partner', 'anodoo_customer_segment_static', 'segment_id', 'customer_id', string='静态客户列表', help='客户细分下的静态客户列表',
                                    domain="[('partner_type', '=', 'customer')]")
    
    segment_snapshot_ids = fields.One2many('anodoo.customer.segment.snapshot', 'segment_id', string='客户快照')
    
    def _compute_dynamic_customer_ids(self):
        for record in self:
            record.dynamic_customer_ids
    
    
class CustomerSegmentSnapshot(models.Model):
    _name = "anodoo.customer.segment.snapshot"
    _description = '客户快照，是客户细分的静态客户列表，它是某一个时刻对该客户细分下客户列表的一个快照。'
    
    segment_id = fields.Many2one('anodoo.customer.segment', string='客户细分')
    
    customer_count = fields.Integer('客户数量', compute='_compute_customer_count')
    
    customer_ids = fields.Many2many('res.partner', string='客户', help='客户细分下的静态客户列表',
                                    domain="[('partner_type', '=', 'customer')]")
    
    create_uid = fields.Many2one(string='快照人')
    create_date = fields.Datetime(string='快照日期')
    
    description = fields.Text('描述', translate=False)
    
    def _compute_customer_count(self):
        for record in self:
            record.customer_count = 9283