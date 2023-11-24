# Testing strategy

## Levels of testing

1. domain logic
    - should be used when given module contains complex domain logic
2. adapters
    - should be used when adapters code in given module contains complex logic (e.g. complex database queries)
3. use cases
   - it's the default level of testing as it coordinates domain logic and infrastructure and so writing tests on use 
     cases level should cover most of the code
   - in case of simple domain logic, it can be used instead of domain logic testing
   - in case of complex domain logic, those tests should only cover coordination between domain logic and 
     infrastructure as the execution of use cases tests introduces penalty on performance as those tests require 
     database connection
4. api
   - should check api specific code (e.g. validation, middlewares)
5. application (end-to-end)
   - should not be used to test domain logic nor use cases
   - should mainly check if all the components are wired together correctly
6. integration
   - should check the behaviour of the application when multiple related use cases are executed


## Guidelines

1. Mocks should be avoided as much as possible as they tend to produce false positives.
2. To set up test data, use libraries like [FactoryBoy](https://factoryboy.readthedocs.io/en/stable/index.html) 
   or create fixtures that execute use cases.
3. Divide test cases into given/when/then sections. Use comments to mark those sections.
