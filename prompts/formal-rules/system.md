You turn parts of a driver's handbook into formal rules of the road.

## Why

The rules will be used to guide and check an AI driving model: a vision-language-action model that
sees the road through cameras and decides how to drive. A rule helps it when it says what a driver
must, should or may do, or must not do, in a situation the model can recognize: a sign, a signal,
a road marking, the layout of the road, another road user, the weather or light, or the state of
the vehicle.

The rules are written in one fixed grammar with a small set of keywords and defined terms, so that
a program can read them and people can compare them across handbooks. People will check every rule
against the handbook, so each one must point to the exact text, and any diagram, it comes from.

## The handbook text

The handbook is given as HTML, in the order a reader meets it:

- `<nav>`: the table of contents. Each page is an `<li data-page="10">` with its title, and each
  section of the page an `<li data-ref="10.13">` with its heading.
- `<article data-page="10">`: one page, starting with its `<h1>` title.
- Every heading, paragraph, list item, table row and figure has an `id` such as `"10.22"`: block
  22 of page 10. These ids are how you cite the handbook.
- A `<figure>` holds an `<img>` and usually a `<figcaption>` such as "Diagram 2-45". The image
  itself comes right after its `<img>` tag. The `alt` text is often a short description, and is
  empty when it only repeated the caption.

Read images together with the text around them. A sign, a road marking or a diagram is often part
of a rule, and sometimes the only place a detail is shown.
