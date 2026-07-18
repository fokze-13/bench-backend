<div align="center">
  <img width="200" height="200" src="./docs/assets/logo.svg" alt="Bench Logo" />
</div>

# Bench — Backend

### The anonymous group chat app

> **This is the backend part of the project.**
> Frontend: [link](https://github.com/fokze-13/bench-frontend.git)

Built with **FastAPI + PostgreSQL + Redis**, fully packaged in **Docker** so the whole thing spins up with a single command

---

## A look at the app

<div align="center">

| Home | Chat room | Settings |
|:---:|:---:|:---:|
| <img src="./docs/assets/Simulator%20Screenshot%20-%20iPhone%2017%20Pro%20Max%20-%202026-07-18%20at%2000.04.22.png" width="230" alt="Home screen" /> | <img src="./docs/assets/Simulator%20Screenshot%20-%20iPhone%2017%20Pro%20Max%20-%202026-07-18%20at%2000.15.36.png" width="230" alt="Chat room" /> | <img src="./docs/assets/Simulator%20Screenshot%20-%20iPhone%2017%20Pro%20Max%20-%202026-07-18%20at%2000.04.56.png" width="230" alt="Settings" /> |

| About | Languages |
|:---:|:---:|
| <img src="./docs/assets/Simulator%20Screenshot%20-%20iPhone%2017%20Pro%20Max%20-%202026-07-18%20at%2000.05.03.png" width="230" alt="About the app" /> | <img src="./docs/assets/Simulator%20Screenshot%20-%20iPhone%2017%20Pro%20Max%20-%202026-07-18%20at%2000.04.47.png" width="230" alt="Language selection" /> |

</div>

> These shots are from the mobile client. Note that the **frontend lives in a separate repository** — this repo is the backend.

---

## The idea

Bench is a place to talk to strangers with nothing attached to your name — because there is no name. Instead of one giant public feed, conversations happen in small rooms of **5–6 people**. Everyone shows up under a random alias, so the people around you are real, but nobody knows who anybody is.

The whole thing is built around anonymity as a hard rule, not a setting:

- **Nothing personal is ever asked.** No email, no username, no password, no phone number. Authorization runs entirely on **JWT tokens**, so you get an identity for a session without ever handing over anything that ties back to you.
- **Message history isn't stored.** Conversations live only for as long as they're happening. When a room is done, so are its messages — there's no archive to leak, subpoena, or scrape.
- **Everyone is an alias.** Other people in the room appear under generated names, so the anonymity goes both ways.

The point is simple: freedom of speech and expression, tried out in the small, human-scale setting of a handful of people in a room together.

## Where this is headed

Honestly, the concept isn't fully baked yet. Right now Bench is more of a **tool** than a finished product — there's no grand roadmap or fixed goal behind it, just the motivation to build something that lets people express their thoughts without fear that their anonymity will crack. And since it's **fully open-source**, that promise isn't something you have to take on faith — you can read exactly how it works.

If the idea resonates with you, I'd genuinely love to hear it. Suggestions, criticism, feature ideas, or just a conversation about where this could go — all of it is welcome. This is the kind of project that gets better with more people thinking about it.

## Tech stack

- **FastAPI** — async Python web framework, with WebSockets for real-time chat
- **PostgreSQL** — primary datastore (SQLAlchemy 2.0 async + Alembic migrations)
- **Redis** — sessions, ephemeral state, and fast in-memory coordination
- **Gunicorn + Uvicorn workers** — production ASGI serving
- **Nginx** — reverse proxy and TLS termination (Let's Encrypt / Certbot)
- **Docker + Docker Compose** — the whole system, reproducible anywhere

## Running it

Everything is containerized, so setup is short:

```bash
cp .env.example .env      # fill in your secrets
docker compose up --build
```

That's it. Compose brings up every piece, waits for dependencies to be healthy, and runs database migrations automatically.

### How it's built and run

**Build stage.** The image uses a **multi-stage Dockerfile** to keep the final image small and clean:

1. **`deps` stage** — installs Poetry and resolves all dependencies into an isolated virtualenv. Nothing here but the build toolchain and the packages.
2. **`runtime` stage** — starts from a fresh `python:3.14-slim`, copies over only the built virtualenv and application code, and runs as a **non-root `app` user**. No compilers, no Poetry, no cruft in the shipped image.

The container exposes a `/v1/health` endpoint that Docker uses for **healthchecks**, so orchestration knows when the app is actually ready — not just started.

**Runtime stage.** `docker compose up` orchestrates five containers on a private internal network:

| Container | Image | Role |
|-----------|-------|------|
| **app** | built from `Dockerfile` (`runtime`) | FastAPI application served by Gunicorn/Uvicorn |
| **db** | `postgres:16-alpine` | PostgreSQL, data persisted in a named volume |
| **redis** | `redis:7-alpine` | Redis with password auth, AOF persistence, and an LRU memory cap |
| **nginx** | `nginx:1.27-alpine` | Reverse proxy + TLS, the only service exposed to the outside |
| **migrate** | built from `Dockerfile` (`runtime`) | One-shot job that runs `alembic upgrade head`, then exits |

A few deliberate choices worth calling out:

- **Startup ordering is enforced.** The app waits for Postgres and Redis to report **healthy** — not merely running — before it boots, so there are no race conditions on a cold start.
- **Only Nginx is public.** The app, database, and Redis all sit on an internal bridge network and are never exposed directly; everything reaches the outside world through the proxy.
- **Migrations are their own container.** Schema changes run as a dedicated, disposable `migrate` service instead of being baked into app startup, keeping deploys predictable.
- **Redis is bounded on purpose.** A hard `maxmemory` limit with an `allkeys-lru` policy fits the ephemeral, no-history design — old state is meant to fall away.
- **Resource limits and log rotation** are set per-service, so a single container can't run away with the host's memory or disk.

## Contributing

Bench is early and unfinished on purpose — which means there's real room to shape it. Bug reports, feature ideas, code, or just thoughts on where the project should go are all welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to get started.

## Contact

Built by one developer — reach out anytime:

- **Email:** abdurahmon.bahramov2.0@gmail.com
- **Telegram:** [@hudp72](https://t.me/hudp72)

## License

See [LICENSE](./LICENSE).
