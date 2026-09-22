import type { GameSummary } from '../types';
import styles from './GameHistory.module.css';

type GameHistoryItemProps = {
  game: GameSummary;
  isActive: boolean;
  isCollapsed: boolean;
};

export function GameHistoryItem({ game, isActive, isCollapsed }: GameHistoryItemProps) {
  return (
    <button className={`${styles.item} ${isActive ? styles.active : ''}`} type="button">
      <span>{isCollapsed ? game.title.replace('Game ', '') : game.title}</span>
      {!isCollapsed && <small>{game.updatedAt}</small>}
    </button>
  );
}
