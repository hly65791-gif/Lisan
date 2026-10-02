# Architecture

Lisan uses a modular Clean Architecture style.

app
 -> feature modules
 -> domain
 -> data
 -> core-common/core-ui

Domain owns business models and provider/repository contracts.
Data owns Room and implementations.
UI observes state from ViewModels.

Long-running video work is represented as a persistent WorkManager job.
External AI/media systems must be accessed through provider/service interfaces.
