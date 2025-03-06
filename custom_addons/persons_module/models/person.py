from datetime import datetime
from odoo import models, fields, api

class Person(models.Model):
    _name = "person.model"
    _description = "Person Model"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    birthday = fields.Date(string="Birthday")
    sex = fields.Selection([
        ("male", "Male"),
        ("female", "Female"),
        ("non-binary", "Non-Binary"),
    ], string="Sex")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
        required=True
    )

    full_name = fields.Char(string="Full Name", compute="_compute_full_name", store=True)
    age = fields.Integer(string="Age", compute="_compute_age", store=True)

    @api.depends("first_name", "last_name")
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.first_name} {record.last_name}"

    @api.depends("birthday")
    def _compute_age(self):
        for record in self:
            if record.birthday:
                birth_year = record.birthday.year
                current_year = datetime.now().year
                record.age = current_year - birth_year
            else:
                record.age = 0
