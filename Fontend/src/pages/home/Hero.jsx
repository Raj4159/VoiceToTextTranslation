import React, { useState } from 'react';
import ContactsList from './ContactsList';
import ChatScreen from './ChatScreen';
import ChatInput from './ChatInput';

const Hero = () => {
  // Dummy contact list
  const contacts = [
    { id: 1, name: 'Alice', avatar: 'https://randomuser.me/api/portraits/women/1.jpg' },
    { id: 2, name: 'Bob', avatar: 'https://randomuser.me/api/portraits/men/2.jpg' },
    { id: 3, name: 'Charlie', avatar: 'https://randomuser.me/api/portraits/men/3.jpg' },
    { id: 3, name: 'daemon', avatar: 'https://randomuser.me/api/portraits/men/4.jpg' },
    { id: 3, name: 'ramlal', avatar: 'https://randomuser.me/api/portraits/men/5.jpg' },
    { id: 3, name: 'bhagwan', avatar: 'https://randomuser.me/api/portraits/men/6.jpg' },
    { id: 3, name: 'shamu', avatar: 'https://randomuser.me/api/portraits/men/7.jpg' },
    { id: 3, name: 'Chandu', avatar: 'https://randomuser.me/api/portraits/men/8.jpg' },
    { id: 3, name: 'harley', avatar: 'https://randomuser.me/api/portraits/men/9.jpg' },
    { id: 3, name: 'osama bin ladin', avatar: 'https://randomuser.me/api/portraits/men/10.jpg' },
  ];

  const [activeContact, setActiveContact] = useState(null);
  const [messages, setMessages] = useState([]);

  const handleSelectContact = (contact) => {
    setActiveContact(contact);
    setMessages([]); // Clear messages for the new contact
  };

  const handleSendMessage = (messageText) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: messageText, sender: 'user' },
    ]);

    // Simulate a bot response after 1 second
    setTimeout(() => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: 'This is a dummy response.', sender: 'bot' },
      ]);
    }, 1000);
  };

  return (
    <div className="h-screen flex overflow-hidden">
      {/* Contacts list on the left */}
      <ContactsList
        contacts={contacts}
        activeContact={activeContact}
        onSelectContact={handleSelectContact}
      />

      {/* Main chat area */}
      {activeContact ? (
        <div className="flex-1 flex flex-col">
          {/* ChatScreen with a fixed height to allow scrolling */}
          <div className="flex-1 flex flex-col">
            <ChatScreen activeContact={activeContact} messages={messages} />
          </div>
          {/* ChatInput at the bottom */}
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
      ) : (
        <div className="w-3/4 bg-[#0B141A] flex items-center justify-center text-white">
          <h2>Select a contact to start chatting</h2>
        </div>
      )}
    </div>
  );
};

export default Hero;



// import React, { useState } from 'react';
// import ContactsList from './ContactsList';
// import ChatScreen from './ChatScreen';
// import ChatInput from './ChatInput';

// const Hero = () => {
//   // Dummy contact list
//   const contacts = [
//     { id: 1, name: 'Alice', avatar: 'https://randomuser.me/api/portraits/women/1.jpg' },
//     { id: 2, name: 'Bob', avatar: 'https://randomuser.me/api/portraits/men/2.jpg' },
//     { id: 3, name: 'Charlie', avatar: 'https://randomuser.me/api/portraits/men/3.jpg' },
//     // Add more contacts if needed
//   ];

//   const [activeContact, setActiveContact] = useState(null);
//   const [messages, setMessages] = useState([]);

//   const handleSelectContact = (contact) => {
//     setActiveContact(contact);
//     setMessages([]); // Clear messages for the new contact
//   };

//   const handleSendMessage = (messageText) => {
//     // Add user message
//     setMessages((prevMessages) => [
//       ...prevMessages,
//       { text: messageText, sender: 'user' }
//     ]);

//     // Simulate a bot response after 1 second
//     setTimeout(() => {
//       setMessages((prevMessages) => [
//         ...prevMessages,
//         { text: 'This is a dummy response.', sender: 'bot' }
//       ]);
//     }, 1000);
//   };

//   return (
//     <div className="h-screen flex">
//       {/* Contacts list on the left */}
//       <ContactsList
//         contacts={contacts}
//         activeContact={activeContact}
//         onSelectContact={handleSelectContact}
//       />
      
//       {/* Main chat area */}
//       {activeContact ? (
//         <div className="flex-1 flex flex-col">
//           {/* ChatScreen takes up the middle area, with scrolling */}
//           <ChatScreen activeContact={activeContact} messages={messages} />
          
//           {/* ChatInput at the bottom */}
//           <ChatInput onSendMessage={handleSendMessage} />
//         </div>
//       ) : (
//         // Placeholder screen when no contact is selected
//         <div className="w-3/4 bg-[#0B141A] flex items-center justify-center text-white">
//           <h2>Select a contact to start chatting</h2>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Hero;
