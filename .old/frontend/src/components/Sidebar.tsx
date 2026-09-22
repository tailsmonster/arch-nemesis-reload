import { Button } from './ui/Button';
import { shortId } from '../lib/format';
import type { GameEvent, GameState, Round } from '../types';

type SidebarProps = {
  events: GameEvent[];
  game: GameState | null;
  isLoading: boolean;
  isOpen: boolean;
  onClose: () => void;
  onStartGame: () => void;
  round: Round | null;
};

export function Sidebar({ events, game, isLoading, isOpen, onClose, onStartGame, round }: SidebarProps) {
  return (
    <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
      <div className="brand-card">
        <div className="logo-placeholder">ARCH NEMESIS</div>
        <Button className="mobile-only close-button" onClick={onClose} variant="ghost" aria-label="Close menu">
          ×
        </Button>
      </div>

      <nav className="menu-stack" aria-label="game navigation">
        {game ? (
          <button className="menu-item active">
            <span>Round {round?.round_number ?? 1}</span>
            <small>{shortId(game.id)}</small>
          </button>
        ) : (
          <p className="muted menu-copy">Start a game to create the first chat log.</p>
        )}
        <div className="menu-skeleton" />
        <div className="menu-skeleton" />
        <div className="menu-skeleton" />
        <div className="menu-skeleton" />
        <div className="menu-skeleton" />
      </nav>

      <section className="event-log">
        <h2>Events</h2>
        {events.length === 0 ? <p className="muted">No events yet.</p> : events.map((event) => <p key={event.id}>{event.message}</p>)}
      </section>

      <Button className="new-game-button" disabled={isLoading} onClick={onStartGame} variant="block">
        New Game
      </Button>
    </aside>
  );
}
