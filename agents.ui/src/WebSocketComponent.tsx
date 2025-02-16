import React, { useState, useEffect, useRef } from "react";

const WebSocketComponent: React.FC = () => {
  const [message, setMessage] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const websocket = useRef<WebSocket | null>(null);

  useEffect(() => {
    websocket.current = new WebSocket(
      `ws://${import.meta.env.VITE_API_BASE_URL}/`
    );

    websocket.current.onopen = () => {
      console.log("WebSocket connection established");
    };

    websocket.current.onmessage = (event: MessageEvent) => {
      setResponse(event.data);
    };

    websocket.current.onclose = () => {
      console.log("WebSocket connection closed");
    };

    return () => {
      websocket.current?.close();
    };
  }, []);

  const sendMessage = () => {
    websocket.current?.send(message);
    setMessage("");
  };

  return (
    <div>
      <h1>Funny Name Maker</h1>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your name"
      />
      <button onClick={sendMessage}>Send</button>
      <div>
        <h2>Response:</h2>
        <p>{response}</p>
      </div>
    </div>
  );
};

export default WebSocketComponent;
