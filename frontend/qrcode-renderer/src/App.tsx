import { useState, useEffect } from 'react';
import QRCodeDisplay from './components/QRCodeDisplay';
import { getToken } from './api';
import { TokenError, TokenResponse } from './types';

function App() {
  const [uniqueId, setUniqueId] = useState<string>('');
  const [latitude, setLatitude] = useState<string>('');
  const [longitude, setLongitude] = useState<string>('');
  const [tokenData, setTokenData] = useState<TokenResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchToken = async () => {
    if (!uniqueId) {
      setError('Please enter a unique ID (e.g., phone number)');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const request = {
        uniqueId,
        ...(latitude && longitude ? {
          latitude: parseFloat(latitude),
          longitude: parseFloat(longitude)
        } : {})
      };

      const response = await getToken(request);
      setTokenData(response);
    } catch (err) {
      const tokenError = err as TokenError;
      setError(tokenError.message);
      setTokenData(null);
    } finally {
      setLoading(false);
    }
  };

  // Auto-refresh token when it expires
  const handleTokenExpire = () => {
    if (uniqueId) {
      fetchToken();
    }
  };

  // Optional: Get user's location on initial load
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLatitude(position.coords.latitude.toString());
          setLongitude(position.coords.longitude.toString());
        },
        () => {
          // Silently fail if user denies location access
        }
      );
    }
  }, []);

  return (
    <div className="container">
      <h1>QR Code Generator</h1>
      
      <div className="input-group">
        <input
          type="text"
          placeholder="Enter unique ID (e.g., phone number)"
          value={uniqueId}
          onChange={(e) => setUniqueId(e.target.value)}
        />
        
        <div className="input-row">
          <input
            type="text"
            placeholder="Latitude (optional)"
            value={latitude}
            onChange={(e) => setLatitude(e.target.value)}
          />
          <input
            type="text"
            placeholder="Longitude (optional)"
            value={longitude}
            onChange={(e) => setLongitude(e.target.value)}
          />
        </div>
        
        <button onClick={fetchToken} disabled={loading}>
          {loading ? <span className="loading"></span> : 'Generate QR Code'}
        </button>
      </div>
      
      {error && <div className="error">{error}</div>}
      
      {tokenData && (
        <QRCodeDisplay
          token={tokenData.token}
          expiration={tokenData.expiration}
          onExpire={handleTokenExpire}
        />
      )}
    </div>
  );
}

export default App;
