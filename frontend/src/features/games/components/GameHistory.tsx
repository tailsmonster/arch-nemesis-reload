import type { GameSummary } from '../types';
import { GameHistoryItem } from './GameHistoryItem';
import styles from './GameHistory.module.css';

type GameHistoryProps = {
  activeGameId: string;
  games: GameSummary[];
  isCollapsed: boolean;
};

export function GameHistory({ activeGameId, games, isCollapsed }: GameHistoryProps) {
  return (
    <nav className={styles.history} aria-label="Game history">
      {games.map((game) => (
        <GameHistoryItem key={game.id} game={game} isActive={game.id === activeGameId} isCollapsed={isCollapsed} />
      ))}
    </nav>
  );
}
