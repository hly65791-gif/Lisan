# Lisan v0.38 — Home Recent Projects

The home screen now observes `ProjectRepository.observeProjects()` through `HomeViewModel` and renders up to three real, most-recent projects from Room.

Behavior:
- Empty state opens the video picker.
- Recent cards show project name, source/target languages, status, and progress for active jobs.
- The list remains ordered by `updatedAt DESC` from the Room DAO.
- Tapping a card opens the Projects screen for the full project list.

No fake sample projects are rendered by the home screen.
