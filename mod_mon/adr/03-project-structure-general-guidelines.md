# Project structure general guidelines

Project structure should enable easy navigation and understanding of the project. Thus, most of the code should be placed
in modules. Project structure should be as close as possible to the following reference structure:

```
project_name
├── adr
├── api  // this is the "entry point" of the application; does not define endpoints but imports them from modules
├── shared_kernel   // domain code shared by different modules
├── infrastructure  // code related to infrastructure (e.g. database, message broker, ...)
├── tools
├── tests   // application level tests; each module should have its own tests
├── module_1  // module code which follows the structure described below
├── ...
```

Each module should follow the following structure:

```
module_name
├── adr
├── api
├── core
├── tests
```
