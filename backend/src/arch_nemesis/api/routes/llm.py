from fastapi import APIRouter

from arch_nemesis.agents.director.service import evaluate_turn
from arch_nemesis.agents.fact_checker.service import fact_check
from arch_nemesis.agents.nemesis.service import respond
from arch_nemesis.api.schemas.llm import LLMResponse, LLMTextRequest
from arch_nemesis.game.rules import apply_director_evaluation

router = APIRouter()


@router.post("/fact-check", response_model=LLMResponse)
def direct_fact_check(request: LLMTextRequest) -> dict:
    result = fact_check(request.text, game_id=request.game_id)
    return {"result": result.model_dump()}


@router.post("/director-evaluate", response_model=LLMResponse)
def direct_director_evaluate(request: LLMTextRequest) -> dict:
    fact = fact_check(request.text, game_id=request.game_id)
    game = {"persuasion": 0, "anger": 0, "turn_count": 0}
    result = evaluate_turn(request.text, game, fact, game_id=request.game_id)
    return {"result": result.model_dump()}


@router.post("/respond", response_model=LLMResponse)
def direct_respond(request: LLMTextRequest) -> dict:
    fact = fact_check(request.text, game_id=request.game_id)
    game = {"persuasion": 0, "anger": 0, "turn_count": 0}
    director = evaluate_turn(request.text, game, fact, game_id=request.game_id)
    rules = apply_director_evaluation(director)
    result = respond(request.text, game, rules, game_id=request.game_id)
    return {"result": result.model_dump()}
