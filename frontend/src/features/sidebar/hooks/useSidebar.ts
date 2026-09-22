import { useState } from 'react';

export function useSidebar(defaultCollapsed = false) {
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed);

  return {
    isCollapsed,
    toggleSidebar: () => setIsCollapsed((current) => !current),
  };
}
