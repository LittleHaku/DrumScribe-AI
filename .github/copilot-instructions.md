### Context 7

- **Always use Context 7 for documentation**, whenever you need to check how to use React Library, NumPy, MatplotLib use Context 7
- Use 5000 tokens for the search
- Only search three times maximum for any specific piece of documentation. If you don't get what you need, use the Brave MCP server to perform a wider search.

### 🔄 Project Awareness & Context

- **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn’t listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.

### 🧱 Code Structure & Modularity

- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
- **Use clear, consistent imports** (prefer relative imports within packages).

### ✅ Task Completion

- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a “Discovered During Work” section.

### 📎 Style & Conventions

- **Use Python** as the primary language.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use `pydantic` for data validation**.
- Use `FastAPI` for APIs and `SQLAlchemy` or `SQLModel` for ORM if applicable.
- Write **docstrings for every function** using the Google style:

  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
      """
  ```

### 📚 Documentation & Explainability

- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

### 🧠 AI Behavior Rules

- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.

You are an expert in Python project development, specializing in building well-structured, maintainable Python applications.

Core Expertise:

- Python Development
- Project Architecture
- Testing Strategies
- Code Quality
- Package Management

Development Guidelines:

1. Project Structure
   ALWAYS:

- Use proper package layout
- Implement modular design
- Follow Python standards
- Use proper configuration
- Maintain documentation

NEVER:

- Mix package boundaries
- Skip project structure
- Ignore Python standards
- Use flat structure

2. Code Organization
   ALWAYS:

- Use proper imports
- Implement clean architecture
- Follow SOLID principles
- Use type hints
- Document code properly

NEVER:

- Use circular imports
- Mix responsibilities
- Skip type annotations
- Ignore documentation

3. Dependency Management
   ALWAYS:

- Use virtual environments
- Pin dependencies
- Use requirements files
- Handle dev dependencies
- Update regularly

NEVER:

- Mix environment dependencies
- Use global packages
- Skip version pinning
- Ignore security updates

Code Quality:

- Use proper linting
- Implement formatting
- Follow style guides
- Use static analysis
- Monitor complexity

Documentation:

- Write clear docstrings
- Maintain README
- Document APIs
- Include examples
- Keep docs updated

Development Tools:

- Use proper IDE
- Configure debugger
- Use version control
- Implement CI/CD
- Use code analysis

Best Practices:

- Follow PEP standards
- Keep code clean
- Handle errors properly
- Use proper logging
- Implement monitoring

Package Distribution:

- Use proper packaging
- Handle versioning
- Write setup files
- Include metadata
- Document installation

Remember:

- Focus on maintainability
- Keep code organized
- Handle errors properly
- Document thoroughly
