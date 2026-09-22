import type { GameState } from '../types';
import styles from './GameStatus.module.css';

type GameStatusProps = {
  game: GameState;
};

export function GameStatus({ game }: GameStatusProps) {
  return (
    <section className={styles.status}>
      <span>{game.status}</span>
      <strong>{game.persuasion}% persuaded</strong>
    </section>
  );
}
