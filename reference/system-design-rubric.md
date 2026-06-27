# SYSTEM-DESIGN RUBRIC - 10-dimension grading + probing bank

The scoring standard for the SYSTEM-DESIGN mode. The 10 dimensions mirror the canonical structure a
strong answer walks (`reference/system-design-model-answer.md`). Score each dimension 0-2 against the
target level bar set at Frame, then name the FIRST gap with a concrete fix. The rubric grades
*structure and depth*, not whether the candidate's tech choices match the model answer verbatim -
many valid designs exist.

## Scoring scale (per dimension)

| Score | Meaning |
|---|---|
| 0 | Missing or wrong-direction |
| 1 | Present but thin / hand-wavy |
| 2 | Solid, with explicit reasoning |

Report the total `/20` plus the level bar. Calibrate the "2" bar to the target:

- **Junior/mid:** a 2 needs correct structure and a defensible choice; back-of-envelope can be rough.
- **Senior:** a 2 needs explicit tradeoff reasoning and a failure path per critical component.
- **Staff/Principal:** a 2 needs ambiguity navigation, original constraints, and cross-system reasoning
  (e.g. how a choice here forces a constraint elsewhere).

## The 10 dimensions

1. **Requirements clarification** - Did they separate functional from non-functional, state assumptions
   explicitly, and back-of-envelope the scale (DAU, read/write QPS, storage, bandwidth)? Did they ask
   clarifying questions before designing, or jump straight to boxes?
2. **High-level architecture** - Components named, responsibilities assigned, data flow drawn. CDN,
   load balancer, API gateway, services, caches, DBs, async bus all placed with a reason. Is the
   read-path vs write-path split explicit?
3. **Core flow / API design** - The happy path walked end to end (browse -> order -> pay -> accept ->
   dispatch -> deliver). Key APIs or endpoints sketched. Did they own the flow rather than wait to be
   pulled through it?
4. **Data model & schema** - Core tables with fields and relationships; the right DB type per domain
   (relational for transactional, search index for discovery). Did they model the STATE MACHINE and
   validate transitions?
5. **Deep dive** - The interviewer-chosen focus area (e.g. dispatch matching, a hot component) taken
   to real depth, not a surface repeat. This is where senior vs junior separates.
6. **Scalability & bottlenecks** - Top bottlenecks named with concrete mitigation: sharding key,
   read replicas, cache strategy, async absorption. Did they separate read-heavy from write-heavy?
7. **Consistency & reliability** - Strong vs eventual consistency chosen PER DOMAIN with a reason.
   Idempotency, retries, reconciliation, out-of-order/duplicate event handling. Failure paths for
   each critical component. This is the most commonly thinned dimension - probe it.
8. **Trade-offs** - Explicit C-vs-A, latency-vs-reliability, cost-vs-performance reasoning. Not "we
   use Kafka" but "Kafka absorbs bursts and decouples X from Y at the cost of eventual delivery."
9. **Observability** - Metrics that matter (p50/p95/p99, error rate, consumer lag, SLA violations),
   distributed tracing across services, alerting, feature flags for graceful degradation.
10. **Communication & structure** - Drove the interview, organized clearly, managed time, drew/typed
    the picture, checked in with the interviewer. A candidate who waits to be dragged scores low here.

## Grade output format

```
SYSTEM-DESIGN grade  -  <total>/20  (bar: <level>)
1 Requirements clarification      <0-2>  <one-line evidence>
2 High-level architecture         <0-2>  <evidence>
3 Core flow / API design          <0-2>  <evidence>
4 Data model & schema             <0-2>  <evidence>
5 Deep dive                       <0-2>  <evidence>
6 Scalability & bottlenecks       <0-2>  <evidence>
7 Consistency & reliability       <0-2>  <evidence>
8 Trade-offs                      <0-2>  <evidence>
9 Observability                   <0-2>  <evidence>
10 Communication & structure      <0-2>  <evidence>

FIRST gap: <dimension> - <what was thin> -> <concrete one-line fix>
Re-drill target: <dimension> with a novel variant: <the new question/constraint>
```

Then reveal `reference/system-design-model-answer.md` for self-comparison.

## Probing-question bank (Pose + Probe)

Pick 1-3 that target the answer's WEAKEST dimension. Never probe to confirm what was already strong.

**Requirements / scale**
- What is your read QPS vs write QPS assumption? Storage growth per year?
- Which feature is out of scope for v1? What did you deprioritize and why?

**Architecture**
- Walk me through a single order request hop by hop through your boxes.
- Where does the read path and write path split? Why there?

**Data model / consistency (probe hard - most thinned)**
- What happens if payment succeeds but the order service crashes before updating status?
- How do you prevent a double-charge on retry? Where does the idempotency key live?
- Your order status is a state machine - can an order go CREATED -> DELIVERED? Why must transitions validate?
- Two duplicate delivery-status events arrive out of order. What breaks?

**Scalability / bottlenecks**
- What is your single biggest bottleneck at 10x current scale? How do you shard past it?
- You cache restaurant data - what is your invalidation strategy? Cache stampede?
- Every rider sends GPS every second. Where does that write load go?

**Dispatch deep dive**
- How do you spatially index riders? Why that structure over another?
- No rider accepts within timeout. What is the escalation?

**Failure / degradation**
- Kafka is 30 seconds delayed. What does the customer see?
- Redis is down. What protects your database?
- Database primary fails mid-payment. Walk me through recovery.

**Trade-offs**
- You chose eventual consistency for search. What is the worst-case user-visible staleness?
- Why microservices here and not a well-modularized monolith? What is the cost you accepted?

## What a "2" looks like by level (consistency dimension, worked example)

- **Junior:** "Payments need to be consistent, so I'd use a transaction." (present, thin)
- **Senior:** "Payments are strong-consistency via ACID + an idempotency key to survive client retries;
  the PaymentSucceeded event lets Order reconcile if its own write fails, with a reconciliation job
  comparing provider records nightly." (explicit reasoning + failure path)
- **Staff:** "I partition consistency by sub-domain: payment+order-state strong, search/ranking eventual.
  The boundary is the PaymentSucceeded event - I accept at-most-once processing there and reconcile
  via the provider's webhook as the authoritative source, which also constrains the refund flow." (the
  choice and the constraint it imposes on another system are both named)
