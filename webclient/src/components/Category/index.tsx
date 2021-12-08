import React from 'react';

import './Category.scss';
import { TCategory } from '../../common/types';

interface ICategoryProps extends Omit<TCategory, 'id'> {}

const Category = ({ label, image, subCategories }: ICategoryProps) => {
  return (
    <div
      className="category"
      style={{
        background: `url(${image}) no-repeat`,
      }}
    >
      <p className="category__name">{label}</p>
    </div>
  );
};

export default Category;
