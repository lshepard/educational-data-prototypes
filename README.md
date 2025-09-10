# Prototype System Overview

## Goals

We want to enable **rapid prototyping of educational products** in a school-based environment, while ensuring fundamental **data security** and **compliance**.  
This system is designed to:

- Accelerate **front-end and dynamic app prototyping** using AI and LLMs (e.g., Lovable, Vercel, Claude Code, etc.).  
- Provide engaging experiences for both **teachers and students**.  
- Ensure **FERPA-compliant handling of student information**.  
- Reduce repeated integration work by offering a **single, consistent data setup** for all prototypes.

---

## Core Principles

1. **One-time integrations**  
   - If a school site uses a given SIS or LMS, we integrate once (likely via **Edlink** or similar).  
   - That data flows into a single, secure service layer.  
   - Each prototype can then securely reuse this data without new integrations.

2. **Long-lived secure service**  
   - Provides the **underlying data layer** (schools, classes, students, and related records).  
   - Includes a **skeleton CRUD app** to browse and manage data.  
   - Handles **authentication/authorization**.  
     - Initially via **Supabase Auth**.  
     - Later can expand to support SSO (Google, Microsoft, etc.).

3. **Independent prototype systems**  
   - Each prototype (a classroom assistant, grading dashboard, interactive tool, etc.) can be built however teams prefer:
     - Vibe-coded with **Vercel**.  
     - Stood up as a standalone service on **Railway**.  
     - Generated with **Claude Code** or similar tools.  
   - All prototypes consume the **same secure backend**.

---

## Proposed Architecture

### Long-Lived Secure Service
- Stable service exposing a clean API (REST/OpenAPI).  
- Enforces **data access policies** (row-level security, per-user scoping).  
- Stores canonical school/class/student data.  
- Provides an **admin CRUD UI** for safe inspection and management.  
- Central point of integration with SIS/LMS.  

### Prototype Applications
- Built independently, focusing on user experience and rapid iteration.  
- Call the secure service for data and auth, **never directly handle raw SIS/LMS credentials**.  
- Sandbox and production separation enforced.  

---

## Demonstration System

The demonstration system will consist of **three components**:

1. **Standalone Secure Service**  
   - Represents the long-lived backend.  
   - Provides mock school/class/student data.  
   - Exposes APIs and CRUD UI.  
   - Authentication via Supabase.
   - Written in Python (could just as easily be Nest as well)

2. **Vibe-coded App 1 (Vercel)**  
   - A front-end prototype (e.g., audio chatbot using Vercel AI SDK).
   - Uses the secure service API for roster/class data.

3. **Vibe-coded App 2 (Lovable)**  
   - Another prototype UI (e.g., dashboard or student experience).  
   - Also integrates with the secure service API.  

---

## Future Directions

- Add **Edlink integration** for real SIS/LMS data.  
- Expand **SSO options** for school partners.  
- Provide a library/SDK to simplify connecting new prototypes.  
- Add auditing, rate-limits, and monitoring for production readiness.  

---

## Summary

This system separates **stable, secure data services** from **fast, flexible prototyping**.  
By doing so, we can support school partners with real integrations, while still allowing creative teams to experiment rapidly and safely.
