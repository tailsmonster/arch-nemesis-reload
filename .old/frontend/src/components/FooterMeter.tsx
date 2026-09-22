import type { GameState } from '../types';

const MAX_PERSUASION = 2500;

type FooterMeterProps = {
  game: GameState | null;
};

export function FooterMeter({ game }: FooterMeterProps) {
  const persuasion = game?.persuasion ?? 0;
  const percent = Math.round((persuasion / MAX_PERSUASION) * 100);

  return (
    <footer className="footer-meter">
      <div className="meter-copy">
        Persuasion Meter: {percent}% ({persuasion}/{MAX_PERSUASION})
      </div>
      <div className="meter-track">
        <div className="meter-fill" style={{ width: `${Math.min(percent, 100)}%` }} />
      </div>
    </footer>
  );
}
