export type SubmitTurnRequest = {
  argument: string;
};

export type SubmitTurnResponse = {
  game_id: string;
  messages: unknown[];
};
