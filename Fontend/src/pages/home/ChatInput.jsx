import React, { useState, useRef } from 'react';
import { MdMic } from 'react-icons/md';
import axios from 'axios';

const TRANSLATE_LANGUAGES = {
  Hindi: "hin_Deva",
  Assamese: "asm_Beng",
  Bengali: "ben_Beng",
  Bodo: "brx_Deva",
  Dogri: "doi_Deva",
  Konkani: "gom_Deva",
  Gujarati: "guj_Gujr",
  Kannada: "kan_Knda",
  Sanskrit: "san_Deva",
  Punjabi: "pan_Guru",
  Malayalam: "mal_Mlym",
  Odia: "ory_Orya",
  Nepali: "npi_Deva",
  Maithili: "mai_Deva",
  Santali: "sat_Olck",
  Marathi: "mar_Deva",
  Tamil: "tam_Taml",
  Telugu: "tel_Telu",
  English: "eng_Latn",
  Urdu: "urd_Arab",
};

const ChatInput = ({ onSendMessage }) => {
  const [messageText, setMessageText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('Hindi'); // Target language
  const [srcLanguage, setSrcLanguage] = useState('Hindi'); // Source language
  const [mode, setMode] = useState('Text'); // 'Text' or 'Speech'
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);

  const startRecording = async () => {
    setIsRecording(true);
    setShowPopup(true);
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      audioChunks.current = [];

      mediaRecorder.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.current.push(event.data);
        }
      };

      mediaRecorder.current.start();
    }
  };

  const stopRecording = () => {
    setIsRecording(false);
    setShowPopup(false);
    if (mediaRecorder.current) {
      mediaRecorder.current.stop();
      mediaRecorder.current.onstop = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/wav' });
        const audioFile = new File([audioBlob], 'file.wav', { type: 'audio/wav' });

        const formData = new FormData();
        formData.append('audio', audioFile);
        formData.append('tgt_lang', TRANSLATE_LANGUAGES[selectedLanguage]);

        try {
          // Call the transcribe and translate API
          const response = await axios.post('http://127.0.0.1:8000/app/transcribe_and_translate/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          // Display the transcription and translation result in the chat
          const { transcription, translation, detected_language } = response.data;
          onSendMessage({type: 'text', content: translation});
        } catch (error) {
          console.error('Error during transcription or translation:', error);
          onSendMessage({type: 'text', content: 'Failed to transcribe or translate the audio.'});
        }
      };
    }
  };


  const handleSendClick = async () => {
    if (messageText.trim()) {
      const tgt_lang = TRANSLATE_LANGUAGES[selectedLanguage];
      const src_lang = TRANSLATE_LANGUAGES[srcLanguage];

      try {
        // Construct the URL with query parameters
        const params = new URLSearchParams({
          text: messageText,  // No need to encode manually, URLSearchParams will handle it
          tgt_lang: tgt_lang,
          src_lang: src_lang,
        });

        // Make the API request using axios with the query parameters
        const response = await axios.post(`http://127.0.0.1:8000/app/Translate_Text/?${params}`, {}, {
          headers: {
            'Accept': 'application/json',  // Ensure JSON response
          },
        });

        // Handle response and show translated text in chat
        const { translated_text } = response.data;
        onSendMessage({ type: 'text', content: translated_text }); // Include type and content
      } catch (error) {
        console.error('Error during text translation:', error);
        onSendMessage({ type: 'text', content: 'Failed to translate the text.' }); // Include type and content
      }

      setMessageText('');  // Clear the message input after sending
    }
  };

  const handleSendSpeech = async () => {
    if (messageText.trim()) {
      const tgt_lang = TRANSLATE_LANGUAGES[selectedLanguage];
      const src_lang = TRANSLATE_LANGUAGES[srcLanguage];

      try {
        // Construct the URL for the Text-to-Speech API
        const params = new URLSearchParams({
          text: messageText,
          src_lang: src_lang,
          tgt_lang: tgt_lang,
        });

        // Make the API request using axios and specify the response type as 'blob'
        const response = await axios.post(`http://127.0.0.1:8000/app/Text_to_Speech/?${params}`, {}, {
          headers: {
            'Accept': 'audio/wav',
          },
          responseType: 'blob',  // Get the audio file as a binary large object (blob)
        });

        // Create a blob URL from the response data
        const audioBlob = new Blob([response.data], { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);

        // Send the audio URL as a message
        onSendMessage({ type: 'audio', content: audioUrl }); // Include type and content

      } catch (error) {
        console.error('Error during speech generation:', error);
        onSendMessage({ type: 'audio', content: 'Failed to generate speech.' }); // Include type and content
      }

      setMessageText('');  // Clear the message input after sending
    }
  };
  

  return (
    <div className="bg-[#2A2A2A] p-4 flex items-center gap-2 shadow-md">
      {/* Container for source language selection */}
      <div className="flex items-center">
        <label className="text-white mr-2">Source:</label>
        <select
          className="border border-[#CFCFCF] rounded-full p-2 bg-[#3A3A3A] text-white"
          value={srcLanguage}
          onChange={(e) => setSrcLanguage(e.target.value)}
        >
          {Object.keys(TRANSLATE_LANGUAGES).map((lang) => (
            <option key={TRANSLATE_LANGUAGES[lang]} value={lang}>
              {lang}
            </option>
          ))}
        </select>
      </div>

      {/* Container for target language selection */}
      <div className="flex items-center">
        <label className="text-white mr-2">Target:</label>
        <select
          className="border border-[#CFCFCF] rounded-full p-2 bg-[#3A3A3A] text-white"
          value={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
        >
          {Object.keys(TRANSLATE_LANGUAGES).map((lang) => (
            <option key={TRANSLATE_LANGUAGES[lang]} value={lang}>
              {lang}
            </option>
          ))}
        </select>
      </div>

      <input
        className="flex-1 p-2 rounded-full border border-[#CFCFCF] bg-[#3A3A3A] text-white"
        type="text"
        placeholder="Type a message..."
        value={messageText}
        onChange={(e) => setMessageText(e.target.value)}
        onKeyPress={(e) => {
          if (e.key === 'Enter') {
            if (mode === 'Text') {
              handleSendClick();  // Call the text translation API
            } else if (mode === 'Speech') {
              handleSendSpeech(); // Call the speech generation API
            }
          }
        }}
        style={{ color: 'white' }}
      />

      <button
        className="bg-[#25D366] p-2 rounded-full text-white"
        onClick={mode === 'Speech' ? handleSendSpeech : handleSendClick}
      >
        Send
      </button>
      <button
        className={`bg-[${isRecording ? '#FF0000' : '#25D366'}] p-2 rounded-full text-white`}
        onClick={startRecording}
      >
        <MdMic size={20} />
      </button>

      {/* New dropdown for Text/Speech mode (independent feature) */}
      <div className="flex items-center">
        <label className="text-white mr-2">Mode:</label>
        <select
          className="border border-[#CFCFCF] rounded-full p-2 bg-[#3A3A3A] text-white"
          value={mode}
          onChange={(e) => setMode(e.target.value)}
        >
          <option value="Text">Text</option>
          <option value="Speech">Speech</option>
        </select>
      </div>

      {/* Pop-up for Stop and Send */}
      {showPopup && (
        <div className="popup bg-[#3A3A3A] p-4 rounded-lg shadow-md absolute bottom-20 right-10 text-white">
          <p>Recording... Press Stop to Save</p>
          <button
            className="bg-[#FF0000] p-2 rounded-full text-white mt-2"
            onClick={stopRecording}
          >
            Stop and Send
          </button>
        </div>
      )}
    </div>
  );
};

export default ChatInput;
