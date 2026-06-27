# SYSTEM-DESIGN MODEL ANSWER - ground truth reference

> Ground truth for the SYSTEM-DESIGN mode. Reveal this to the user ONLY at the Grade phase, after they
> have performed their own full answer. It demonstrates the structure, depth, and tradeoff reasoning a
> strong senior-level answer exhibits, against which the user's answer is compared. Calibrate the depth
> bar up (staff) or down (junior) at Frame. The canonical example below is reproduced verbatim.

---

# System Design Interview Model Answer

## Design a Large-Scale Food Ordering and Delivery Platform

### 1. Clarify and Define Requirements

Before jumping into the architecture, I would first clarify the scope.

I understand that we are designing a high-traffic food ordering and delivery platform similar to Coupang Eats or Uber Eats. The core flow is: a customer searches restaurants, places an order, pays, the restaurant accepts the order, a rider is assigned, and the customer tracks delivery status in real time.

For functional requirements, I would include:

Customers should be able to browse restaurants, view menus, place orders, pay, and track order status. Restaurants should be able to manage menus, accept or reject orders, and update preparation status. Riders should receive delivery requests, accept assignments, pick up orders, and update delivery progress. The system should also support notifications, promotions, refunds, and customer support events.

For non-functional requirements, the system should be highly available, scalable, and resilient to traffic spikes, especially during lunch, dinner, holidays, and discount events. Ordering and payment require strong correctness, while restaurant browsing and delivery tracking can tolerate eventual consistency. The system should provide low latency for browsing and tracking, but reliability is more important than ultra-low latency for order placement and payment.

I will assume an initial scale of around 1 million daily active users, with peak traffic of 10,000 to 50,000 read requests per second for restaurant browsing, and 1,000 to 5,000 order submissions per minute during peak events. Even if the interviewer gives a lower number, I would design the system so it can grow 10x.

---

### 2. High-Level Design

At a high level, I would separate the system into several services:

1. API Gateway
2. User Service
3. Restaurant Service
4. Menu Service
5. Search Service
6. Order Service
7. Payment Service
8. Dispatch/Rider Matching Service
9. Delivery Tracking Service
10. Notification Service
11. Promotion/Coupon Service
12. Event Streaming Platform
13. Data Analytics and Monitoring Platform

The client applications would be customer mobile apps, restaurant tablets or dashboards, and rider mobile apps.

Traffic first goes through a CDN and load balancer. Static assets such as images and restaurant photos are served from CDN. Dynamic requests go through the API Gateway, which handles authentication, rate limiting, request routing, and basic throttling.

For read-heavy services like restaurant browsing, menus, and search, I would use caching aggressively. Redis can cache restaurant lists, menu data, popular search results, and user session data. Search can be backed by Elasticsearch or OpenSearch because users need location-based restaurant discovery, keyword search, filtering, and ranking.

For transactional services like order and payment, I would use a relational database such as MySQL or PostgreSQL because we need ACID transactions, constraints, and strong consistency. For high scale, the order database can be partitioned or sharded by user ID, order ID, or region.

For asynchronous workflows, I would use Kafka. Order events, payment events, restaurant acceptance events, rider assignment events, and notification events can all be published to Kafka. This reduces tight coupling between services and improves resilience under traffic spikes.

A simplified architecture would look like this:

Customer App / Restaurant App / Rider App
-> CDN / Load Balancer
-> API Gateway
-> Microservices: Restaurant, Menu, Search, Order, Payment, Dispatch, Tracking, Notification
-> Redis Cache
-> MySQL/PostgreSQL for transactional data
-> Elasticsearch/OpenSearch for search
-> Kafka for event streaming
-> Object Storage for images/logs
-> Monitoring, Alerting, Analytics

---

### 3. Core Order Flow

The most important flow is order placement.

First, the customer browses restaurants and menus. These are mostly read-heavy operations, so the system serves them from Redis cache or search index where possible. If cache misses occur, the system reads from the restaurant/menu database and repopulates the cache.

Second, the customer submits an order. The Order Service validates the request: user, restaurant status, menu availability, price, coupon, address, and estimated delivery area. Then it creates an order with status `PENDING_PAYMENT`.

Third, the Payment Service processes payment. Payment should be idempotent because users may retry due to network issues. I would use an idempotency key generated by the client or server so repeated payment requests do not create duplicate charges.

