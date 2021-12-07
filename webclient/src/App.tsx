import React from 'react';

import Header from './components/Header';
import Auth from './pages/Auth';
import './App.scss';

function App() {
  return (
    <div className="App">
      <Header />
      <Auth />
    </div>
  );
}

export default App;
