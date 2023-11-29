# Command and Queries

Client applications communicate with the system by sending HTTP requests which are handled in endpoints and in turn 
trigger commands and queries. Commands are used to change the state of the system, while queries are used to 
retrieve data from the system.

## CQS

The system applies [Command Query Separation](https://en.wikipedia.org/wiki/Command%E2%80%93query_separation) 
pattern with a remark that commands are allowed to return `private key` of the created entity.

## Using mediator to trigger handlers

Currently, it's not decided whether any mediator should be used to trigger handlers. The decision will be made after
some use cases are implemented.
