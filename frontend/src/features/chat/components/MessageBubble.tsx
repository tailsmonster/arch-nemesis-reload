import type { ChatMessage } from '../types';
import styles from './MessageBubble.module.css';

type MessageBubbleProps = {
  message: ChatMessage;
};

export function MessageBubble({ message }: MessageBubbleProps) {
  if (message.role === 'system') {
    return <div className={styles.systemMessage}>{message.content}</div>;
  }

  const isPlayer = message.role === 'player';

  return (
    <article className={`${styles.messageRow} ${isPlayer ? styles.playerRow : styles.nemesisRow}`}>
      {!isPlayer && <div className={styles.avatar}>🐧</div>}
      <div className={styles.messageStack}>
        {!isPlayer && <strong className={styles.speaker}>ARCH NEMESIS</strong>}
        <div className={`${styles.bubble} ${isPlayer ? styles.playerBubble : styles.nemesisBubble}`}>{message.content}</div>
        <span className={styles.meta}>{isPlayer ? 'You' : message.createdAt}</span>
      </div>
    </article>
  );
}
