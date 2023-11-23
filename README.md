# Modular_monolith

## Project goals

The "mission" of this project is to create a modular monolith project to be used in the future as a template for other
new projects. This includes evaluating different libraries which may help creation and maintenance of such project.

My ambition is to also evaluate different ways of using the patterns used in this project when refactoring
a non-modular legacy codebase.

### Priorities
1. Solve problem of communication between modules (with and without Anti Corruption Layer)
2. Assessing how to use such a template in legacy code
3. Getting to know the Dependency Injection lib(s) (comparison with HAPS, which is used in the project I currently work in, mainly in terms of the alleged disadvantages of the "service locator")
4. Solving the "cross-cutting concerns" problem (logging in, transaction management, ...)
5. Assessment of different ways to solve the problem of access rights to entities (different user roles)
6. Assessing the benefits and drawbacks of mixing domain models with DB mapping and other non-"Clean Architecture" patterns

## Project setup

### Prerequisites
1. Python 3.9 or higher
2. pip-tools

### Installation
1. Clone the repository
2. Run `pip-sync` to install all dependencies
