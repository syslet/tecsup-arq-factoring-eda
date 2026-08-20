from factoring_app.domain.entities import InvoiceSheet, Sale, Invoice
from factoring_app.infrastructure.db_config import SessionLocal
from pricing_rabbitmq_adapter.pricing_rabbitmq_service import get_latest_pricing


class RegistrarPlanillaUseCase:
    def __init__(self, sheet_repo, invoice_repo, validacion_service):
        self.sheet_repo = sheet_repo
        self.invoice_repo = invoice_repo
        self.validacion_service = validacion_service

    def ejecutar(self, planilla: InvoiceSheet, invoices: list = None):
        db = SessionLocal()
        try:
            # 1. Recuperar último pricing desde RabbitMQ
            pricing_event = get_latest_pricing()
            if "error" in pricing_event:
                raise ValueError("No se pudo obtener el pricing desde RabbitMQ")

            advance_rate = pricing_event.get("advance_rate")
            monthly_rate = pricing_event.get("monthly_rate")

            # 2. Calcular campos derivados
            total_amount = planilla.total_amount
            planilla.advance_rate = advance_rate
            planilla.monthly_rate = monthly_rate
            planilla.advance_amount = total_amount - (total_amount * advance_rate)
            planilla.interest_fee = planilla.advance_amount * monthly_rate
            planilla.commission = total_amount * advance_rate
            planilla.net_disbursement = total_amount - planilla.interest_fee - planilla.commission

            # 3. Validar facturas con SUNAT
            if invoices:
                for factura in invoices:
                    if not self.validacion_service.validar_factura(factura):
                        raise ValueError(f"Factura inválida: {factura.invoice_number}")
                    self.invoice_repo.guardar_factura(factura)

            # 4. Guardar planilla
            self.sheet_repo.guardar_planilla(planilla)

            # 5. Guardar registro en tabla sales
            venta = Sale(
                total_amount=total_amount,
                advance_amount=planilla.advance_amount,
                advance_rate=advance_rate,
                pricing_rate=monthly_rate,
                pricing_timestamp=pricing_event.get("timestamp"),
                monto_final=planilla.net_disbursement
            )
            db.add(venta)
            db.commit()
            db.refresh(venta)

            return {
                "status": "Planilla y venta registradas",
                "planilla_id": planilla.id,
                "sale_id": venta.id,
                "advance_rate": advance_rate,
                "monthly_rate": monthly_rate,
                "advance_amount": planilla.advance_amount,
                "interest_fee": planilla.interest_fee,
                "commission": planilla.commission,
                "net_disbursement": planilla.net_disbursement
            }

        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
