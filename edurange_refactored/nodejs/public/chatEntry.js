import React from 'react';
import ReactDOM from 'react-dom/client';
import ChatApp from './ChatApp';

const root = ReactDOM.createRoot(document.getElementById('chatEntry_id'));

root.render(
  <React.StrictMode>
    <ChatApp />
  </React.StrictMode>
);
