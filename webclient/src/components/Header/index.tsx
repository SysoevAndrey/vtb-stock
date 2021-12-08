import React from 'react';

import { useAppContext } from '../../context';
import './Header.scss';

const Header = () => {
  const { state } = useAppContext();

  return (
    <header className="header">
      <p className="header__logo">VTB.Корзина</p>
      <ul className="header__list">
        <li className="header__list-item">+7 (925) 999 88 77</li>
        <li className="header__list-item">
          {state.logged && <div className="header__profile"></div>}
        </li>
      </ul>
    </header>
  );
};

export default Header;
