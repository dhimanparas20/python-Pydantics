from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Union
from pydantic import (
    BaseModel, 
    EmailStr, 
    Field, 
    validator, 
    root_validator, 
    AnyUrl,
    constr, 
    conint, 
    confloat,
    SecretStr
)

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Subject(BaseModel):
    name: str
    code: str
    credits: int = Field(ge=1, le=6)

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"

class EmergencyContact(BaseModel):
    name: str
    relationship: str
    phone: str
    
    @validator('phone')
    def validate_phone(cls, v):
        if not v.replace('-', '').isdigit():
            raise ValueError('Phone must contain only digits and hyphens')
        return v

class Student(BaseModel):
    # Basic information
    id: int = Field(..., description="Unique student identifier")
    first_name: str
    last_name: str
    full_name: Optional[str] = None
    email: EmailStr
    password: SecretStr
    date_of_birth: date
    age: Optional[int] = None
    gender: Gender
    active: bool = True
    
    # Academic information
    gpa: confloat(ge=0.0, le=4.0) = 0.0
    subjects: List[Subject] = []
    favorite_subjects: Set[str] = set()
    grades: Dict[str, float] = {}
    
    # Contact information
    address: Address
    phone: Optional[str] = None
    website: Optional[AnyUrl] = None
    emergency_contacts: List[EmergencyContact] = []
    
    # Additional fields
    enrollment_date: datetime = Field(default_factory=datetime.now)
    graduation_year: Optional[int] = None
    notes: Optional[str] = Field(None, max_length=1000)
    tags: List[str] = []
    
    # Validators
    @validator('full_name', always=True)
    def set_full_name(cls, v, values):
        if v:
            return v
        if 'first_name' in values and 'last_name' in values:
            return f"{values['first_name']} {values['last_name']}"
        return v
    
    @validator('age', always=True)
    def calculate_age(cls, v, values):
        if v is not None:
            return v
        if 'date_of_birth' in values:
            today = date.today()
            dob = values['date_of_birth']
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return None
    
    @root_validator
    def check_graduation_year(cls, values):
        if values.get('graduation_year') and values.get('enrollment_date'):
            if values['graduation_year'] < values['enrollment_date'].year:
                raise ValueError('Graduation year cannot be before enrollment year')
        return values
    
    class Config:
        validate_assignment = True
        extra = "forbid"
        schema_extra = {
            "example": {
                "id": 12345,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "secret123",
                "date_of_birth": "2000-01-15",
                "gender": "male",
                "gpa": 3.5,
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "state": "CA",
                    "zip_code": "12345",
                    "country": "USA"
                }
            }
        }

# Create a student instance
student = Student(
    id=1001,
    first_name="Jane",
    last_name="Smith",
    email="jane.smith@university.edu",
    password="SecurePassword123",
    date_of_birth=date(2000, 5, 15),
    gender=Gender.FEMALE,
    gpa=3.8,
    subjects=[
        Subject(name="Computer Science", code="CS101", credits=4),
        Subject(name="Mathematics", code="MATH201", credits=3)
    ],
    favorite_subjects={"Computer Science", "Physics"},
    grades={"CS101": 95.5, "MATH201": 88.0},
    address=Address(
        street="456 University Ave",
        city="College Town",
        state="NY",
        zip_code="54321"
    ),
    phone="555-123-4567",
    website="https://jane-smith.portfolio.dev",
    emergency_contacts=[
        EmergencyContact(
            name="Robert Smith",
            relationship="Father",
            phone="555-987-6543"
        )
    ],
    graduation_year=2024,
    tags=["honors", "scholarship"]
)

# Print the student as JSON
print(student.json(indent=2))
