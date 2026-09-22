import styles from './TypingIndicator.module.css';

export function TypingIndicator() {
  return (
    <div className={styles.typingIndicator} aria-label="Arch Nemesis is typing">
      <span />
      <span />
      <span />
    </div>
  );
}
