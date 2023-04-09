import React, { useContext, useEffect, useState } from 'react'

export const ChatContext = React.createContext();

export function useChatContext() {
  return useContext(ChatContext);
}

export function ChatProvider({children}) {

  const [user, setUser] = useState(null);

  const value = {
    user, setUser
  }

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  )
}
