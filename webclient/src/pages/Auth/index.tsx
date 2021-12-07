import React, { useState } from 'react';

import { useAppContext } from '../../context';
import './Auth.scss';

const Auth = () => {
  const { dispatch } = useAppContext();

  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');

  const signIn = () => {
    console.log(login, password);
    
    dispatch({ type: 'SIGN_IN' });
  };

  return (
    <div className="auth">
      <div className="auth__form">
        <h1 className="auth__title">Вход</h1>
        <input
          autoComplete="off"
          className="input auth__input"
          onChange={({ target: { value } }) => setLogin(value)}
          placeholder="Логин"
          type="text"
          value={login}
        />
        <input
          autoComplete="off"
          className="input auth__input"
          onChange={({ target: { value } }) => setPassword(value)}
          placeholder="Пароль"
          type="password"
          value={password}
        />
        <div className="auth__buttons">
          <button
            className="button button_primary auth__button"
            onClick={signIn}
          >
            Войти
          </button>
          <button className="button auth__button">
            Войти с помощью VTB ID
          </button>
        </div>
      </div>
    </div>
  );
};

export default Auth;
