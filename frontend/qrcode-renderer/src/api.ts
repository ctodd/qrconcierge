import axios from 'axios';
import { TokenRequest, TokenResponse } from './types';

const API_BASE_URL = 'https://lgnd27dxvc.execute-api.us-east-1.amazonaws.com/prod';

export const getToken = async (request: TokenRequest): Promise<TokenResponse> => {
  try {
    const params: Record<string, string> = {
      uniqueId: request.uniqueId,
    };
    
    if (request.latitude !== undefined && request.longitude !== undefined) {
      params.latitude = request.latitude.toString();
      params.longitude = request.longitude.toString();
    }
    
    const response = await axios.get<TokenResponse>(`${API_BASE_URL}/getToken`, {
      params,
    });
    
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const statusCode = error.response?.status || 500;
      let message = 'Failed to retrieve token';
      
      if (statusCode === 403) {
        message = 'Access denied. Your ID may not exist or is blacklisted.';
      } else if (statusCode === 404) {
        message = 'Token service not found.';
      } else if (statusCode === 429) {
        message = 'Too many requests. Please try again later.';
      } else if (statusCode >= 500) {
        message = 'Server error. Please try again later.';
      }
      
      throw { statusCode, message };
    }
    throw { statusCode: 500, message: 'Unknown error occurred' };
  }
};
