import React, { useState } from 'react';

function ConnectionInfo() {
  const [text, setText] = useState('');
  
  const handleTextChange = (e) => {
    setText(e.target.value);
  };

  const handleCopyClick = () => {
    navigator.clipboard.writeText(text).then(() => {
      alert('Text copied to clipboard');
    }).catch(err => {
      alert('Failed to copy text to clipboard');
    });
  };

  return (
    <div>
      <input type="text" value={text} onChange={handleTextChange} />
      <button onClick={handleCopyClick}>Copy to Clipboard</button>
    </div>
  );
}

export default ConnectionInfo;
