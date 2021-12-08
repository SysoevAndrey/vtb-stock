export type TCategory = {
  id: string;
  label: string;
  image: string;
  subCategories: TCategory[];
};
