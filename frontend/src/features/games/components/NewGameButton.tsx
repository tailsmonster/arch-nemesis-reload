type NewGameButtonProps = {
  onClick: () => void;
};

export function NewGameButton({ onClick }: NewGameButtonProps) {
  return (
    <button type="button" onClick={onClick}>
      + New Game
    </button>
  );
}
