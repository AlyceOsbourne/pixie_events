## Pixie Events
(This is a work in progress, and currently very much a proof of concept)
___
 A global event system emulating pythons dunder style magic
___

### Current Features:
- Global `__setup__`, `__update__` and `__teardown__` magic dunders
- Flow control decorators `@before`, `@after` and `@priority`
- Event attrs, decorators and functions to simplify intercommunication of modules
- Event based Input system, just listen to the mouse or keyboard and get events for them

### How does it work?
It utilizes a module scanning system to find these methods and run them they dynamically.
This is controlled by a system loop. The loop is started by calling `.run()` from the core module, 
and can be ended by calling `.finish()`

 With the event system there are multiple ways to utilize it, you can use the `@subscribe` decorator with an event name, 
or you can utilize the `Event` enum class, where each member is a declared event which you can subscribe to.
The event system also include an `EventAttr` descriptor for you to use for observable attributes
that you want to trigger an event when changed (this is still being improved)

### How do I use it?
~ to be added ~