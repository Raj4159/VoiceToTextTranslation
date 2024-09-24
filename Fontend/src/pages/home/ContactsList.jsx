import React from 'react';

const ContactsList = ({ contacts, activeContact, onSelectContact }) => {
  return (
    <div className="w-1/4 bg-[#202C33] text-white h-screen overflow-y-auto border-r-2 border-black">
      <h2 className="p-4 text-lg">Contacts</h2>
      <ul>
        {contacts.map((contact) => (
          <li
            key={contact.id}
            className={`p-4 cursor-pointer flex items-center gap-4 hover:bg-[#2A3942] ${
              activeContact?.id === contact.id ? 'bg-[#2A3942]' : ''
            }`}
            onClick={() => onSelectContact(contact)}
          >
            <img className="w-10 h-10 rounded-full" src={contact.avatar} alt={contact.name} />
            <span>{contact.name}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ContactsList;
