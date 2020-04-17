from django import forms
from ra.admin.admin import ra_admin_site, RaAdmin, RaMovementAdmin, RaMovementInlineAdmin
from .models import Client, Product, SimpleSales, Invoice, InvoiceLine


class ClientAdmin(RaAdmin):
    fields = ('slug', 'title', 'notes', 'address', 'email', 'telephone')

    view_template = 'admin/client_view.html'


class ProductAdmin(RaAdmin):
    pass


class SalesOrderAdmin(RaMovementAdmin):
    fields = ['slug', 'doc_date', 'client', ('product', 'price', 'quantity', 'value')]

    add_form_template = change_form_template = 'salesorder_changeform.html'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'value':
            formfield.widget = forms.TextInput(attrs={'readonly': 'readonly'})
        return formfield


class InvoiceLineAdmin(RaMovementInlineAdmin):
    fields = ['product', 'quantity', 'price', 'discount', 'value']
    model = InvoiceLine


class InvoiceAdmin(RaMovementAdmin):
    fields = [('slug', 'doc_date'), 'client']
    inlines = [InvoiceLineAdmin]
    copy_to_formset = ['client']


ra_admin_site.register(Client, ClientAdmin)
ra_admin_site.register(Product, ProductAdmin)
ra_admin_site.register(SimpleSales, SalesOrderAdmin)
ra_admin_site.register(Invoice, InvoiceAdmin)