Fourth, after payment succeeds, the Payment Service publishes a `PaymentSucceeded` event to Kafka. The Order Service consumes the event and updates order status to `PAID`.

Fifth, the Restaurant Service or restaurant app receives the order. If the restaurant accepts, a `RestaurantAccepted` event is published.

Sixth, the Dispatch Service tries to match a rider based on location, rider availability, distance, restaurant preparation time, and delivery SLA. Once a rider is assigned, the order status moves to `RIDER_ASSIGNED`.

Finally, the Delivery Tracking Service receives GPS updates from the rider app. Customers receive near-real-time updates through WebSocket, Server-Sent Events, or push notifications.

---

### 4. Low-Level Design and Data Model

For the Order Service, the main tables could be:

`orders`

* order_id
* user_id
* restaurant_id
* rider_id
* status
* total_price
* delivery_address_id
* created_at
* updated_at

`order_items`

* order_item_id
* order_id
* menu_item_id
* quantity
* unit_price
* options

`payments`

* payment_id
* order_id
* user_id
* amount
* payment_status
* external_payment_reference
* idempotency_key
* created_at

`delivery_tasks`

* task_id
* order_id
* rider_id
* pickup_location
* dropoff_location
* task_status
* estimated_pickup_time
* estimated_delivery_time

The order status should be modeled as a state machine:

`CREATED -> PENDING_PAYMENT -> PAID -> RESTAURANT_ACCEPTED -> RIDER_ASSIGNED -> PICKED_UP -> DELIVERED`

Failure states include:

`PAYMENT_FAILED`, `RESTAURANT_REJECTED`, `CANCELLED`, `REFUNDED`, `DELIVERY_FAILED`.

This state machine is important because distributed systems can receive duplicate, delayed, or out-of-order events. Each status transition should be validated. For example, an order should not move from `CREATED` directly to `DELIVERED`.

For Kafka topics, I would define:

* `order-created`
* `payment-succeeded`
* `payment-failed`
* `restaurant-accepted`
* `restaurant-rejected`
* `rider-assigned`
* `delivery-status-updated`
* `notification-requested`

Each event should include an event ID, order ID, timestamp, producer name, schema version, and idempotency key where needed.

---

### 5. Caching Strategy

I would use Redis for several purposes.

For restaurant and menu data, Redis can cache frequently accessed restaurants and menus. Cache TTL can be short, for example 1 to 5 minutes, because restaurant availability and menu changes are not as strict as payment data.

For user sessions and tokens, Redis can provide fast access.

For rate limiting, Redis can track request counts per user, IP, or device.

For hot restaurants or promotion events, we can pre-warm the cache before the event starts.

However, I would not use Redis as the source of truth for orders or payments. Orders and payments should be stored in a durable relational database.

---

### 6. Database and Consistency Strategy

I would use different consistency models depending on the domain.

For order creation, payment, cancellation, and refund, I would prefer strong consistency. These operations affect money and user trust.

For restaurant search, menu display, delivery tracking, and recommendation ranking, eventual consistency is acceptable. It is usually fine if a restaurant ranking or estimated delivery time is slightly stale.

The main transactional database can use replication for read scaling and failover. The primary handles writes, and replicas handle read-heavy internal queries. As traffic grows, we can shard orders by region or order ID. For example, Seoul orders and Busan orders could be partitioned separately, or order IDs could encode region and timestamp.

Indexes are important. I would index:

* `orders(user_id, created_at)`
* `orders(restaurant_id, created_at)`
* `orders(status, updated_at)`
* `delivery_tasks(rider_id, task_status)`
* `payments(order_id)`
* `payments(idempotency_key)`

---

### 7. Dispatch and Rider Matching Deep Dive

The dispatch problem is one of the most important parts of a delivery system.

The Dispatch Service needs to match orders to riders efficiently. It should consider rider location, restaurant location, customer location, rider availability, current workload, estimated preparation time, and promised delivery SLA.

For geospatial queries, I would use Redis GEO, PostGIS, or a location indexing system such as H3 or geohash. Riders continuously send location updates, but we should not write every GPS update directly to the main database because that would create too much write traffic. Instead, recent rider locations can be stored in Redis or a high-throughput location store, while important delivery milestones are persisted to the database.

The dispatch algorithm can start simple:

Find available riders within a radius, rank them by estimated pickup time, assign the best rider, and send an offer. If the rider does not accept within a timeout, retry with the next rider.

