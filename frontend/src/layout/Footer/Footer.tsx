import type { GameState } from '../../features/games/types';
import styles from './Footer.module.css';

type FooterProps = {
  game: GameState;
};

export function Footer({ game }: FooterProps) {
  return (
    <footer className={styles.footer}>
      <Meter label="Persuasion" value={game.persuasion} tone="persuasion" />
      <Meter label="Anger" value={game.anger} tone="anger" />
      <p className={styles.status}>Status: {game.status.toUpperCase()}</p>
    </footer>
  );
}

type MeterProps = {
  label: string;
  tone: 'persuasion' | 'anger';
  value: number;
};

function Meter({ label, tone, value }: MeterProps) {
  return (
    <div className={styles.meterGroup}>
      <span>{label}</span>
      <div className={styles.track}>
        <div className={`${styles.fill} ${styles[tone]}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}
