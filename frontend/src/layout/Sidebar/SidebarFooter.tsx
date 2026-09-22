import styles from './Sidebar.module.css';

type SidebarFooterProps = {
  isCollapsed: boolean;
  onNewGame: () => void;
};

export function SidebarFooter({ isCollapsed, onNewGame }: SidebarFooterProps) {
  return (
    <footer className={styles.footer}>
      <button className={styles.newGameButton} type="button" onClick={onNewGame}>
        <span>＋</span>
        {!isCollapsed && <span>New Game</span>}
      </button>
    </footer>
  );
}
