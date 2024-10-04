import React from 'react';

const ChatScreen = ({ activeContact, messages = [] }) => {
  return (
    <div className="flex-1 bg-[#1B1B1B] flex flex-col">
      {/* Chat Header */}
      <div className="bg-[#075E54] p-4 flex items-center gap-4 text-white">
        <img
          className="w-10 h-10 rounded-full"
          src={activeContact?.avatar}
          alt={activeContact?.name || 'Contact Avatar'}
        />
        <h2 className="font-bold">{activeContact?.name || 'Unknown'}</h2>
      </div>

      <div className="flex-1 p-4" style={{ maxHeight: 'calc(93vh - 90px)', overflowY: 'auto' }}>
        {messages.length > 0 ? (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`mb-4 flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.type === 'text' ? (
                <p className={`inline-block p-2 rounded-md ${msg.sender === 'user' ? 'bg-[#25D366]' : 'bg-[#2A2A2A] text-white'}`}>
                  {msg.content} {/* Use msg.content for text messages */}
                </p>
              ) : msg.type === 'audio' ? (
                <div className={`inline-block ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <audio controls className="bg-[#2A2A2A] rounded-md">
                    <source src={msg.content} type="audio/wav" />
                    Your browser does not support the audio element.
                  </audio>
                </div>
              ) : null}
            </div>
          ))
        ) : (
          <p className="text-gray-400">No messages yet.</p>
        )}
      </div>
    </div>
  );
};

export default ChatScreen;




// import React from 'react';

// const ChatScreen = ({ activeContact, messages }) => {
//   return (
//     <div className="flex-1 overflow-y-auto p-4">
//       {/* Header with active contact name */}
//       <div className="border-b border-gray-300 mb-4">
//         <h2 className="text-xl font-semibold">{activeContact.name}</h2>
//       </div>

//       {/* Messages display area */}
//       <div>
//         {messages.map((message, index) => (
//           <div key={index} className={`message ${message.sender}`}>
//             {message.type === 'text' ? (
//               <div className="text-message bg-blue-100 p-2 rounded-lg mb-2">
//                 <strong>{message.sender === 'user' ? 'You' : activeContact.name}:</strong>
//                 <p>{message.content}</p>
//               </div>
//             ) : message.type === 'audio' ? (
//               <div className="audio-message mb-2">
//                 <strong>{message.sender === 'user' ? 'You' : activeContact.name}:</strong>
//                 <audio controls className="mt-1">
//                   <source src={message.content} type="audio/wav" />
//                   Your browser does not support the audio element.
//                 </audio>
//               </div>
//             ) : null}
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// };

// export default ChatScreen;


// import React from 'react';

// const ChatScreen = ({ activeContact, messages = [] }) => {
//   return (
//     <div className="flex-1 bg-[#1B1B1B] flex flex-col justify-between">
//       {/* Chat Header */}
//       <div className="bg-[#075E54] p-4 flex items-center gap-4 text-white">
//         <img
//           className="w-10 h-10 rounded-full"
//           src={activeContact?.avatar}
//           alt={activeContact?.name || 'Contact Avatar'}
//         />
//         <h2 className="font-bold">{activeContact?.name || 'Unknown'}</h2>
//       </div>

//       {/* Messages */}
//       <div className="flex-1 p-4 overflow-y-auto">
//         {messages.length > 0 ? (
//           messages.map((msg, index) => (
//             <div
//               key={index}
//               className={`mb-4 flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
//             >
//               <p className={`inline-block p-2 rounded-md ${msg.sender === 'user' ? 'bg-[#25D366]' : 'bg-[#2A2A2A] text-white'}`}>
//                 {msg.text}
//               </p>
//             </div>
//           ))
//         ) : (
//           <p className="text-gray-400">No messages yet.</p>
//         )}
//       </div>
//     </div>
//   );
// };

// export default ChatScreen;

