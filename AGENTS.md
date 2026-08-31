# AGENTS.md

- Treat `.agents/` as private project memory for important decisions, plans, and progress tracking. Keep it ignored by Git, consult it before significant work, and update it when project direction or progress changes.
- Do not preserve backward compatibility. Remove obsolete paths instead of adding compatibility layers, fallbacks, or migrations.
- Choose the simplest implementation that fully meets the current requirements. Avoid speculative abstractions, configuration, and indirection.
- Grow the system in layers. Start from the smallest version that works end to end, and add each new capability on top of a product that already works. Never trade a working product for unfinished complexity.
- Keep components modular and concerns clearly separated.
- Prefer established, well-maintained libraries when they reduce overall complexity or improve reliability. Do not reimplement common functionality without a clear reason.
- Lean on the dependencies already in the project before writing your own implementation or adding packages. Do not assume a library lacks a capability without checking its documentation and types.
- Make architectural decisions for the long term. Do not accept a stopgap that only works for now and is meant to be replaced later.
- Study how established products solve the problem before designing a solution. Adopt their proven patterns and conventions rather than inventing an approach from scratch.
- Begin each human-authored source file with a concise two- or three-line introduction explaining what the file owns and why it exists. Use the format's normal documentation style, and do not add invalid comments to machine-readable files such as JSON.
- Give every function or method a concise docstring or documentation comment that explains its purpose or contract. Prefer comments that explain why the code exists; do not narrate obvious individual statements.
- Create a function only when it represents a meaningful, cohesive task, boundary, callback, or reusable operation. Prefer a readable block in its natural caller over many tiny helpers that merely rename a few lines.
- Keep functions large enough to complete one clear task and small enough to understand as a unit. Split a function when it mixes responsibilities, not merely because it has reached an arbitrary line count.
