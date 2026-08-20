import pytest
from factoring_app.application.venta_use_cases import RegistrarPlanillaUseCase
from factoring_app.domain.entities import InvoiceSheet, Invoice

class FakeRepo:
    def guardar_planilla(self, sheet):
        sheet.id = 12
        return sheet
    def guardar_facturas(self, facturas):
        for i, f in enumerate(facturas, start=101):
            f.id = i
        return facturas

def test_registro_planilla_con_facturas():
    use_case = RegistrarPlanillaUseCase(FakeRepo())
    sheet = InvoiceSheet(company_id=1, sheet_code="PLAN001", currency="PEN", total_amount=10000, advance_amount=8000)
    invoices = [Invoice(invoice_number="F001-0001", amount=5000, currency="PEN")]
    result = use_case.ejecutar(sheet, invoices)
    assert result["sheet"].id == 12
    assert len(result["invoices"]) == 1
    assert result["invoices"][0].id == 101
