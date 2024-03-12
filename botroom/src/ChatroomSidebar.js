// ChatroomSidebar.js
import React from 'react';

const ChatroomSidebar = () => {
  const tips = [
    { id: 1, title: 'conversation from a kid:' , content: " “like, nuclear power is like, when we use tiny, tiny things called atoms to make electricity.It's like having a super special toy that makes lots and lots of power.But some people say it's not good because it can be a little bit dangerous, like when you play with toys that might break.So, um, do I agree with having nuclear power as the main electric thingy in Taiwan?I think it's like deciding which flavor of ice cream is the best.some people like chocolate, and some people like vanilla.Maybe grown-ups can talk and think really hard to decide what's safest and best for everyone in Taiwan. It's like picking the yummiest ice cream, but way more serious!" },
    // Add more rooms as needed
  ];
  
  return (
    <div className="sidebar">
      <h2>Paragraph Question:<p style={{color: '#aa3333'}}>Do you agree with development the nuclear power as main electric source in Taiwan?</p></h2>
      <ul>
        {tips.map(tip => (
          <li>
            <div key={tip.id} >
              <p>{tip.title}</p>
              <p>{tip.content}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChatroomSidebar;
