import { GameHistory } from '../../features/games/components/GameHistory';
import type { GameSummary } from '../../features/games/types';
import { SidebarFooter } from './SidebarFooter';
import { SidebarHeader } from './SidebarHeader';
import styles from './Sidebar.module.css';

type SidebarProps = {
  activeGameId: string;
  games: GameSummary[];
  isCollapsed: boolean;
  onNewGame: () => void;
  onToggle: () => void;
};

export function Sidebar({ activeGameId, games, isCollapsed, onNewGame, onToggle }: SidebarProps) {
  return (
    <aside className={`${styles.sidebar} ${isCollapsed ? styles.collapsed : ''}`}>
      <SidebarHeader isCollapsed={isCollapsed} onToggle={onToggle} />
      <GameHistory activeGameId={activeGameId} games={games} isCollapsed={isCollapsed} />
      <SidebarFooter isCollapsed={isCollapsed} onNewGame={onNewGame} />
    </aside>
  );
}
