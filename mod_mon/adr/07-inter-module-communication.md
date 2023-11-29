# Inter-modules communication

Modules should be highly decoupled from each other but there should also be a way to communicate between them. This is
 achieved by using domain events and derivatives of those and queries.

## Events

Events enable processing commands that span over multiple modules 

### Types

The table summarizes events and the context under which they should be used.

|     Event type    | Emitter/Handler transaction | Emitter/Handler Bounded Context |                       Comment                      |
|:-----------------:|:---------------------------:|:-------------------------------:|:--------------------------------------------------:|
| Domain Event      |             Same            |               Same              |               Can hold Value Objects               |
| Notification      |           Separate          |               Same              | Serializable; Versioned; Cannot hold Value Objects |
| Integration Event |           Separate          |             Separate            | Serializable; Versioned; Cannot hold Value Objects |

#### Domain Event

Used mainly to split use case processing that needs to be handled by multiple "DDD modules" which are part of the same
 Bounded Context. Because it's handled within the same transaction, the handler is always able to process the 
current event's payload (domain events are processed the moment they are published) which means those events do not 
need to be versioned and can hold `Value Object`

#### Notification

Enables splitting processing of a use case into multiple transactions which is important when e.g.
- the 1st handler executes the critical part which should not be rolled-back when other parts fail
- other parts are time-consuming

As this event is processed in a separate transaction, there needs to be a mechanism that assures a `Notification` is 
always handled. (Outbox and Inbox patterns)[https://microservices.io/patterns/data/transactional-outbox.html] are used
for that which guarantee "at leas once delivery". Because of the guarantee it's important for the handlers to 
process a `Notification` idempotently.

Delivery of a `Notification` should be retried on failure (with a limit of retries).

Because those events are stored in an `Outbox`, the event's payload might change before it's processed by its 
handlers. This requires versioning the events and makes incorporating `Value Object` forbidden as it should be 
freely adjusted to domain needs which poses a risk of introducing breaking changes to `Notification`

#### Integration Events

They are very much like `Notification` but processed in a different Bounded Context


## Queries

Queries enable retrieving data from other modules

### Types

|      Query type      | Emitter/Handler Bounded Context |                      Comment                     |
|:--------------------:|:-------------------------------:|:------------------------------------------------:|
| Externally triggered |             Separate            | Triggered by Client or different Bounded Context |
| Internally triggered |               Same              |       Triggered in the same Bounded Context      |

As `Query` is processed immediately in the same process it does not require versioning nor serialization and storing.


## Definitions of events, queries and queries results

Handling module should have the same event/query payload definition as the emitter or a subset of those. This 
doesn't mean that they need to share code as they each party can hold own copy of the payload.

Sharing code is acceptable for `Domain Event` and `Internally Triggered Query` as they are emitted and handled in 
the same Bounded Context. However, they should be accessible by different modules within Bounded Context from a 
single file and tests should ensure that modules do not import any other files.

Sharing code is not acceptable for all other events and queries as they are emitted and handled in different Bounded 
Contexts and importing `python modules` is forbidden between them.


## Events and queries delivery

Modules being decoupled means `python modules` must not be imported from external modules, or importing should be 
restricted to a `python module` which publishes an interface of a module. That makes it impossible to trigger 
external's module command handler (`ExternalModuleCommandHandler().handle(command)`) directly or even by some entry 
point provided by the module (`external_module.handle(command)`).

To deliver events and queries an independent (not belonging to any emitter nor handler) mediator/bus/pud-sub 
solution is required.

As mentioned in [Command and queries ADR](./06-commands-and-queries.md) the decision on using mediator will be made
after some use cases are implemented. However, if there's no need to distinguish between `externally and internally
triggered queries` (discussed in [Queries](#Queries)), the mediator should be used as the queries between modules
must use mediator.


## References
https://buildplease.com/pages/vos-in-events/#:~:text=Events%20are%20immutable.,Objects%2C%20but%20not%20for%20Events
https://www.kamilgrzybek.com/blog/posts/modular-monolith-integration-styles
https://www.kamilgrzybek.com/blog/posts/handling-domain-event-missing-part
https://github.com/kgrzybek/modular-monolith-with-ddd
https://devblogs.microsoft.com/cesardelatorre/domain-events-vs-integration-events-in-domain-driven-design-and-microservices-architectures/
