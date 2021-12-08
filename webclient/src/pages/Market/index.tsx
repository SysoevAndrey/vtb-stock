import React, { useEffect } from 'react';
import axios from 'axios';

const Market = () => {
  useEffect(() => {
    (async () => {
      const { data } = await axios.get('/api/products/filters');

      console.log(data);
    })();
  }, []);

  return <h1>Hello</h1>;
};

export default Market;
