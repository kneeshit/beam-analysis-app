from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import numpy as np

from .models import (
    BeamProperties, LoadRequest, LoadType, PointMoment, PointForce,
    ConstantForceProfile, TriangularForceProfile, AnalysisResults, ErrorResponse
)
from .session_manager import session_manager
from .calculations import calculate_structural_analysis
from .visualization import draw_beam, create_engineering_plot

app = FastAPI(title="Beam Analysis API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Beam Analysis API is running"}

@app.post("/api/session/create")
async def create_session():
    """Create a new session"""
    session_id = session_manager.create_session()
    return {"session_id": session_id}

@app.post("/api/session/{session_id}/beam-properties")
async def set_beam_properties(session_id: str, beam_properties: BeamProperties):
    """Set beam properties for a session"""
    if not session_manager.get_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Validate support locations
    if beam_properties.support1 >= beam_properties.length or beam_properties.support2 >= beam_properties.length:
        raise HTTPException(status_code=400, detail="Support locations must be within beam length")
    
    if beam_properties.support1 == beam_properties.support2:
        raise HTTPException(status_code=400, detail="Support locations must be different")
    
    success = session_manager.update_beam_properties(session_id, beam_properties)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Beam properties updated successfully"}

@app.post("/api/session/{session_id}/loads/add")
async def add_load(session_id: str, load_request: LoadRequest):
    """Add a load to the session"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session.beam_properties:
        raise HTTPException(status_code=400, detail="Beam properties must be set first")
    
    beam_length = session.beam_properties.length
    
    # Validate load location/range
    if load_request.load_type == LoadType.POINT_MOMENT:
        load_data = load_request.load_data
        if load_data.location >= beam_length:
            raise HTTPException(status_code=400, detail="Load location must be within beam length")
        session.point_moments.append(load_data)
    
    elif load_request.load_type == LoadType.POINT_FORCE:
        load_data = load_request.load_data
        if load_data.location >= beam_length:
            raise HTTPException(status_code=400, detail="Load location must be within beam length")
        session.point_forces.append(load_data)
    
    elif load_request.load_type == LoadType.CONSTANT_FORCE_PROFILE:
        load_data = load_request.load_data
        if load_data.start_location >= beam_length or load_data.end_location > beam_length:
            raise HTTPException(status_code=400, detail="Load range must be within beam length")
        if load_data.start_location >= load_data.end_location:
            raise HTTPException(status_code=400, detail="Start location must be less than end location")
        session.constant_force_profiles.append(load_data)
    
    elif load_request.load_type == LoadType.TRIANGULAR_FORCE_PROFILE:
        load_data = load_request.load_data
        if load_data.start_location >= beam_length or load_data.end_location > beam_length:
            raise HTTPException(status_code=400, detail="Load range must be within beam length")
        if load_data.start_location >= load_data.end_location:
            raise HTTPException(status_code=400, detail="Start location must be less than end location")
        session.triangular_force_profiles.append(load_data)
    
    return {"message": "Load added successfully"}

@app.get("/api/session/{session_id}/loads")
async def get_loads(session_id: str):
    """Get all loads for a session"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "point_moments": session.point_moments,
        "point_forces": session.point_forces,
        "constant_force_profiles": session.constant_force_profiles,
        "triangular_force_profiles": session.triangular_force_profiles
    }

@app.delete("/api/session/{session_id}/loads/clear")
async def clear_loads(session_id: str):
    """Clear all loads for a session"""
    success = session_manager.clear_loads(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "All loads cleared successfully"}

