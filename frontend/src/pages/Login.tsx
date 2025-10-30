import React, { useState } from 'react';
import { Button, TextField } from '@mui/material';
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
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <img src="/images/logo.png" alt="Growth-Wave Logo" style={{ width: '80px', verticalAlign: 'middle' }} />
          <div style={{ display: 'inline-block', verticalAlign: 'middle', marginLeft: '10px', textAlign: 'left' }}>
            <h1 style={{ margin: 0, fontSize: '24px' }}>Growth-Wave</h1>
            <p style={{ margin: 0, fontSize: '14px' }}>슈어소트테크 인사평가시스템</p>
          </div>
        </div>
        <h2>Login</h2>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <TextField
          label="사용자 이름"
          variant="outlined"
          fullWidth
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{ marginBottom: '10px' }}
        />
        <TextField
          type="password"
          label="비밀번호"
          variant="outlined"
          fullWidth
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ marginBottom: '10px' }}
        />
        <Button type="submit" variant="contained" color="primary" style={{ padding: '10px' }}>
          로그인
        </Button>
      </form>
    </div>
  );
};

export default Login;