import type { FormEvent } from 'react';

import { Button } from './ui/Button';

type ChatComposerProps = {
  canChat: boolean;
  isLoading: boolean;
  onChange: (value: string) => void;
  onSubmit: (event: FormEvent) => void;
  value: string;
};

export function ChatComposer({ canChat, isLoading, onChange, onSubmit, value }: ChatComposerProps) {
  return (
    <form className="chat-composer" onSubmit={onSubmit}>
      <textarea
        aria-label="player argument"
        disabled={!canChat || isLoading}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Make this chatbox look EXACTLY like chatgpt. Even the way it expands and creates a scrollable textbox."
        rows={1}
        value={value}
      />
      <Button disabled={!canChat || isLoading || !value.trim()} type="submit" variant="ghost">
        ↑
      </Button>
    </form>
  );
}
