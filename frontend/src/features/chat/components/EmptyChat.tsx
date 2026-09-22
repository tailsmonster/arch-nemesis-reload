import styles from './EmptyChat.module.css';

export function EmptyChat() {
  return (
    <section className={styles.emptyChat}>
      <div className={styles.mockBubbleLeft} />
      <div className={styles.mockBubbleRight} />
      <div className={styles.mockBubbleLeftWide} />
    </section>
  );
}
