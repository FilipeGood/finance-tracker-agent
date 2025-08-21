## Context

This project is a personal finance tracker agent built with LangChain and OpenAI GPT models that can track expenses, analyze spending patterns, and provide financial insights through natural language interactions. The codebase is functionally complete with both terminal and Telegram bot interfaces, but requires production cleanup to remove code duplication, fix compatibility issues, and standardize error handling patterns.

**Current State**: Two separate main entry points (`main_terminal_interaction.py` and `main_tg_interaction.py`) with duplicate functionality, timezone compatibility issues in the Telegram bot, unused imports, and development artifacts that need cleanup before production deployment.

**Task**: Perform final production cleanup focusing on consolidating duplicate functionality, fixing bugs, removing development artifacts, and standardizing error handling - all while keeping changes simple and avoiding creation of multiple new files.

## Implementation Steps

### Step 1: Create Shared Interface Module
- Create `src/interface_handler.py` to handle common functionality between terminal and telegram interfaces
- Move shared error handling, response formatting, and agent interaction logic from both main files
- Implement common methods: `handle_agent_response()`, `format_error_response()`, `validate_environment()`
- Keep entry points separate but delegate core functionality to shared handler

### Step 2: Fix and Standardize Main Files
- Fix timezone/pytz compatibility issues in `main_tg_interaction.py` by updating ApplicationBuilder usage
- Remove unused imports (`pytz`, `re`) from telegram module
- Standardize environment variable handling across both main files using shared validation
- Remove code duplication by delegating to shared interface handler
- Ensure consistent error handling and logging patterns

### Step 3: Clean Up Codebase Structure
- Remove `notebooks/` directory and `__pycache__/` directories from repository
- Update `.gitignore` to prevent future development artifact commits
- Remove unused imports and dead code from all modules
- Consolidate similar utility functions within existing modules
- Standardize docstring and typing patterns across codebase

### Step 4: Production Configuration and Documentation
- Update `Pipfile` to remove development-only dependencies
- Create production-ready environment variable documentation
- Add proper error logging instead of print statements
- Update README.md with clear production deployment instructions
- Verify all functionality works correctly with cleaned codebase

## References

- LangChain Agent Documentation: https://python.langchain.com/docs/tutorials/agents
- Python Telegram Bot API: https://python-telegram-bot.readthedocs.io/
- Python Environment Management: https://pipenv.pypa.io/en/latest/
