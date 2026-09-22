import { useState } from 'react';

import { ChatComposer } from './components/ChatComposer';
import { FooterMeter } from './components/FooterMeter';
import { GameStage } from './components/GameStage';
import { Sidebar } from './components/Sidebar';
import { TopStatsBar } from './components/TopStatsBar';
import { useGameSession } from './hooks/useGameSession';

export default function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const session = useGameSession();

  async function startGame() {
    await session.startGame();
    setIsSidebarOpen(false);
  }

  return (
    <div className="app-shell">
      <Sidebar
        events={session.events}
        game={session.game}
        isLoading={session.isLoading}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        onStartGame={startGame}
        round={session.round}
      />

      {isSidebarOpen && <button className="scrim mobile-only" onClick={() => setIsSidebarOpen(false)} aria-label="Close menu" />}

      <main className="main-panel">
        <TopStatsBar game={session.game} onOpenMenu={() => setIsSidebarOpen(true)} />
        <div className="stage-shell">
          <GameStage error={session.error} game={session.game} turns={session.turns} />
          <ChatComposer
            canChat={session.canChat}
            isLoading={session.isLoading}
            onChange={session.setArgument}
            onSubmit={session.submitTurn}
            value={session.argument}
          />
        </div>
        <FooterMeter game={session.game} />
      </main>
    </div>
  );
}
