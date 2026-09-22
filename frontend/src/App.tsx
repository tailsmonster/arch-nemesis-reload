import { FormEvent, useState } from 'react';

type GameStatus = 'active' | 'won' | 'lost';
type PlayMode = 'chat' | 'fight' | 'complete';

type GameState = {
  id: string;
  active_round_id: string;
  persuasion: number;
  anger: number;
  strikes: number;
  turn_count: number;
  status: GameStatus;
  mode: PlayMode;
};

type Round = {
  id: string;
  round_number: number;
  status: string;
};

type Turn = {
  id: string;
  round_id: string;
  turn_number: number;
  player_argument: string;
  nemesis_response: string;
  persuasion_delta: number;
  anger_delta: number;
  strike_delta: number;
  judge_reasoning: string;
  argument_quality: 'weak' | 'ok' | 'strong';
};

type GameEvent = {
  id: string;
  event_type: string;
  message: string;
};

type GameDetail = {
  game: GameState;
  active_round: Round;
  turns: Turn[];
  events: GameEvent[];
};

type SubmitTurnResponse = {
  game: GameState;
  turn: Turn;
  turns: Turn[];
};

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

export default function App() {
  const [game, setGame] = useState<GameState | null>(null);
  const [round, setRound] = useState<Round | null>(null);
  const [turns, setTurns] = useState<Turn[]>([]);
  const [events, setEvents] = useState<GameEvent[]>([]);
  const [argument, setArgument] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  async function startGame() {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/games`, { method: 'POST' });
      if (!response.ok) throw new Error('Could not create game.');
      const body = (await response.json()) as GameDetail;
      setGame(body.game);
      setRound(body.active_round);
      setTurns(body.turns);
      setEvents(body.events);
      setIsSidebarOpen(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error.');
    } finally {
      setIsLoading(false);
    }
  }

  async function submitTurn(event: FormEvent) {
    event.preventDefault();
    if (!game || !argument.trim()) return;

    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/games/${game.id}/turns`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ argument }),
      });
      if (!response.ok) throw new Error('Could not submit argument.');
      const body = (await response.json()) as SubmitTurnResponse;
      setGame(body.game);
      setTurns(body.turns);
      setArgument('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error.');
    } finally {
      setIsLoading(false);
    }
  }

  const canChat = game?.status === 'active' && game.mode === 'chat';

  return (
    <div className="app-shell">
      <aside className={`sidebar ${isSidebarOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <strong>Arch Nemesis</strong>
          <button className="icon-button mobile-only" onClick={() => setIsSidebarOpen(false)} aria-label="Close menu">
            ×
          </button>
        </div>
        <button className="new-game" onClick={startGame} disabled={isLoading}>
          New round
        </button>
        <nav className="round-list" aria-label="conversation history">
          {game ? (
            <button className="round-item active">
              <span>Round {round?.round_number ?? 1}</span>
              <small>{shortId(game.id)}</small>
            </button>
          ) : (
            <p className="muted">Start a round to create a conversation log.</p>
          )}
        </nav>
        <section className="event-log">
          <h2>Events</h2>
          {events.length === 0 ? <p className="muted">No events yet.</p> : events.map((event) => <p key={event.id}>{event.message}</p>)}
        </section>
      </aside>

      {isSidebarOpen && <button className="scrim mobile-only" onClick={() => setIsSidebarOpen(false)} aria-label="Close menu" />}

      <main className="player-column">
        <header className="topbar">
          <button className="icon-button mobile-only" onClick={() => setIsSidebarOpen(true)} aria-label="Open menu">
            ☰
          </button>
          <div>
            <strong>Arch Nemesis: Reload</strong>
            <span>{game ? `Game ${shortId(game.id)} · ${game.mode}` : 'No active round'}</span>
          </div>
        </header>

        <section className="stage" aria-label="player area">
          {game?.mode === 'fight' ? <FightPlaceholder game={game} /> : <ChatStage turns={turns} error={error} />}
        </section>

        <footer className="status-footer">
          <div className="meters" aria-label="game stats">
            <Meter label="Persuasion" value={game?.persuasion ?? 0} max={30} />
            <Meter label="Anger" value={game?.anger ?? 0} max={30} />
            <span className="stat-pill">Strikes: {game?.strikes ?? 0}/3</span>
            <span className="stat-pill">Turns: {game?.turn_count ?? 0}</span>
            <span className="stat-pill">Status: {game?.status ?? 'idle'}</span>
          </div>

          <form className="composer" onSubmit={submitTurn}>
            <textarea
              value={argument}
              onChange={(event) => setArgument(event.target.value)}
              placeholder={game ? 'Make your case for Windows...' : 'Start a round before arguing.'}
              disabled={!canChat || isLoading}
            />
            <button disabled={!canChat || isLoading || !argument.trim()}>Send</button>
          </form>
        </footer>
      </main>
    </div>
  );
}

function ChatStage({ turns, error }: { turns: Turn[]; error: string | null }) {
  return (
    <div className="chat-stage">
      {turns.length === 0 ? (
        <div className="empty-state">
          <h1>Convince the Arch zealot.</h1>
          <p>Use practical arguments: games, drivers, hardware, compatibility, work software, or usability.</p>
        </div>
      ) : (
        turns.map((turn) => (
          <article className="turn" key={turn.id}>
            <Message role="You" body={turn.player_argument} />
            <Message role="Arch Nemesis" body={turn.nemesis_response} />
            <div className="turn-feedback">
              <span>Persuasion {formatDelta(turn.persuasion_delta)}</span>
              <span>Anger {formatDelta(turn.anger_delta)}</span>
              {turn.strike_delta > 0 && <span>Strike +{turn.strike_delta}</span>}
              <span>{turn.argument_quality}</span>
              <p>{turn.judge_reasoning}</p>
            </div>
          </article>
        ))
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

function Message({ role, body }: { role: string; body: string }) {
  return (
    <div className="message-row">
      <div className="avatar">{role.slice(0, 1)}</div>
      <div className="message-copy">
        <strong>{role}</strong>
        <p>{body}</p>
      </div>
    </div>
  );
}

function FightPlaceholder({ game }: { game: GameState }) {
  return (
    <div className="fight-stage">
      <div className="arena-box">
        <p>Fight mode placeholder</p>
        <h1>Punch-Out style robot fight goes here.</h1>
        <span>Triggered by anger/strikes. Game {shortId(game.id)}</span>
      </div>
    </div>
  );
}

function Meter({ label, value, max }: { label: string; value: number; max: number }) {
  return (
    <label className="meter">
      <span>{label}</span>
      <progress value={value} max={max} />
      <small>{value}</small>
    </label>
  );
}

function formatDelta(value: number) {
  return value >= 0 ? `+${value}` : `${value}`;
}

function shortId(id: string) {
  return id.slice(0, 8);
}
