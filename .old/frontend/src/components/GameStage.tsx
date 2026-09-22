import { formatDelta } from '../lib/format';
import type { GameState, Turn } from '../types';

type GameStageProps = {
  error: string | null;
  game: GameState | null;
  turns: Turn[];
};

export function GameStage({ error, game, turns }: GameStageProps) {
  if (game?.mode === 'fight') {
    return (
      <section className="game-stage fight-stage" aria-label="fight stage">
        <div className="fight-card">
          <p>Fight mode placeholder</p>
          <h1>Punch-Out robot fight area</h1>
          <span>This can become a fullscreen sprite/canvas stage.</span>
        </div>
      </section>
    );
  }

  return (
    <section className="game-stage" aria-label="chat stage">
      {turns.length === 0 ? (
        <div className="chat-empty">
          <div className="mock-message mock-message-left" />
          <div className="mock-message mock-message-right" />
          <div className="mock-message mock-message-left wide" />
        </div>
      ) : (
        <div className="conversation-log">
          {turns.map((turn) => (
            <article className="turn-pair" key={turn.id}>
              <ChatBubble align="left" label="You" message={turn.player_argument} />
              <ChatBubble align="right" label="Arch Nemesis" message={turn.nemesis_response} />
              <div className="turn-points">
                <span>Persuasion {formatDelta(turn.persuasion_delta)}</span>
                <span>Anger {formatDelta(turn.anger_delta)}</span>
                {turn.strike_delta > 0 && <span>Strike +{turn.strike_delta}</span>}
                <span>{turn.argument_quality}</span>
                <p>{turn.judge_reasoning}</p>
              </div>
            </article>
          ))}
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </section>
  );
}

function ChatBubble({ align, label, message }: { align: 'left' | 'right'; label: string; message: string }) {
  return (
    <div className={`chat-bubble-wrap ${align === 'right' ? 'chat-bubble-wrap-right' : ''}`}>
      <div className="chat-bubble">
        <strong>{label}</strong>
        <p>{message}</p>
      </div>
    </div>
  );
}
