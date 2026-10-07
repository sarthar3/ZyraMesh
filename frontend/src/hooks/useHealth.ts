import { useState, useEffect } from 'react';

export function useHealth() {
  const [isHealthy, setIsHealthy] = useState<boolean>(true);
  const [isReady, setIsReady] = useState<boolean>(true);
  const [dbStatus, setDbStatus] = useState<string>('healthy');
  const [redisStatus, setRedisStatus] = useState<string>('healthy');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch('/api/v1/ready');
        if (res.ok) {
          const data = await res.json();
          setIsReady(data.status === 'ready');
          setDbStatus(data.database?.status || 'unknown');
          setRedisStatus(data.redis?.status || 'unknown');
          setIsHealthy(true);
        } else {
          setIsReady(false);
          setIsHealthy(false);
        }
      } catch (e) {
        setIsReady(false);
        setIsHealthy(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 5000);
    return () => clearInterval(interval);
  }, []);

  return { isHealthy, isReady, dbStatus, redisStatus };
}
