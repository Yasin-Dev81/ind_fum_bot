from config import SQLALCHEMY_DATABASE_URL
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import requests
import os


# URL of the certificate
cert_url = "https://letsencrypt.org/certs/isrgrootx1.pem"
# Path to save the certificate locally
cert_path = os.path.join(os.path.dirname(__file__), 'certs', 'isrgrootx1.pem')

# Ensure the directory exists
os.makedirs(os.path.dirname(cert_path), exist_ok=True)

def down_cert():
    response = requests.get(cert_url)
    if response.status_code == 200:
        with open(cert_path, 'wb') as cert_file:
            cert_file.write(response.content)
        print("Certificate downloaded successfully.")
    else:
        print("Failed to download certificate:", response.status_code)

IS_SQLITE = SQLALCHEMY_DATABASE_URL.startswith("sqlite")

if IS_SQLITE:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
else:
    down_cert()
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=10,
        max_overflow=30,
        pool_recycle=3600,
        pool_timeout=10,
        connect_args={
            "ssl": {
                "ca": cert_path
            }
        }
        # pool_pre_ping=True,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    except exc.SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()
