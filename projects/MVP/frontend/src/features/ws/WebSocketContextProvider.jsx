import { CompatClient, Stomp } from "@stomp/stompjs";
import { createContext, ReactNode, useContext, useEffect, useRef, useState } from "react";

// import {
//   createContext,
//   ReactNode,
//   useContext,
//   useEffect,
//   useRef,
//   useState,
// } from "react";


// Context to share the WebSocket client
const WsContext = createContext(null);

export const useWebSocket = () => useContext(WsContext);

export const WebSocketContextProvider = ({
  children,
  endpoint,
}) => {
  const [socket, setSocket] = useState(null);
  const socketRef = useRef(null);

  useEffect(() => {
    if (!endpoint) {
      console.error("WebSocket endpoint is missing");
      return;
    }

    const ws = new WebSocket(endpoint);

    ws.onopen = () => {
      console.log(`Connected to WebSocket: ${endpoint}`);
      setSocket(ws);
      socketRef.current = ws;
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("Message from server:", data);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
      setSocket(null);
    };

    return () => {
      ws.close();  
    };
  }, [endpoint]); 

  return (
    <WsContext.Provider value={socket}>
      {children}
    </WsContext.Provider>
  );
};
