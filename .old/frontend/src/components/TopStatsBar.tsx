import { Button } from './ui/Button';
import { shortId } from '../lib/format';
import type { GameState } from '../types';

type TopStatsBarProps = {
  game: GameState | null;
  onOpenMenu: () => void;
};

export function TopStatsBar({ game, onOpenMenu }: TopStatsBarProps) {
  return (
    <header className="top-stats-bar">
      <Button className="mobile-only" onClick={onOpenMenu} variant="ghost" aria-label="Open menu">
        ☰
      </Button>
      <span>Game # {game ? shortId(game.id) : '—'}</span>
      <span>Score {game?.persuasion ?? 0}</span>
      <span>Time Elapsed</span>
    </header>
  );
}
