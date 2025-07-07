from pydantic import BaseModel, Field
from typing import List, Optional, Union
from enum import Enum

class LoadType(str, Enum):
    POINT_MOMENT = "Point Moment"
    POINT_FORCE = "Point Force"
    CONSTANT_FORCE_PROFILE = "Constant Force Profile"
    TRIANGULAR_FORCE_PROFILE = "Triangular Force Profile"

class PointMoment(BaseModel):
    magnitude: float = Field(..., description="Moment magnitude in N-m")
    location: float = Field(..., ge=0, description="Location along beam in meters")

class PointForce(BaseModel):
    magnitude: float = Field(..., description="Force magnitude in N")
    location: float = Field(..., ge=0, description="Location along beam in meters")

class ConstantForceProfile(BaseModel):
    magnitude: float = Field(..., description="Distributed load magnitude in N/m")
    start_location: float = Field(..., ge=0, description="Start location in meters")
    end_location: float = Field(..., ge=0, description="End location in meters")

class TriangularForceProfile(BaseModel):
    magnitude: float = Field(..., description="Peak load magnitude in N")
    start_location: float = Field(..., ge=0, description="Start location in meters")
    end_location: float = Field(..., ge=0, description="End location in meters")

class BeamProperties(BaseModel):
    length: float = Field(..., gt=0, description="Beam length in meters")
    support1: float = Field(..., ge=0, description="First support location in meters")
    support2: float = Field(..., ge=0, description="Second support location in meters")
    modulus_of_elasticity: float = Field(default=1.0, gt=0, description="Modulus of elasticity in Pa")
    second_moment_of_area: float = Field(default=1.0, gt=0, description="Second moment of area in m^4")

class LoadRequest(BaseModel):
    load_type: LoadType
    load_data: Union[PointMoment, PointForce, ConstantForceProfile, TriangularForceProfile]

class BeamSession(BaseModel):
    session_id: str
    beam_properties: Optional[BeamProperties] = None
    point_moments: List[PointMoment] = []
    point_forces: List[PointForce] = []
    constant_force_profiles: List[ConstantForceProfile] = []
    triangular_force_profiles: List[TriangularForceProfile] = []

class AnalysisResults(BaseModel):
    shear_force: List[float]
    bending_moment: List[float]
    slope: List[float]
    deflection: List[float]
    x_coordinates: List[float]
    max_shear_force: float
    max_bending_moment: float
    max_deflection: float
    max_slope: float
    reaction_forces: List[float]

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
