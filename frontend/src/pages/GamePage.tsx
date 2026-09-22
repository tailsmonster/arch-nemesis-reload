import { Chat } from '../features/chat/components/Chat';
import { useGame } from '../features/games/hooks/useGame';
import { useSidebar } from '../features/sidebar/hooks/useSidebar';
import { AppShell } from '../layout/AppShell/AppShell';
import { Footer } from '../layout/Footer/Footer';
import { Navbar } from '../layout/Navbar/Navbar';
import { Sidebar } from '../layout/Sidebar/Sidebar';
import styles from './GamePage.module.css';

export function GamePage() {
  const { isCollapsed, toggleSidebar } = useSidebar(false);
  const gameSession = useGame();

  return (
    <AppShell isSidebarCollapsed={isCollapsed}>
      <Sidebar
        activeGameId={gameSession.game.id}
        games={gameSession.games}
        isCollapsed={isCollapsed}
        onNewGame={gameSession.startNewGame}
        onToggle={toggleSidebar}
      />
      <section className={styles.gameWorkspace}>
        <Navbar game={gameSession.game} />
        <Chat canSubmit={gameSession.canSubmit} messages={gameSession.messages} onSubmit={gameSession.submitArgument} />
        <Footer game={gameSession.game} />
      </section>
    </AppShell>
  );
}
