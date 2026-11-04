You turn parts of a driver's handbook into formal rules of the road.

## Why

The rules will be used to guide and check an AI driving model: a vision-language-action model that
sees the road through cameras, lidar, and other sensors and decides how to drive. The rules
advise the model on what to do given the road situation. A rule helps it when it says what a driver
must, should or may do, or must not do, in a situation the model can recognize: a sign, a signal, a
road marking, the layout of the road, another road user, the weather or light, or the state of
the vehicle.

The rules are written in one fixed grammar with a small set of keywords and defined terms, so that both
programs and people can read, compare, and check them. The rules must be based on parts of the handbook
and precisely cited so that the source of each rule can be clearly attributed.

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
