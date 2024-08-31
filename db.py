from sqlalchemy import create_engine, Column, Integer, ForeignKey, StaticPool, String, Float
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

# Create a connection to the database
engine = create_engine("sqlite+pysqlite:///:memory:",
                       echo=True,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool)

Session = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# Datasets model
class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    routes = relationship("Route", back_populates="dataset", cascade="all, delete-orphan")
    expires_date = Column(String, nullable=False)
    expires_timezone_type = Column(Integer, nullable=False)
    expires_timezone = Column(String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'expires_date': self.expires_date,
            'expires_timezone_type': self.expires_timezone_type,
            'expires_timezone': self.expires_timezone,
            'routes': [route.to_dict() for route in self.routes]
        }


# Data model with a foreign key to the datasets table
class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False, index=True)
    dataset = relationship("Dataset", back_populates="routes")
    uuid = Column(String, nullable=False, unique=True)
    from_id = Column(String, nullable=False)
    from_name = Column(String, nullable=False)
    to_id = Column(String, nullable=False)
    to_name = Column(String, nullable=False)
    distance = Column(Integer, nullable=False)
    schedule = relationship("Schedule", back_populates="route", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'from_id': self.from_id,
            'from_name': self.from_name,
            'to_id': self.to_id,
            'to_name': self.to_name,
            'distance': self.distance,
            'schedule': [schedule.to_dict() for schedule in self.schedule]
        }


# Schedule model with a foreign key to the routes table
class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False, index=True)
    route = relationship("Route", back_populates="schedule")
    uuid = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    start_date = Column(String, nullable=False)
    start_timezone_type = Column(Integer, nullable=False)
    start_timezone = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    end_timezone_type = Column(Integer, nullable=False)
    end_timezone = Column(String, nullable=False)
    company_id = Column(String, nullable=False)
    company_state = Column(String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'price': self.price,
            'start_date': self.start_date,
            'start_timezone_type': self.start_timezone_type,
            'start_timezone': self.start_timezone,
            'end_date': self.end_date,
            'end_timezone_type': self.end_timezone_type,
            'end_timezone': self.end_timezone,
            'company_id': self.company_id,
            'company_state': self.company_state
        }


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    from_name = Column(String, nullable=False)
    to_name = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    start_timezone_type = Column(Integer, nullable=False)
    start_timezone = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    end_timezone_type = Column(Integer, nullable=False)
    end_timezone = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    operator_name = Column(String, nullable=False)


# Create the tables
Base.metadata.create_all(engine)
