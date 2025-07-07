import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

class BeamAnalysisAPI {
  constructor() {
    this.sessionId = null;
    this.axiosInstance = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
    });
  }

  async createSession() {
    try {
      console.log('Creating session...');
      const response = await this.axiosInstance.post('/session/create');
      this.sessionId = response.data.session_id;
      console.log('Session created:', this.sessionId);
      return this.sessionId;
    } catch (error) {
      console.error('Error creating session:', error);
      console.error('Error details:', error.response?.data || error.message);
      throw error;
    }
  }

  async setBeamProperties(beamProperties) {
    if (!this.sessionId) {
      throw new Error('No active session');
    }
    
    try {
      const response = await this.axiosInstance.post(
        `/session/${this.sessionId}/beam-properties`,
        beamProperties
      );
      return response.data;
    } catch (error) {
      console.error('Error setting beam properties:', error);
      throw error;
    }
  }

  async addLoad(loadType, loadData) {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    try {
      const response = await this.axiosInstance.post(
        `/session/${this.sessionId}/loads/add`,
        {
          load_type: loadType,
          load_data: loadData
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error adding load:', error);
      throw error;
    }
  }

  async getLoads() {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    try {
      const response = await this.axiosInstance.get(`/session/${this.sessionId}/loads`);
      return response.data;
    } catch (error) {
      console.error('Error getting loads:', error);
      throw error;
    }
  }

  async clearLoads() {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    try {
      const response = await this.axiosInstance.delete(`/session/${this.sessionId}/loads/clear`);
      return response.data;
    } catch (error) {
      console.error('Error clearing loads:', error);
      throw error;
    }
  }

  async calculateAnalysis() {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    try {
      const response = await this.axiosInstance.post(`/session/${this.sessionId}/calculate`);
      return response.data;
    } catch (error) {
      console.error('Error calculating analysis:', error);
      throw error;
    }
  }

  async getBeamImage() {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    try {
      const response = await this.axiosInstance.get(`/session/${this.sessionId}/beam-image`);
      return response.data.image;
    } catch (error) {
      console.error('Error getting beam image:', error);
      throw error;
    }
  }

  async getEngineeringPlot(plotType) {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    try {
      const response = await this.axiosInstance.get(`/session/${this.sessionId}/plot/${plotType}`);
      return response.data.image;
    } catch (error) {
      console.error('Error getting engineering plot:', error);
      throw error;
    }
  }

  async deleteSession() {
    if (!this.sessionId) {
      return;
    }

    try {
      await this.axiosInstance.delete(`/session/${this.sessionId}`);
      this.sessionId = null;
    } catch (error) {
      console.error('Error deleting session:', error);
    }
  }
}

export default new BeamAnalysisAPI();
