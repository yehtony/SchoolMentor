// ChatInput.js
import React, { useState } from 'react';

const ChatInput = ({ sendMessage }) => {
  const [input, setInput] = useState('');

  const handleSendMessage = () => {
    if (input.trim() !== '') {
      sendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        placeholder="Type a message..."
        value={input}
        onChange={e => setInput(e.target.value)}
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
};

export default ChatInput;
