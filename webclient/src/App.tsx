import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import Header from './components/Header';
import { useAppContext } from './context';
import Auth from './pages/Auth';
import './App.scss';
import Market from './pages/Market';

const App = () => {
  const { state } = useAppContext();

  return (
    <div className="App">
      <Header />
      <BrowserRouter>
        <Routes>
          <Route
            path="/login"
            element={!state.logged ? <Auth /> : <Navigate to="/" />}
          />
          <Route
            path="/*"
            element={state.logged ? <Market /> : <Navigate to="/login" />}
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
};

export default App;
