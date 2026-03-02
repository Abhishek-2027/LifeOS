# backend/app/services/reasoning_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.services.memory_service import MemoryService
from app.reasoning_engine.context_builder import ContextBuilder
from app.reasoning_engine.trend_analyzer import TrendAnalyzer
from app.reasoning_engine.conflict_detector import ConflictDetector
from app.reasoning_engine.decision_engine import DecisionEngine
from app.reasoning_engine.llm_reasoner import LLMReasoner


class ReasoningService:

    @staticmethod
    async def reason(db: AsyncSession, user_id, query: str):

        # 🔹 1. Retrieve relevant memories from PostgreSQL
        memories = await MemoryService.search_memory(
            db=db,
            user_id=user_id,
            query=query,
            k=5
        )

        if not memories:
            return {"message": "No relevant memories found."}

        # 🔹 2. Build structured context
        context_builder = ContextBuilder()
        context = context_builder.build(memories)

        # 🔹 3. Analyze trends
        trend_analyzer = TrendAnalyzer()
        trends = trend_analyzer.analyze(memories)

        # 🔹 4. Detect conflicts
        conflict_detector = ConflictDetector()
        conflict = conflict_detector.detect(memories)

        # 🔹 5. Decision logic
        decision_engine = DecisionEngine()
        decision = decision_engine.decide(trends, conflict)

        # 🔹 6. Final LLM reasoning
        llm = LLMReasoner()
        explanation = llm.reason(
            context=context,
            trends=trends,
            conflict=conflict,
            decision=decision,
            user_query=query
        )

        return {
            "retrieved_memories": [m.text for m in memories],
            "trend_analysis": trends,
            "conflict": conflict,
            "decision_summary": decision,
            "llm_explanation": explanation,
        }