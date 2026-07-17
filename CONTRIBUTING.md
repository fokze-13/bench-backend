# Contributing to Bench

First off — thank you for being here. Bench is an early, unfinished project, and that's exactly why your input matters. The concept isn't fully baked yet, so this isn't just about fixing bugs. Ideas, questions, and honest criticism are as welcome as code.

If you're reading this, you already care enough to help. That's the hard part.

## Ways to contribute

You don't have to write code to make this better:

- **Shape the direction.** The idea is still forming. If you have thoughts on where Bench should go, open a discussion or an issue — that kind of input is genuinely valuable right now.
- **Report bugs.** Found something broken? Tell us what happened, what you expected, and how to reproduce it.
- **Suggest features.** Have an idea for a feature or a change? Describe the problem it solves, not just the solution.
- **Improve the docs.** If something in the README or here was confusing, that's a bug too.
- **Write code.** Fixes, features, cleanups — all welcome.

## Before you start

A few things worth knowing:

- **This is the backend.** It's built with FastAPI, PostgreSQL, and Redis, all packaged in Docker. The [README](./README.md) walks through the stack and how to run it.
- **Anonymity is the point.** Bench is built so that no personal data is ever collected or stored — no email, no username, no password, no message history. Any contribution has to respect that. If a change would weaken anonymity or start retaining user data, it doesn't fit the project, no matter how useful it is otherwise.
- **When in doubt, ask first.** For anything larger than a small fix, open an issue before writing a lot of code. It saves everyone time and avoids work that can't be merged.

## Getting set up

Everything runs in Docker, so setup is short:

```bash
git clone <your-fork-url>
cd bench-backend
cp .env.example .env      # fill in your secrets
docker compose up --build
```

That brings up the app, database, Redis, and proxy, and runs migrations automatically. See the [README](./README.md) for the full breakdown of what each container does.

## Making changes

1. **Fork** the repository and create a branch off the main development branch. Give it a short, descriptive name (for example, `fix/room-cleanup` or `feature/alias-generator`).
2. **Make your change.** Keep it focused — one logical change per pull request is much easier to review than a large mixed one.
3. **Match the surrounding code.** Follow the style, naming, and structure already in the codebase so your change reads like it belongs.
4. **Test it.** Make sure the project still runs and existing tests pass. If you're adding behavior, add a test for it where it makes sense.
5. **Write a clear commit message.** Say what changed and why, not just what.

## Opening a pull request

When your change is ready:

- Open a pull request against the main development branch.
- Describe **what** you changed and **why**. If it fixes an issue, link it.
- If it's a work in progress and you want early feedback, say so — that's fine.
- Be ready for a bit of back and forth. Review is a conversation, not a gate.

## Reporting bugs and requesting features

Open an issue and include enough for someone else to understand it:

- **For bugs:** what you did, what you expected, what actually happened, and steps to reproduce.
- **For features:** the problem you're trying to solve and, if you have one, a rough idea of the solution.

Clear, small, specific issues get looked at faster than large vague ones.

## Code of conduct

This is a small, open project, and the expectation is simple: be decent to each other.

- Be respectful and constructive, especially when disagreeing.
- Critique ideas and code, not people.
- Assume good faith. Most misunderstandings are just that.
- Harassment, personal attacks, and hostility have no place here.

If you run into behavior that crosses a line, or you're unsure about something, reach out directly — contact details are below.

## Contact

This is a one-developer project, so the fastest way to reach me is directly:

- **Email:** abdurahmon.bahramov2.0@gmail.com
- **Telegram:** [@hudp72](https://t.me/hudp72)
- **Issues and discussions:** [link](https://github.com/fokze-13/bench-backend/issues)

Whether it's a bug, an idea, or just a conversation about where Bench should go — I'd be glad to hear from you.