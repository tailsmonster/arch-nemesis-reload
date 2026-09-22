import { FormEvent, useState } from 'react';

type GameStatus = 'active' | 'won' | 'lost';

type GameState = {
  id: number;
  persuasion: number;
  anger: number;
  turn_count: number;
  status: GameStatus;
};

type Turn = {
  id: number;
  turn_number: number;
  player_argument: string;
  nemesis_response: string;
  persuasion_delta: number;
  anger_delta: number;
  judge_reasoning: string;
  argument_quality: 'weak' | 'ok' | 'strong';
};

type GameDetail = {
  game: GameState;
  turns: Turn[];
};

type SubmitTurnResponse = GameDetail & {
  turn: Turn;
};

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

export default function App() {
  const [game, setGame] = useState<GameState | null>(null);
  const [turns, setTurns] = useState<Turn[]>([]);
  const [argument, setArgument] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function startGame() {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/games`, { method: 'POST' });
      if (!response.ok) throw new Error('Could not create game.');
      const body = (await response.json()) as GameDetail;
      setGame(body.game);
      setTurns(body.turns);
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

  return (
    <main className="shell">
      <header>
        <p className="eyebrow">Arch Nemesis: Reload</p>
        <h1>Convince an Arch zealot to install Windows.</h1>
        <p className="summary">
          Start a persistent game, argue your case, and watch deterministic state change after a LangGraph turn.
        </p>
      </header>

      <section className="panel controls">
        <button onClick={startGame} disabled={isLoading}>
          {game ? 'Restart Game' : 'Start Game'}
        </button>
        {game && (
          <div className="stats" aria-label="game stats">
            <span>Game #{game.id}</span>
            <span>Persuasion: {game.persuasion}</span>
            <span>Anger: {game.anger}</span>
            <span>Turns: {game.turn_count}</span>
            <span>Status: {game.status}</span>
          </div>
        )}
      </section>

      {error && <p className="error">{error}</p>}

      <section className="panel conversation" aria-label="turn history">
        {turns.length === 0 ? (
          <p className="empty">No arguments yet. Say something persuasive about drivers, games, or compatibility.</p>
        ) : (
          turns.map((turn) => (
            <article className="exchange" key={turn.id}>
              <div className="message player">
                <strong>You</strong>
                <p>{turn.player_argument}</p>
              </div>
              <div className="message nemesis">
                <strong>Arch Nemesis</strong>
                <p>{turn.nemesis_response}</p>
              </div>
              <p className="judge">
                Judge: {turn.argument_quality} · Persuasion {formatDelta(turn.persuasion_delta)} · Anger{' '}
                {formatDelta(turn.anger_delta)} — {turn.judge_reasoning}
              </p>
            </article>
          ))
        )}
      </section>

      <form className="panel composer" onSubmit={submitTurn}>
        <textarea
          value={argument}
          onChange={(event) => setArgument(event.target.value)}
          placeholder="Explain why Windows might actually be the pragmatic choice..."
          disabled={!game || game.status !== 'active' || isLoading}
        />
        <button disabled={!game || game.status !== 'active' || isLoading || !argument.trim()}>
          Submit Argument
        </button>
      </form>
    </main>
  );
}

function formatDelta(value: number) {
  return value >= 0 ? `+${value}` : `${value}`;
}
