import React from 'react';

import Advertisement from '../../components/Advertisement';
import Categories from '../../components/Categories';
import './Market.scss';

const Market = () => {
  return (
    <div className="market">
      <Advertisement />
      <Categories />
    </div>
  );
};

export default Market;
