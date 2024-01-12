# Introduce Notification Event

In [Inter-module communication ADR](./07-inter-module-communication.md) the concepts of domain and Integration Events 
were introduced. At the moment of writing the mentioned ADR it was believed that those two types of events are
sufficient. During implementation of inter-module communication it turned out that there is a need for a third type.

## Problem

As modules use separate database transactions, the problem of exactly once processing of events needs to be 
addressed. Outbox and Inbox patterns are commonly used to solve this problem and they are used in this project as 
well. However, with the current implementation of inter-module communication, the following scenario is possible:

1. Module A publishes an event
2. The event is stored in Module A's Outbox
3. Module B attempts to store the event in its Inbox but fails

A simple solution in case of such a failure is to retry the operation. However, this is impossible to do as both 
Module A and Module B handlers may subscribe to the same event. Simply re-publishing the event would result in
duplicate processing of the event by Module A.

## Solution

The solution to the problem is to introduce a third type of event - Notification Event. The Notification Event is
kind of a wrapper around the Domain Event. It informs modules that the Domain Event was published and that
they should process it in a separate transaction. It may be used both by the module that publishes the originating 
Domain Event and by others.

### Impact on Integration Events

At the moment of writing this ADR Integration Events are not implemented yet. Their role is to enable communication 
between different bounded contexts, in separate transactions. That makes them very similar to Notification Events. 
When implementing Integration Events, the code created for handling Notification Events should be reused.

### Implementation details

The Notification Event can be implemented as a separate class that literally wraps the Domain Event.

```mermaid
---
title: subscribing to Notification Event
---
sequenceDiagram
    Module A ->> Event Bus: Subscribe to Notification Event<br>originating from DomainEventA
    Module B ->> Event Bus: Subscribe to Notification Event<br>originating from DomainEventA
```

```mermaid
---
title: Storing Domain Event in outbox
---
sequenceDiagram
    Module A ->> Event Bus: Publish Domain Event
    Event Bus ->> Module A: Trigger "Store in Outbox" handler
    Module A ->> Module A Outbox: Store event
    Event Bus ->> Module A: Trigger all other event handlers
```

```mermaid
---
title: Processing Notification Event
---
sequenceDiagram
    participant Module A Outbox
    participant Module A Outbox Processor
    participant Event Bus
    participant Module A
    participant Module A Inbox
    participant Module B
    participant Module B Inbox
    note over Module A Inbox, Module B Inbox: inboxes needed to process command only ones
    Module A Outbox Processor ->> Module A Outbox: Get unprocessed Notification Events
    Module A Outbox Processor ->> Event Bus: Publish Notification Event<br>originating from DomainEventA
    Event Bus ->> Module A: Trigger notification handler
    Module A ->> Module A Inbox: Store command
    Event Bus ->> Module B: Trigger notification handler
    Module B ->> Module B Inbox: Store command
    Module A Outbox Processor ->> Module A Outbox: Mark event as processed
```

```mermaid
---
title: Processing Inbox
---
sequenceDiagram
    participant Module A Inbox
    participant Module A Inbox Processor
    participant Module A
    participant Module B Inbox
    participant Module B Inbox Processor
    participant Module B
    Module A Inbox Processor ->> Module A Inbox: Get unprocessed commands
    Module A Inbox Processor ->> Module A: Process command
    Module A Inbox Processor ->> Module A Inbox: Mark command as processed
    Module B Inbox Processor ->> Module B Inbox: Get unprocessed commands
    Module B Inbox Processor ->> Module B: Process command
    Module B Inbox Processor ->> Module B Inbox: Mark command as processed
```


## References
https://www.kamilgrzybek.com/blog/posts/handling-domain-event-missing-part
https://devblogs.microsoft.com/cesardelatorre/domain-events-vs-integration-events-in-domain-driven-design-and-microservices-architectures/
