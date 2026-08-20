from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from factoring_app.domain.entities import Base

# URL de conexión a la base de datos
DATABASE_URL = "postgresql://factoring_user:factoring_pass@db:5432/factoring_db"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Configuración de la sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Mantiene los objetos válidos después del commit
)

# Inicializar la base de datos y crear las tablas
def init_db():
    Base.metadata.create_all(bind=engine)
