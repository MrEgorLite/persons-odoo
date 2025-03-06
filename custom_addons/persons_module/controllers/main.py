from odoo import http
from odoo.http import request

class PersonWebsiteController(http.Controller):

    @http.route("/persons/", auth="public", website=True)
    def persons_page(self, **kwargs):
        persons = request.env["person.model"].sudo().search([], order="id desc", limit=5)
        return request.render("persons_module.persons_template", {"persons": persons})

    @http.route("/persons/all/", auth="public", website=True)
    def persons_all_page(self, **kwargs):
        persons = request.env["person.model"].sudo().search([], order="id desc")
        return request.render("persons_module.persons_all_template", {"persons": persons})

    @http.route("/persons/add/", auth="public", website=True)
    def person_add_form(self, **kwargs):
        companies = request.env["res.company"].sudo().search([])
        return request.render("persons_module.person_add_template", {"companies": companies})

    @http.route("/persons/submit/", type="http", auth="public", website=True, csrf=True)
    def person_submit(self, **post):
        if post:
            request.env["person.model"].sudo().create({
                "first_name": post.get("first_name"),
                "last_name": post.get("last_name"),
                "birthday": post.get("birthday") or False,
                "sex": post.get("sex"),
                "company_id": int(post.get("company_id")) if post.get("company_id") else False,
            })
        return request.redirect("/persons/")
