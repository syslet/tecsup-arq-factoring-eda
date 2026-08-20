import pytest
from factoring_app.application.registro_use_cases import RegistrarEmpresaUseCase
from factoring_app.domain.entities import Company

class FakeSunatService:
    def validar_empresa(self, ruc):
        return {"estado": "VALID"}

class FakeRepo:
    def guardar_empresa(self, empresa):
        empresa.id = 1
        return empresa

def test_registro_empresa_valida():
    use_case = RegistrarEmpresaUseCase(FakeRepo(), FakeSunatService())
    empresa = Company(ruc="20123456789", razon_social="Empresa SAC")
    result = use_case.ejecutar(empresa)
    assert result.id == 1
    assert result.razon_social == "Empresa SAC"
