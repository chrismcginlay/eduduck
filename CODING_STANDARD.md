#Coding Standard Notes#

##Function pre-condition asserts##
These should be used to provide expected initial conditions for most functions;
not necessary where get_entity_or_404() constructs are used.
All asserts must have no side effects.

##Function post-condition asserts##
Use these to specify return value properties where computation is cheap
All asserts must have no side effects.

##Class instantiation representation check##
Constructors should implement an assertion based representation check either 
directly in __init__() or in a separate myclass_checkrep() if representation
integrity will need to be checked repeatedly.