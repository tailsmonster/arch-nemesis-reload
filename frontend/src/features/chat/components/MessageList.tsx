import type { ChatMessage } from '../types';
import { EmptyChat } from './EmptyChat';
import { MessageBubble } from './MessageBubble';
import styles from './MessageList.module.css';

type MessageListProps = {
  messages: ChatMessage[];
};

export function MessageList({ messages }: MessageListProps) {
  if (messages.length === 0) {
    return <EmptyChat />;
  }

  return (
    <section className={styles.messageList} aria-label="Conversation">
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
    </section>
  );
}
