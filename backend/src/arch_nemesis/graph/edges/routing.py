LINEAR_TURN_FLOW = [
    "load_context",
    "llm_fact_check",
    "llm_director_evaluate",
    "apply_rules",
    "llm_nemesis_respond",
    "persist_turn",
]

APPLICATION_FLOW_NODES = [
    "client_chat_ui",
    "api_create_or_select_game",
    "api_select_round_id",
    "db_load_game_context",
    "api_submit_player_argument",
    "graph_turn_start",
    *LINEAR_TURN_FLOW,
    "api_return_updated_state",
    "client_render_state",
    "await_next_player_turn",
]