@app.post("/api/session/{session_id}/calculate")
async def calculate_analysis(session_id: str):
    """Perform structural analysis calculation"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session.beam_properties:
        raise HTTPException(status_code=400, detail="Beam properties must be set first")
    
    # Convert loads to the format expected by the calculation function
    f1 = [[m.magnitude, m.location] for m in session.point_moments]
    f2 = [[f.magnitude, f.location] for f in session.point_forces]
    f3 = [[p.magnitude, p.start_location, p.end_location] for p in session.constant_force_profiles]
    f4 = [[p.magnitude, p.start_location, p.end_location] for p in session.triangular_force_profiles]
    
    beam_props = session.beam_properties
    
    try:
        V, BM, slope, deflection, reaction_forces = calculate_structural_analysis(
            f1, f2, f3, f4,
            beam_props.support1, beam_props.support2, beam_props.length,
            beam_props.modulus_of_elasticity, beam_props.second_moment_of_area
        )
        
        # Create x-coordinates
        x_coordinates = np.linspace(0, beam_props.length, len(V)).tolist()
        
        # Calculate maximum values
        max_shear_force = max(map(abs, V)) if V else 0
        max_bending_moment = max(map(abs, BM)) if BM else 0
        max_deflection = max(map(abs, deflection)) if deflection else 0
        max_slope = max(map(abs, slope)) if slope else 0
        
        # Extract reaction forces from the returned reaction_forces list
        reactions = [rf[0] for rf in reaction_forces] if reaction_forces else [0, 0]
        
        return AnalysisResults(
            shear_force=V,
            bending_moment=BM,
            slope=slope,
            deflection=deflection,
            x_coordinates=x_coordinates,
            max_shear_force=max_shear_force,
            max_bending_moment=max_bending_moment,
            max_deflection=max_deflection,
            max_slope=max_slope,
            reaction_forces=reactions
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.get("/api/session/{session_id}/beam-image")
async def get_beam_image(session_id: str):
    """Generate and return beam schematic image"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session.beam_properties:
        raise HTTPException(status_code=400, detail="Beam properties must be set first")
    
    # Convert loads to the format expected by the visualization function
    f1 = [[m.magnitude, m.location] for m in session.point_moments]
    f2 = [[f.magnitude, f.location] for f in session.point_forces]
    f3 = [[p.magnitude, p.start_location, p.end_location] for p in session.constant_force_profiles]
    f4 = [[p.magnitude, p.start_location, p.end_location] for p in session.triangular_force_profiles]
    
    beam_props = session.beam_properties
    
    try:
        image_base64 = draw_beam(
            beam_props.length, beam_props.support1, beam_props.support2,
            f1, f2, f3, f4
        )
        return {"image": image_base64}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation error: {str(e)}")

@app.get("/api/session/{session_id}/plot/{plot_type}")
async def get_engineering_plot(session_id: str, plot_type: str):
    """Generate engineering diagram plots"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session.beam_properties:
        raise HTTPException(status_code=400, detail="Beam properties must be set first")
    
    # First calculate the analysis
    f1 = [[m.magnitude, m.location] for m in session.point_moments]
    f2 = [[f.magnitude, f.location] for f in session.point_forces]
    f3 = [[p.magnitude, p.start_location, p.end_location] for p in session.constant_force_profiles]
    f4 = [[p.magnitude, p.start_location, p.end_location] for p in session.triangular_force_profiles]
    
    beam_props = session.beam_properties
    
    try:
        V, BM, slope, deflection, _ = calculate_structural_analysis(
            f1, f2, f3, f4,
            beam_props.support1, beam_props.support2, beam_props.length,
            beam_props.modulus_of_elasticity, beam_props.second_moment_of_area
        )
        
        x_coordinates = np.linspace(0, beam_props.length, len(V)).tolist()
        
        # Generate the requested plot
        if plot_type == "shear":
            image_base64 = create_engineering_plot(
                x_coordinates, V, "Shear Force Diagram", "Beam Length (m)", "Shear Force (N)",
                beam_props.support1, beam_props.support2
            )
        elif plot_type == "moment":
            image_base64 = create_engineering_plot(
                x_coordinates, BM, "Bending Moment Diagram", "Beam Length (m)", "Bending Moment (N⋅m)",
                beam_props.support1, beam_props.support2
            )
        elif plot_type == "slope":
            image_base64 = create_engineering_plot(
                x_coordinates, slope, "Slope Diagram", "Beam Length (m)", "Slope (rad)",
                beam_props.support1, beam_props.support2
            )
        elif plot_type == "deflection":
            image_base64 = create_engineering_plot(
                x_coordinates, deflection, "Deflection Diagram", "Beam Length (m)", "Deflection (m)",
                beam_props.support1, beam_props.support2
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid plot type. Use: shear, moment, slope, or deflection")
        
        return {"image": image_base64}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plot generation error: {str(e)}")

@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    success = session_manager.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
