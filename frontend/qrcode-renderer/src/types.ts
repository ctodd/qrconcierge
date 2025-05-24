export interface TokenResponse {
  token: string;
  expiration: number; // Unix timestamp in seconds
}

export interface TokenError {
  statusCode: number;
  message: string;
}

export interface TokenRequest {
  uniqueId: string;
  latitude?: number;
  longitude?: number;
}
