export type GameStatusValue = 'active' | 'won' | 'lost';

export type GameSummary = {
  id: string;
  title: string;
  status: GameStatusValue;
  persuasion: number;
  anger: number;
  turnCount: number;
  updatedAt: string;
};

export type GameState = GameSummary;
