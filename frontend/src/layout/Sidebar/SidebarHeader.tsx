import styles from './Sidebar.module.css';

type SidebarHeaderProps = {
  isCollapsed: boolean;
  onToggle: () => void;
};

export function SidebarHeader({ isCollapsed, onToggle }: SidebarHeaderProps) {
  return (
    <header className={styles.header}>
      <div className={styles.logo} aria-label="Arch Nemesis logo">
        <span>🐧</span>
        {!isCollapsed && <strong>ARCH NEMESIS</strong>}
      </div>
      <button className={styles.toggleButton} type="button" onClick={onToggle} aria-label="Toggle sidebar">
        {isCollapsed ? '»' : '«'}
      </button>
    </header>
  );
}
