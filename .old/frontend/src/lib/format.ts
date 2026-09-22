export function formatDelta(value: number) {
  return value >= 0 ? `+${value}` : `${value}`;
}

export function shortId(id: string) {
  return id.slice(0, 8);
}
