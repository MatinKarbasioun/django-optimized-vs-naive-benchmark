from typing import Optional

from drf_pydantic import BaseModel
from pydantic import Field, field_validator

from crm.value_objects import Gender


class CustomerSearchRequestDto(BaseModel):
    search: Optional[str] = Field(
        None,
        max_length=255,
        description="Search query across name and customer ID"
    )
    gender: Optional[Gender] = Field(None, description="Filter by gender")
    city: Optional[str] = Field(None, max_length=100, description="Filter by city name")
    country: Optional[str] = Field(None, max_length=100, description="Filter by country name")
    min_age: Optional[int] = Field(None, ge=0, le=150, description="Minimum age filter")
    max_age: Optional[int] = Field(None, ge=0, le=150, description="Maximum age filter")
    min_points: Optional[int] = Field(None, ge=0, description="Minimum loyalty points")
    max_points: Optional[int] = Field(None, ge=0, description="Maximum loyalty points")
    has_relationship: Optional[bool] = Field(
        None,
        description="Filter customers with/without loyalty relationship"
    )

    # Pagination
    page: int = Field(default=1, ge=1, description="Page number (1-based)")
    per_page: int = Field(default=50, ge=1, le=200, description="Items per page (max 200)")

    # Sorting
    ordering: Optional[str] = Field(
        default="created",
        regex=r'^-?(created|first_name|last_name|birthday|points|last_activity|city|country)$',
        description="Sort field (prefix with - for descending)"
    )

    @classmethod
    @field_validator('max_age')
    def validate_age_range(cls, v, values):
        """Validate age range is logical"""
        if v and 'min_age' in values and values['min_age']:
            if v < values['min_age']:
                raise ValueError('max_age must be greater than or equal to min_age')
        return v

    @classmethod
    @field_validator('max_points')
    def validate_points_range(cls, v, values):
        """Validate points range is logical"""
        if v and 'min_points' in values and values['min_points']:
            if v < values['min_points']:
                raise ValueError('max_points must be greater than or equal to min_points')
        return v

    class Config:
        schema_extra = {
            "example": {
                "search": "John",
                "gender": "M",
                "city": "New York",
                "min_age": 25,
                "max_age": 65,
                "min_points": 100,
                "has_relationship": True,
                "page": 1,
                "per_page": 50,
                "ordering": "-created"
            }
        }