import { useMemo, useState } from 'react';

import type { ChatMessage } from '../../chat/types';
import type { GameState, GameSummary } from '../types';

const initialGame: GameState = {
  id: 'game-5',
  title: 'Game 5',
  status: 'active',
  persuasion: 18,
  anger: 42,
  turnCount: 2,
  updatedAt: 'Just now',
};

const initialMessages: ChatMessage[] = [
  {
    id: 'm1',
    role: 'system',
    content: 'New duel started. Convince the Arch Nemesis to install Windows.',
    createdAt: '19:00',
  },
  {
    id: 'm2',
    role: 'nemesis',
    content: 'State your case, dual-boot apologist. I have pacman output more persuasive than you.',
    createdAt: '19:01',
  },
  {
    id: 'm3',
    role: 'player',
    content: 'Windows has better game compatibility, especially for multiplayer anti-cheat systems.',
    createdAt: '19:02',
  },
  {
    id: 'm4',
    role: 'system',
    content: 'Persuasion increased by 7. Anger increased by 4.',
    createdAt: '19:02',
  },
  {
    id: 'm5',
    role: 'nemesis',
    content: 'Better compatibility? Have you considered simply not playing garbage assembled by kernel-level spyware merchants?',
    createdAt: '19:03',
  },
];

const history: GameSummary[] = [
  initialGame,
  { id: 'game-4', title: 'Game 4', status: 'lost', persuasion: 43, anger: 100, turnCount: 9, updatedAt: 'Yesterday' },
  { id: 'game-3', title: 'Game 3', status: 'won', persuasion: 100, anger: 71, turnCount: 12, updatedAt: '2 days ago' },
  { id: 'game-2', title: 'Game 2', status: 'lost', persuasion: 25, anger: 100, turnCount: 7, updatedAt: 'Last week' },
  { id: 'game-1', title: 'Game 1', status: 'lost', persuasion: 8, anger: 100, turnCount: 4, updatedAt: 'Last week' },
];

function createId(prefix: string) {
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function createNemesisReply(argument: string) {
  if (/nvidia|driver/i.test(argument)) {
    return 'NVIDIA drivers? You came into my house and said the cursed words out loud. Incredible tactical error.';
  }

  if (/game|compat/i.test(argument)) {
    return 'Game compatibility is not an operating system philosophy. It is a hostage note written by launchers.';
  }

  return 'That was almost coherent, which is upsetting. Unfortunately for you, I run Arch and therefore outrank facts.';
}

export function useGame() {
  const [game, setGame] = useState<GameState>(initialGame);
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [games, setGames] = useState<GameSummary[]>(history);

  const canSubmit = game.status === 'active';

  function submitArgument(argument: string) {
    const trimmed = argument.trim();

    if (!trimmed || !canSubmit) {
      return;
    }

    const persuasionDelta = Math.min(12, Math.max(3, Math.round(trimmed.length / 18)));
    const angerDelta = /nvidia|registry|office|teams/i.test(trimmed) ? 11 : 5;
    const nextPersuasion = Math.min(100, game.persuasion + persuasionDelta);
    const nextAnger = Math.min(100, game.anger + angerDelta);
    const nextStatus = nextPersuasion >= 100 ? 'won' : nextAnger >= 100 ? 'lost' : 'active';
    const now = new Date();
    const createdAt = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const playerMessage: ChatMessage = {
      id: createId('player'),
      role: 'player',
      content: trimmed,
      createdAt,
    };

    const systemMessage: ChatMessage = {
      id: createId('system'),
      role: 'system',
      content: `Persuasion increased by ${persuasionDelta}. Anger increased by ${angerDelta}.`,
      createdAt,
    };

    const nemesisMessage: ChatMessage = {
      id: createId('nemesis'),
      role: 'nemesis',
      content: createNemesisReply(trimmed),
      createdAt,
    };

    const nextGame: GameState = {
      ...game,
      status: nextStatus,
      persuasion: nextPersuasion,
      anger: nextAnger,
      turnCount: game.turnCount + 1,
      updatedAt: 'Just now',
    };

    setGame(nextGame);
    setGames((currentGames) => currentGames.map((item) => (item.id === nextGame.id ? nextGame : item)));
    setMessages((currentMessages) => [...currentMessages, playerMessage, systemMessage, nemesisMessage]);
  }

  function startNewGame() {
    const now = new Date();
    const title = `Game ${games.length + 1}`;
    const nextGame: GameState = {
      id: createId('game'),
      title,
      status: 'active',
      persuasion: 0,
      anger: 12,
      turnCount: 0,
      updatedAt: 'Just now',
    };

    setGame(nextGame);
    setGames((currentGames) => [nextGame, ...currentGames]);
    setMessages([
      {
        id: createId('system'),
        role: 'system',
        content: `${title} started at ${now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}.`,
        createdAt: 'Now',
      },
      {
        id: createId('nemesis'),
        role: 'nemesis',
        content: 'Another challenger. Fine. Explain why I should trade pacman for a progress bar that lies.',
        createdAt: 'Now',
      },
    ]);
  }

  return useMemo(
    () => ({
      canSubmit,
      game,
      games,
      messages,
      startNewGame,
      submitArgument,
    }),
    [canSubmit, game, games, messages],
  );
}
