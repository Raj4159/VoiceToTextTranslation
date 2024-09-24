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
              <p className={`inline-block p-2 rounded-md ${msg.sender === 'user' ? 'bg-[#25D366]' : 'bg-[#2A2A2A] text-white'}`}>
                {msg.text}
              </p>
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

