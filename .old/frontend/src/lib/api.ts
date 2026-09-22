import type { GameDetail, SubmitTurnResponse } from '../types';

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

async function assertOk(response: Response, message: string) {
  if (!response.ok) {
    throw new Error(message);
  }
}

export async function createGame(): Promise<GameDetail> {
  const response = await fetch(`${API_BASE}/games`, { method: 'POST' });
  await assertOk(response, 'Could not create game.');
  return response.json() as Promise<GameDetail>;
}

export async function submitArgument(gameId: string, argument: string): Promise<SubmitTurnResponse> {
  const response = await fetch(`${API_BASE}/games/${gameId}/turns`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ argument }),
  });
  await assertOk(response, 'Could not submit argument.');
  return response.json() as Promise<SubmitTurnResponse>;
}
