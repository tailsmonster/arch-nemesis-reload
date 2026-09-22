import { FormEvent, useState } from 'react';

import { createGame, submitArgument } from '../lib/api';
import type { GameEvent, GameState, Round, Turn } from '../types';

export function useGameSession() {
  const [game, setGame] = useState<GameState | null>(null);
  const [round, setRound] = useState<Round | null>(null);
  const [turns, setTurns] = useState<Turn[]>([]);
  const [events, setEvents] = useState<GameEvent[]>([]);
  const [argument, setArgument] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function startGame() {
    setIsLoading(true);
    setError(null);
    try {
      const body = await createGame();
      setGame(body.game);
      setRound(body.active_round);
      setTurns(body.turns);
      setEvents(body.events);
      setArgument('');
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
      const body = await submitArgument(game.id, argument);
      setGame(body.game);
      setTurns(body.turns);
      setArgument('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error.');
    } finally {
      setIsLoading(false);
    }
  }

  return {
    argument,
    canChat: game?.status === 'active' && game.mode === 'chat',
    error,
    events,
    game,
    isLoading,
    round,
    setArgument,
    startGame,
    submitTurn,
    turns,
  };
}
