// ChatroomSidebar.js
import React from 'react';

const ChatroomSidebar = () => {
  const tips = [
    { id: 1, title: '磁鐵' , content: "能知道磁鐵的發現科學史" },
    { id: 2, title: '磁鐵與磁力' , content: " “磁鐵的兩極為N極和S極，磁極間的磁力是一種超距力" },
    { id: 3, title: '磁力線與磁場' , content: "磁力線是假想線，可描述磁場的大小及方向" },  ];
  
  return (
    <div className="sidebar">
      <h2>After the class <p >Do you have questions about following units?</p></h2>
      <ul>
        {tips.map(tip => (
          <li>
            <div key={tip.id} >
              <p style={{color: '#aa3333'}}>{tip.title}</p>
              <p>{tip.content}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChatroomSidebar;
