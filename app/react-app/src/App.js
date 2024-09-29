import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import pinataImage from '../src/images/Pinata.jpg'
import awsimage from '../src/images/aws.jpg'
function App() {
    const chatMessagesRef = useRef();
    const [messages, setMessages] = useState([]);
    const [userInput, setUserInput] = useState('');
    const [isWaiting, setIsWaiting] = useState(false);
    const [lastMessageTime, setLastMessageTime] = useState(0);
    const [isChatOpen, setIsChatOpen] = useState(false);
    const RATE_LIMIT_DELAY = 1000;

    useEffect(() => {
        if (chatMessagesRef.current) {
            chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
        }
    }, [messages]);

    const addMessage = (content, isUser = false, sources = [], isError = false) => {
        const message = { content, isUser, sources, isError };
        setMessages((prevMessages) => [...prevMessages, message]);
    };

    const sendMessage = async () => {
        const message = userInput.trim();
        if (message && !isWaiting) {
            addMessage(message, true);
            setUserInput('');
            setIsWaiting(true);

            try {
                const response = await fetch('http://localhost:5000/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                addMessage(data.response, false, data.sources);
            } catch (error) {
                console.error('Error:', error);
                addMessage(`Error: ${error.message}`, false, [], true);
            } finally {
                setIsWaiting(false);
            }
        }
    };

    const rateLimitedSendMessage = async () => {
        const now = Date.now();
        if (now - lastMessageTime < RATE_LIMIT_DELAY) {
            addMessage("Please wait a moment before sending another message.", false, [], true);
            return;
        }
        setLastMessageTime(now);
        await sendMessage();
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            rateLimitedSendMessage();
        }
    };

    const toggleChat = () => {
        setIsChatOpen(!isChatOpen);
    };

    return (
        <div className="app-container">
            <div className="sidebar">
                <div className="logo">AI Chatbot</div>
                <nav>
                    <ul>
                        <li><a href="#home">Home</a></li>
                        <li><a href="#about">About</a></li>
                        <li><a href="#contact">Contact</a></li>
                    </ul>
                </nav>
                <button className="chat-toggle" onClick={toggleChat}>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path fillRule="evenodd" d="M4.848 2.771A49.144 49.144 0 0112 2.25c2.43 0 4.817.178 7.152.52 1.978.292 3.348 2.024 3.348 3.97v6.02c0 1.946-1.37 3.678-3.348 3.97a48.901 48.901 0 01-3.476.383.39.39 0 00-.297.17l-2.755 4.133a.75.75 0 01-1.248 0l-2.755-4.133a.39.39 0 00-.297-.17 48.9 48.9 0 01-3.476-.384c-1.978-.29-3.348-2.024-3.348-3.97V6.741c0-1.946 1.37-3.68 3.348-3.97zM6.75 8.25a.75.75 0 01.75-.75h9a.75.75 0 010 1.5h-9a.75.75 0 01-.75-.75zm.75 2.25a.75.75 0 000 1.5H12a.75.75 0 000-1.5H7.5z" clipRule="evenodd" />
                    </svg>
                    Open Chatbot
                </button>
            </div>
            <div className="main-content">
                <h1 className="welcome-text">Welcome to Your Decentralized AI Chatbot!</h1>
                <h2 className="powered-by-text">Powered by Pinata and AWS Bedrock</h2>
                <div className="image-container">
                    <img src={pinataImage} alt="Pinata Logo" className="tech-logo" />
                    <img src={awsimage} alt="AWS Bedrock Logo" className="tech-logo" />
                </div>
            </div>
            {isChatOpen && (
                <div className="chat-widget">
                    <div className="chat-header">
                        <h2>AI Chatbot</h2>
                        <button className="close-btn" onClick={toggleChat}>×</button>
                    </div>
                    <div className="chat-messages" ref={chatMessagesRef}>
                        {messages.map((msg, index) => (
                            <div key={index} className={`message ${msg.isUser ? 'user-message' : 'bot-message'} ${msg.isError ? 'error' : ''}`}>
                                <div className="message-content">{msg.content}</div>
                                {msg.sources.length > 0 && (
                                    <div className="sources">
                                        Sources: {msg.sources.map((source, i) => (
                                            <a key={i} href={source.trim().replace(/^["'\s]+|["'\s]+$/g, '')} target="_blank" rel="noopener noreferrer">
                                                {source}
                                            </a>
                                        )).reduce((prev, curr) => [prev, ', ', curr])}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                    <div className="chat-input">
                        <input
                            type="text"
                            value={userInput}
                            onChange={(e) => setUserInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Type your message..."
                        />
                        <button onClick={rateLimitedSendMessage}>Send</button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;