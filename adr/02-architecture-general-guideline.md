# Architecture general guideline

1. Modules are implemented as Python packages
2. Modules should be independent of each other
    - tools such as (importlinter)[https://github.com/seddonym/import-linter] should be used to ensure that modules do not depend on each other 
3. Modules should communicate with each other via clearly defined interfaces
4. Modules should reflect business domains
5. Each module may have its own sub-modules which reflect sub-domains or DDD modules
6. Domain Driven Design is the default approach to designing and implementing modules but it is not mandatory and each module may use a different approach
7. Each module should have its own ADRs
8. It is recommended to use Hexagonal Architecture (Ports and Adapters) but each module may use a different approach
