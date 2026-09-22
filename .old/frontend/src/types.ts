export type GameStatus = 'active' | 'won' | 'lost';
export type PlayMode = 'chat' | 'fight' | 'complete';

export type GameState = {
  id: string;
  active_round_id: string;
  persuasion: number;
  anger: number;
  strikes: number;
  turn_count: number;
  status: GameStatus;
  mode: PlayMode;
};

export type Round = {
  id: string;
  round_number: number;
  status: string;
};

export type Turn = {
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

export type GameEvent = {
  id: string;
  event_type: string;
  message: string;
};

export type GameDetail = {
  game: GameState;
  active_round: Round;
  turns: Turn[];
  events: GameEvent[];
};

export type SubmitTurnResponse = {
  game: GameState;
  turn: Turn;
  turns: Turn[];
};
