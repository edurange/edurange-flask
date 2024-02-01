import React, { useState } from 'react';

function EntryField({ onSendMessage }) {
  const [inputText, setInputText] = useState('');

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSendButtonClick = () => {
    if (inputText.trim() !== '') {
      onSendMessage(inputText);
      setInputText('');
    }
  };

  const handleEnterKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSendButtonClick();
    }
  };

  return (
    <div>
      <input
        type="text"
        value={inputText}
        onChange={handleInputChange}
        onKeyDown={handleEnterKeyDown}
      />
      <button onClick={handleSendButtonClick}>Send</button>
    </div>
  );
}

export default EntryField;
