import type { ReactNode } from 'react';

import styles from './AppShell.module.css';

type AppShellProps = {
  children: ReactNode;
  isSidebarCollapsed: boolean;
};

export function AppShell({ children, isSidebarCollapsed }: AppShellProps) {
  return <div className={`${styles.appShell} ${isSidebarCollapsed ? styles.collapsed : ''}`}>{children}</div>;
}
