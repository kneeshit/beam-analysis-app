import uuid
from typing import Dict, Optional
from .models import BeamSession, BeamProperties

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, BeamSession] = {}
    
    def create_session(self) -> str:
        """Create a new session and return session ID"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = BeamSession(session_id=session_id)
        return session_id
    
    def get_session(self, session_id: str) -> Optional[BeamSession]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def update_beam_properties(self, session_id: str, beam_properties: BeamProperties) -> bool:
        """Update beam properties for a session"""
        session = self.get_session(session_id)
        if session:
            session.beam_properties = beam_properties
            return True
        return False
    
    def clear_loads(self, session_id: str) -> bool:
        """Clear all loads for a session"""
        session = self.get_session(session_id)
        if session:
            session.point_moments.clear()
            session.point_forces.clear()
            session.constant_force_profiles.clear()
            session.triangular_force_profiles.clear()
            return True
        return False
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

# Global session manager instance
session_manager = SessionManager()
