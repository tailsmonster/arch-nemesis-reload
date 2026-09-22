import { apiFetch } from './client';

export type GameDto = {
  id: string;
  title: string;
  status: string;
  persuasion: number;
  anger: number;
  turn_count: number;
};

export function listGames() {
  return apiFetch<GameDto[]>('/api/games');
}

export function createGame() {
  return apiFetch<GameDto>('/api/games', { method: 'POST' });
}
