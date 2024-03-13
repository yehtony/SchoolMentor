// App.js
import React, { useEffect, useState } from 'react';
import './App.css';
import ChatroomSidebar from './ChatroomSidebar';
import Chatroom from './Chatroom';
import ChatInput from './ChatInput';

const SecretKey = "20240116";
const encrypt = (content, secretKey) => {
  let result = '';
  for(let i = 0; i< content.length; i++){
      let charCode = content.charCodeAt(i) ^ secretKey.charCodeAt(i % secretKey.length);
      result += String.fromCharCode(charCode);
  }
  return btoa(result)
}



const App = () => {
  const [ipAddress, setIPAddress] = useState('')
  // const [userId, setUserId] = useState(AES.encrypt(Math.floor(Math.random() * 100000000), AESKey).toString()); // Example initial room ID
  const userId = encrypt(ipAddress, SecretKey);
  const [messages, setMessages] = useState([]); // Placeholder for messages
  useEffect(() => {
    fetch('https://api.ipify.org?format=json')
      .then(response => response.json())
      .then(data => setIPAddress(data.ip))
      .catch(error => console.log(error))
  }, []);

  if (messages.length==0){
    const defaultMessage ={ id: messages.length + 1, text: "哈囉! 有什麼想提問的嗎", sender: 'Bot' , className_p: "message_bot_p" , className_span: "message_bot_span"}
    setMessages(messages => [...messages, defaultMessage] );
  }



  const sendMessage = message => {

    // Implement logic to send a message to the current room
    // For example, an API call to send the message to the current room
    // Update the messages state accordingly

    if (message.trim() === "") return;
    const newMessage = { id: messages.length + 1, text: message, sender: 'Me', className_p: "message_user_p", className_span: "message_user_span"};
    
    setMessages(messages => [...messages, newMessage] );

    // Send POST request to Backend Service
    fetch('https://laughing-memory-5g46vqp5jgr27w6g-5005.app.github.dev/webhooks/rest/webhook/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            message: message,
            sender: userId,
        }),
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(element => {
          setMessages(messages => [...messages, { id: messages.length + 1, text: element.text, sender: 'Bot' , className_p: "message_bot_p" , className_span: "message_bot_span"}] );
        });
        
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    // Example: sendNewMessageToRoom(currentRoom, message).then(updatedMessages => setMessages(updatedMessages));
  };

  return (
    <div>
      <div className="forMb">
        <ChatroomSidebar/>
      </div>
      
      <div className="app" userId={userId}>
        <div className="forPc">
          <ChatroomSidebar/>
        </div>
        <div className="main">
          <Chatroom messages={messages} />
          <ChatInput sendMessage={sendMessage} />
        </div>
      </div>
    </div>

  );
};

export default App;
