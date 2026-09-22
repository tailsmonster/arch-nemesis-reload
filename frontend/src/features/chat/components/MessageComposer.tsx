import { FormEvent, useState } from 'react';

import styles from './MessageComposer.module.css';

type MessageComposerProps = {
  canSubmit: boolean;
  onSubmit: (argument: string) => void;
};

export function MessageComposer({ canSubmit, onSubmit }: MessageComposerProps) {
  const [value, setValue] = useState('');

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = value.trim();

    if (!trimmed || !canSubmit) {
      return;
    }

    onSubmit(trimmed);
    setValue('');
  }

  return (
    <form className={styles.composer} onSubmit={handleSubmit}>
      <textarea
        aria-label="Argument"
        disabled={!canSubmit}
        onChange={(event) => setValue(event.target.value)}
        placeholder="Make your case for Windows without triggering a package manager lecture..."
        rows={1}
        value={value}
      />
      <button disabled={!canSubmit || value.trim().length === 0} type="submit" aria-label="Send argument">
        ↑
      </button>
    </form>
  );
}
