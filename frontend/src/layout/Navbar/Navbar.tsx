import type { GameState } from '../../features/games/types';
import styles from './Navbar.module.css';

type NavbarProps = {
  game: GameState;
};

export function Navbar({ game }: NavbarProps) {
  return (
    <header className={styles.navbar}>
      <div>
        <span className={styles.eyebrow}>Current duel</span>
        <h1>{game.title}</h1>
      </div>
      <dl className={styles.stats}>
        <div>
          <dt>Persuasion</dt>
          <dd>{game.persuasion}%</dd>
        </div>
        <div>
          <dt>Anger</dt>
          <dd>{game.anger}%</dd>
        </div>
        <div>
          <dt>Turns</dt>
          <dd>{game.turnCount}</dd>
        </div>
      </dl>
    </header>
  );
}
