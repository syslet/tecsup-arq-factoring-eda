import pytest
from factoring_app.application.desembolso_use_cases import EjecutarDesembolsoUseCase
from factoring_app.domain.entities import Disbursement

class FakeSunatService:
    def validar_empresa(self, ruc):
        return {"estado": "VALID"}

class FakeBankService:
    def transferir_monto(self, account, amount):
        return {"estado": "TRANSFERENCIA_EXITOSA"}

class FakeNotificationService:
    def enviar_notificacion(self, destinatario, mensaje):
        return {"status": "OK"}

class FakeRepo:
    def guardar_desembolso(self, desembolso):
        desembolso.id = 5
        return desembolso

def test_ejecutar_desembolso_exitoso():
    use_case = EjecutarDesembolsoUseCase(
        disbursement_repo=FakeRepo(),
        banco_service=FakeBankService(),
        notificacion_service=FakeNotificationService()
    )
    desembolso = Disbursement(
        sheet_id=12,
        annotation_code="ANOT001",
        amount=8000,
        currency="PEN",
        bank_name="Banco de Crédito",
        bank_account_number="1234567890",
        cci="00212345678901234567"
    )
    result = use_case.ejecutar(desembolso)
    assert result.id == 5
    assert result.amount == 8000
