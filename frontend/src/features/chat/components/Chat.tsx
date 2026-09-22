import type { ChatMessage } from '../types';
import { MessageComposer } from './MessageComposer';
import { MessageList } from './MessageList';
import styles from './Chat.module.css';

type ChatProps = {
  canSubmit: boolean;
  messages: ChatMessage[];
  onSubmit: (argument: string) => void;
};

export function Chat({ canSubmit, messages, onSubmit }: ChatProps) {
  return (
    <main className={styles.chat}>
      <div className={styles.scrollArea}>
        <MessageList messages={messages} />
      </div>
      <div className={styles.composerDock}>
        <MessageComposer canSubmit={canSubmit} onSubmit={onSubmit} />
      </div>
    </main>
  );
}
