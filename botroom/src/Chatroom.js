// Chatroom.js
import React from 'react';

const Chatroom = ({ messages }) => {
  return (
    <div className="chatroom">
      {messages.map(message => (
        <div key={message.id} >
          <p className={message.className_p}>{message.text}</p>
          <p className={message.className_span}>{message.sender}</p>
        </div>
      ))}
    </div>
  );
};

export default Chatroom;
