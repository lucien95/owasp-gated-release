# Chapter 1: Meet the vulnerable app

> **Status:** In progress
> **Time:** about 6 hours · **Cost:** $0 · **You will need:** the Chapter 0 cluster (`make up`), Python 3.12, Docker

## Goal

By the end of this chapter, an expense-claims API is running in your cluster, you have broken it ten different ways by hand (one for each OWASP Top 10:2025 category), and a basic pipeline still gives it a green tick.

## Why this matters

You cannot judge a security gate until you have seen the attack it is meant to stop. This chapter is the "before" picture for everything that follows. Its most important lesson is uncomfortable: **a green pipeline does not mean a secure application.**

## Concepts first

*Written as each step is built.*

## The application

An expense-claims API ([ADR-0005](../adr/0005-expense-claims-api-as-the-workload.md)). Three seeded users with synthetic data:

| User | Role | Should be able to |
| --- | --- | --- |
| `alice` | employee | Submit claims and see only her own |
| `bob` | manager | Approve or reject his team's claims, but never his own |
| `carol` | finance | See approved claims and mark them paid |

| Method and path | What it does |
| --- | --- |
| `POST /auth/login` | Username and password → access token |
| `POST /claims` | Submit a claim |
| `GET /claims` | List claims, with `?search=` |
| `GET /claims/{id}` | View one claim |
| `POST /claims/{id}/approve` | Manager approves a claim |
| `POST /claims/{id}/pay` | Finance marks a claim paid |
| `POST /claims/import` | Bulk-import claims from a file |
| `GET /health` | Liveness check for Kubernetes |

## Steps

1. Create the application skeleton and run it locally (*planned*)
2. Add the database, users, and claims (*planned*)
3. Add the endpoints, including the planted flaws (*planned*)
4. Package it as a container and run it in the cluster (*planned*)
5. Attack it by hand: ten OWASP categories (*planned*)
6. Add a basic pipeline that stays green anyway (*planned*)
7. Start `VULNERABILITIES.md` (*planned*)

## What broke

*Recorded as it happens.*
