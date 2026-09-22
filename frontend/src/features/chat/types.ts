export type MessageRole = 'player' | 'nemesis' | 'system';

export type ChatMessage = {
  id: string;
  role: MessageRole;
  content: string;
  createdAt: string;
};
