# factoring/domain/entities.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from sqlalchemy import Date

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    phone = Column(String(30))
    role = Column(String(50), default="GIRADOR")
    verification_status = Column(String(50), default="PENDING_VERIFICATION")
    is_active = Column(Boolean, default=True)
    failed_login_attempts = Column(Integer, default=0)
    is_locked = Column(Boolean, default=False)
    locked_until = Column(DateTime)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="legal_representative")

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    ruc = Column(String(11), unique=True, nullable=False)
    business_name = Column(String(255), nullable=False)
    legal_representative_user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    bank_name = Column(String(100), nullable=False)
    bank_account_number = Column(String(50), nullable=False)
    cci = Column(String(20), nullable=False)
    currency = Column(String(10), default="PEN")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    legal_representative = relationship("User", back_populates="company")
    documents = relationship("CompanyDocument", back_populates="company")
    sheets = relationship("InvoiceSheet", back_populates="company")

class CompanyDocument(Base):
    __tablename__ = "company_documents"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    document_type = Column(String(50), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="documents")

class InvoiceSheet(Base):
    __tablename__ = "invoice_sheets"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    sheet_code = Column(String(50), unique=True, nullable=False)
    currency = Column(String(10), default="PEN")
    total_amount = Column(Float, nullable=False)
    advance_amount = Column(Float, nullable=False)
    interest_fee = Column(Float, nullable=False)
    commission = Column(Float, nullable=False)
    net_disbursement = Column(Float, nullable=False)
    advance_rate = Column(Float, default=0.85)
    monthly_rate = Column(Float, default=0.02)
    status = Column(String(50), default="QUOTED")
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="sheets")
    invoices = relationship("Invoice", back_populates="sheet")
    disbursement = relationship("Disbursement", back_populates="sheet", uselist=False)

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    sheet_id = Column(Integer, ForeignKey("invoice_sheets.id"), nullable=False)
    invoice_number = Column(String(50), nullable=False)
    drawer_ruc = Column(String(11), nullable=False)
    debtor_ruc = Column(String(11), nullable=False)
    debtor_name = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    days_to_maturity = Column(Integer, nullable=False)
    sunat_status = Column(String(20), default="VALID")
    is_approved = Column(Boolean, default=True)
    rejection_reason = Column(Text)

    sheet = relationship("InvoiceSheet", back_populates="invoices")

class Disbursement(Base):
    __tablename__ = "disbursements"
    id = Column(Integer, primary_key=True)
    sheet_id = Column(Integer, ForeignKey("invoice_sheets.id"), unique=True, nullable=False)
    annotation_code = Column(String(100), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="PEN")
    bank_name = Column(String(100), nullable=False)
    bank_account_number = Column(String(50), nullable=False)
    cci = Column(String(20), nullable=False)
    status = Column(String(50), default="DISBURSED")
    executed_at = Column(DateTime, default=datetime.utcnow)

    sheet = relationship("InvoiceSheet", back_populates="disbursement")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Float, nullable=False)
    advance_amount = Column(Float, nullable=False)
    advance_rate = Column(Float, nullable=False)
    pricing_rate = Column(Float, nullable=False)
    pricing_timestamp = Column(String, nullable=False)  # guardamos el timestamp como string ISO
    monto_final = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)