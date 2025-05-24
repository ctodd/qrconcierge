import { useEffect, useState } from 'react';
import QRCode from 'qrcode.react';

interface QRCodeDisplayProps {
  token: string;
  expiration: number;
  onExpire: () => void;
}

const QRCodeDisplay = ({ token, expiration, onExpire }: QRCodeDisplayProps) => {
  const [timeLeft, setTimeLeft] = useState<number>(0);
  const [progress, setProgress] = useState<number>(100);
  
  useEffect(() => {
    // Calculate initial time left in seconds
    const expirationDate = new Date(expiration * 1000);
    const now = new Date();
    const initialTimeLeft = Math.max(0, Math.floor((expirationDate.getTime() - now.getTime()) / 1000));
    const totalDuration = initialTimeLeft;
    
    setTimeLeft(initialTimeLeft);
    
    // Set up countdown timer
    const timer = setInterval(() => {
      setTimeLeft((prevTime) => {
        if (prevTime <= 1) {
          clearInterval(timer);
          onExpire();
          return 0;
        }
        
        // Calculate progress percentage
        const newTimeLeft = prevTime - 1;
        const newProgress = (newTimeLeft / totalDuration) * 100;
        setProgress(newProgress);
        
        return newTimeLeft;
      });
    }, 1000);
    
    return () => clearInterval(timer);
  }, [token, expiration, onExpire]);
  
  // Format time left as MM:SS
  const formatTimeLeft = () => {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };
  
  return (
    <div className="qr-container">
      <QRCode value={token} size={256} level="H" />
      <div className="countdown">
        Expires in: {formatTimeLeft()}
        <div className="countdown-bar">
          <div 
            className="countdown-progress" 
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>
    </div>
  );
};

export default QRCodeDisplay;
