# Python Lab

> A hands-on lab for anyone who wants to go from writing their first line of Python to building production-grade systems. No prior programming experience required. By Phase 11 you will have built a full data pipeline with automated reporting, tests, async I/O, and a REST API — using nothing but Python and the standard library (plus a few well-chosen packages).

---

## Who this is for

Complete beginners, developers switching from another language, and engineers who "know enough Python to get by" but want to fill the gaps. Each phase builds directly on the previous one. You will learn by writing real code for a real problem — not toy examples.

---

## The scenario

**Meridian** — a fast-growing e-commerce company — sells outdoor gear across three warehouses and a web store. They have 12,000 SKUs, 2,400 orders per day, and a small ops team running everything on spreadsheets and gut feeling.

The problem: their inventory goes out of sync. Orders ship late. Refund requests pile up. Their biggest wholesale partner just sent a notice: *"If your fill-rate drops below 95% again this quarter, we are pulling the contract."*

The ops manager made the call: automate it with Python. Not a quick script that breaks on Monday. A real system that reads orders, tracks inventory, flags problems, generates reports, and exposes an API for their order management tool.

You are the engineer who has to build it.

---

## What you will build, phase by phase

```
Phase 0  → Setup & First Script      — installing Python, running code, print, variables, types
Phase 1  → Core Python               — control flow, loops, functions, scope
Phase 2  → Data Structures           — lists, dicts, sets, tuples, comprehensions
Phase 3  → Files & Exceptions        — reading/writing files, CSV, JSON, error handling
Phase 4  → Functions In Depth        — args/kwargs, closures, decorators, lambdas
Phase 5  → Object-Oriented Python    — classes, inheritance, dunder methods, dataclasses
Phase 6  → The Standard Library      — pathlib, datetime, collections, itertools, re
Phase 7  → Testing                   — unittest, pytest, fixtures, mocks, TDD workflow
Phase 8  → Performance               — profiling, generators, slots, caching, big-O awareness
Phase 9  → Concurrency               — threading, multiprocessing, asyncio, httpx
Phase 10 → Packaging & APIs          — virtual envs, pyproject.toml, FastAPI, deployment basics
Phase 11 → Capstone                  — full Meridian pipeline, production-ready
```

---

## Lab structure

| Phase | Title | Key concepts |
|---|---|---|
| 0 | Setup & First Script | Installation, REPL, scripts, variables, types, print, input |
| 1 | Core Python | if/elif/else, for/while, functions, return, scope, None |
| 2 | Data Structures | list, dict, set, tuple, list/dict comprehensions, unpacking |
| 3 | Files & Exceptions | open(), csv, json, try/except/finally, custom exceptions |
| 4 | Functions In Depth | *args, **kwargs, closures, decorators, functools |
| 5 | Object-Oriented Python | class, __init__, inheritance, @property, dataclasses |
| 6 | The Standard Library | pathlib, datetime, collections, itertools, re, logging |
| 7 | Testing | unittest, pytest, parametrize, monkeypatch, coverage |
| 8 | Performance | cProfile, generators, __slots__, lru_cache, algorithmic cost |
| 9 | Concurrency | threading, multiprocessing, asyncio, httpx async client |
| 10 | Packaging & APIs | venv, pyproject.toml, FastAPI, Pydantic, uvicorn |
| 11 | Capstone | Full Meridian pipeline end-to-end, tested, packaged, deployed |

---

## The Meridian data model

The system you will build automation for:

```
orders/
├── order_id: string           # e.g. "ORD-00142"
├── sku: string                # e.g. "TENT-3P-GRN"
├── quantity: int
├── warehouse: string          # "north" | "south" | "west"
├── status: string             # "pending" | "shipped" | "cancelled"
└── created_at: string         # ISO 8601

inventory/
├── sku: string
├── warehouse: string
├── stock: int
└── reorder_threshold: int

products/
├── sku: string
├── name: string
├── category: string           # "tent" | "sleeping_bag" | "pack" | "apparel"
└── unit_price: float
```

By Phase 3 you will be reading and writing these as CSV and JSON files. By Phase 5 they become Python classes. By Phase 11 they are stored, queried, and served via a REST API.

---

## Prerequisites

A computer. That's it. Phase 0 walks you through installing Python.

```bash
# After Phase 0 setup:
python3 --version   # should print Python 3.11 or higher
```

---

## Getting started

```bash
git clone <this-repo>
cd python-lab
# Start with Phase 0
cd phase-0-setup
```

No package installation needed for Phase 0 — it uses only the Python standard library.

---

## Cost

This lab is free. It uses no external APIs until optional Phase 9 exercises. All exercises run locally.

---

[AI Engineering Lab →](../ai-engineering-lab) | [DevOps Labs →](../)
