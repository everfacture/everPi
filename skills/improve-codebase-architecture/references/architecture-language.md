# Architecture Language

Shared vocabulary for architecture reviews.

## Terms

**Module**
Anything with an interface and implementation. Scale-agnostic: function, class, package, subsystem, vertical slice.

**Interface**
Everything caller must know to use module correctly: type signature, invariants, ordering constraints, error modes, configuration, performance characteristics.

Avoid using “interface” only as TypeScript/class surface. Architecture interface is wider.

**Implementation**
Code inside module. Distinct from adapter: implementation is substance; adapter is role at seam.

**Depth**
Leverage at interface. Deep module gives much behavior behind small interface. Shallow module exposes almost as much complexity as it hides.

Depth is not implementation-lines / interface-lines. Depth is usefulness per concept caller must learn.

**Seam**
Place where behavior can change without editing caller. Prefer “seam” over overloaded “boundary”.

**Adapter**
Concrete thing satisfying interface at seam. Describes role, not substance.

**Leverage**
What callers get from depth: capability per unit of interface learned.

**Locality**
What maintainers get from depth: change, bugs, knowledge, and verification concentrated in one place.

## Principles

**Deletion test**
Imagine deleting module. If complexity vanishes, module was pass-through. If complexity reappears across N callers, module earned keep.

**Interface is test surface**
Callers and tests cross same seam. If tests must reach past interface, module may be wrong shape.

**One adapter = hypothetical seam. Two adapters = real seam**
Do not introduce seam unless something varies across it or near-term variation is proven.

**Domain names create good seams**
Use project domain vocabulary from `CONTEXT.md`, README, docs, and ADRs. Good module names usually map to domain concepts, not implementation mechanisms.

## Relationships

- Module has interface and implementation.
- Seam is where interface lives.
- Adapter sits at seam and satisfies interface.
- Depth creates leverage for callers and locality for maintainers.
