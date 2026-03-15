from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
import re


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-password_hash", "-properties.user")

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="admin")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-many: User has many Properties
    properties = db.relationship("Property", back_populates="user", cascade="all, delete-orphan")

    @validates("email")
    def validate_email(self, key, value):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email address format.")
        return value

    @validates("username")
    def validate_username(self, key, value):
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters.")
        return value

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)  # apartment, house, commercial, land
    num_units = db.Column(db.Integer, default=1)
    monthly_rent = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FK to User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="properties")
    rent_payments = db.relationship(
        "RentPayment", back_populates="property", cascade="all, delete-orphan"
    )
    tenants = db.relationship(
        "Tenant", secondary="rent_payments", viewonly=True
    )

    @validates("monthly_rent")
    def validate_rent(self, key, value):
        if float(value) <= 0:
            raise ValueError("Monthly rent must be a positive number.")
        return value

    @validates("num_units")
    def validate_units(self, key, value):
        if int(value) < 1:
            raise ValueError("Number of units must be at least 1.")
        return value

    def __repr__(self):
        return f"<Property {self.name}>"

    # ✅ Safe JSON serialization for API
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "property_type": self.property_type,
            "num_units": self.num_units,
            "monthly_rent": self.monthly_rent,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id,
            "tenant_ids": [t.id for t in self.tenants],
            "rent_payment_ids": [r.id for r in self.rent_payments],
        }


class Tenant(db.Model):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    national_id = db.Column(db.String(50), unique=True)
    emergency_contact = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    rent_payments = db.relationship(
        "RentPayment",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )
    properties = db.relationship(
        "Property",
        secondary="rent_payments",
        viewonly=True
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "national_id": self.national_id,
            "emergency_contact": self.emergency_contact,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class RentPayment(db.Model):
    __tablename__ = "rent_payments"

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="pending")
    payment_method = db.Column(db.String(50), default="cash")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tenant = db.relationship("Tenant", back_populates="rent_payments")
    property = db.relationship("Property", back_populates="rent_payments")

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "property_id": self.property_id,
            "amount_paid": self.amount_paid,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status,
            "payment_method": self.payment_method,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }