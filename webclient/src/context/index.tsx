import React, { FC, useContext, useReducer } from 'react';

interface IState {
  logged: boolean;
}

type TActions = { type: 'SIGN_IN' } | { type: 'SIGN_OUT' };

type Reducer = (state: IState, action: TActions) => IState;

const initialState: IState = {
  logged: false,
};

const reducer: Reducer = (state: IState, action: TActions) => {
  switch (action.type) {
    case 'SIGN_IN':
      return { ...state, logged: true };
    case 'SIGN_OUT':
      return { ...state, logged: false };
  }
};

const AppContext = React.createContext<{
  state: IState;
  dispatch: React.Dispatch<TActions>;
}>({
  state: initialState,
  dispatch: () => null,
});

const AppProvider: FC = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => useContext(AppContext);

export { AppContext, AppProvider, initialState };