At larger scale, the algorithm can become more sophisticated by considering batching, predicted preparation time, rider fairness, delivery cost, and regional supply-demand imbalance.

---

### 8. Handling Traffic Spikes

Traffic spikes are expected during lunch, dinner, holidays, and discount campaigns.

I would handle spikes using several layers:

First, CDN and Redis reduce read pressure on backend services.

Second, the API Gateway applies rate limiting and request throttling.

Third, Kafka absorbs bursts for asynchronous processing. For example, notification sending, analytics, restaurant event logs, and some dispatch retries can be processed asynchronously.

Fourth, services should autoscale horizontally based on CPU, memory, request latency, queue lag, and error rate.

Fifth, we can degrade non-critical features. For example, if the system is under heavy load, we can temporarily disable personalized recommendations, reduce tracking update frequency, or simplify restaurant ranking.

The key principle is that core ordering and payment must remain stable, while non-critical features can be degraded.

---

### 9. Failure Handling

There are several important failure scenarios.

If Payment Service succeeds but Order Service fails to update the order, Kafka retry and reconciliation jobs should eventually fix the order status. We should also have a periodic job that compares payment provider records with internal payment records.

If the restaurant does not respond, the order can be automatically cancelled after a timeout and the customer can be refunded.

If rider assignment fails, the Dispatch Service can retry with a wider radius or escalate to manual operations.

If Kafka is delayed, the system should expose intermediate states clearly to the user, such as "Payment completed, waiting for restaurant confirmation."

If Redis goes down, the system should fall back to the database, but with rate limiting to protect the database from overload.

If a database primary fails, replicas and automated failover should be used. For critical systems, multi-AZ deployment is necessary.

---

### 10. Trade-Off Analysis

For consistency versus availability, I would choose strong consistency for payment, order state, cancellation, and refund. For search, restaurant ranking, menu cache, and delivery tracking, I would accept eventual consistency to improve availability and performance.

For latency versus reliability, I would make browsing and search low-latency through caching and search indexing. For order placement, I would accept slightly higher latency to guarantee correctness, idempotency, and reliable payment handling.

For cost versus performance, I would cache only hot and frequently accessed data. Caching everything is expensive and unnecessary. I would also separate read-heavy services from write-heavy services so each can scale independently.

For monolith versus microservices, I would not start with too many services if the product is small. But for a Coupang-scale platform, separating Order, Payment, Dispatch, Restaurant, Search, and Notification makes sense because they have different scaling patterns and failure boundaries.

---

### 11. Bottlenecks and Mitigation

The first bottleneck is the database for orders and payments. I would mitigate this with proper indexing, read replicas, sharding, and keeping transactions short.

The second bottleneck is restaurant/menu browsing during peak times. I would mitigate this with CDN, Redis caching, cache pre-warming, and search index optimization.

The third bottleneck is dispatch matching. I would mitigate this with geospatial indexing, regional partitioning, and asynchronous matching workflows.

The fourth bottleneck is notification fan-out. I would handle this asynchronously using Kafka and worker pools.

The fifth bottleneck is external payment provider latency or failure. I would use timeouts, retries with backoff, idempotency keys, and reconciliation jobs.

---

### 12. Observability and Operations

For production operation, I would monitor:

* API latency: p50, p95, p99
* Error rate by service
* Order success rate
* Payment success and failure rate
* Kafka consumer lag
* Dispatch assignment latency
* Delivery SLA violations
* Database CPU, slow queries, lock waits
* Redis hit rate and memory usage
* External payment provider latency

I would also add distributed tracing so that one order can be traced across API Gateway, Order Service, Payment Service, Kafka, Dispatch Service, and Notification Service.

For incident response, I would prepare dashboards, alerts, runbooks, and feature flags. Feature flags are useful because we can quickly disable non-critical features during incidents.

---

### 13. Final Summary

My design separates read-heavy services from transaction-critical services. Restaurant browsing and menus are optimized with CDN, Redis, and search indexing. Orders and payments use a relational database with strong consistency and idempotency. Kafka decouples services and absorbs traffic spikes. Dispatch uses geospatial indexing and asynchronous matching. The system is designed to degrade gracefully under load while protecting the most important user flow: successful order placement and delivery.

The main trade-off is that I prioritize correctness and reliability for order/payment workflows, while accepting eventual consistency for search, tracking, recommendations, and notifications. This allows the platform to scale while maintaining user trust.
