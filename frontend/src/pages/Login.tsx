import React, { useState } from 'react';
import api from '../services/api';

interface LoginProps {
  onLoginSuccess: () => void;
}

const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError('');
    try {
      const response = await api.auth.login(username, password);
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      onLoginSuccess();
    } catch (err) {
      setError('Failed to login. Please check your credentials.');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', width: '300px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
        <h2>Login</h2>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <input
          type="text"
          placeholder="사용자 이름"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{ marginBottom: '10px', padding: '8px' }}
        />
        <input
          type="password"
          placeholder="비밀번호"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ marginBottom: '10px', padding: '8px' }}
        />
        <button type="submit" style={{ padding: '10px' }}>로그인</button>
      </form>
    </div>
  );
};

export default Login;