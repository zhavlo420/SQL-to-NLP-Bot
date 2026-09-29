# Agent design

The repository uses an explicit orchestrator so each stage is testable.

1. Intent Agent — classifies the question.
2. Glossary Agent — retrieves relevant business definitions and canonicalizes known synonyms.
3. Schema Agent — ranks database metadata using the question and glossary references.
4. Planner — creates an intermediate plan with the retrieved definitions.
5. SQL Generator — produces SQL using canonical business terms.
6. Reviewer — validates SQL.
7. Security Gateway — enforces read-only policy.
8. Executor — runs the approved query.
9. Result Analyst — summarizes results and suggests a chart.

The MVP glossary is a structured local JSON file with lexical retrieval; it does not require a vector database or external embedding service.

To upgrade to Deep Agents, make the orchestrator a Deep Agent and expose specialist capabilities as subagents/tools. Keep authorization and SQL execution outside the model.
