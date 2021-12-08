import axios from 'axios';
import React, { useEffect, useState } from 'react';

import { TCategory } from '../../common/types';
import Category from '../Category';
import './Categories.scss';

const Categories = () => {
  const [categories, setCategories] = useState<TCategory[]>([]);

  useEffect(() => {
    (async () => {
      const {
        data: { categories: fetchedCategories },
      } = await axios('/api/products/filters');

      setCategories(fetchedCategories);
    })();
  }, []);

  return (
    <div className="categories">
      <h2 className="categories__title">Категории товаров</h2>
      <div className="categories__list">
        {categories.map(({ id, label, image, subCategories }) => (
          <Category
            key={id}
            label={label}
            image={image}
            subCategories={subCategories}
          />
        ))}
      </div>
    </div>
  );
};

export default Categories;
