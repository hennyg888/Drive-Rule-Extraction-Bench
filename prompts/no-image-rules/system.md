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
- Every heading, paragraph, list item and table row has an `id` such as `"10.22"`: block 22 of
  page 10. These ids are how you cite the handbook.
- The handbook is given as text only. Its images (signs, road markings, diagrams) and their
  captions have been taken out. Block numbers skip where an image was, so `"21.6"` may be followed
  by `"21.8"`.

The text sometimes points to an image that is not there ("See Diagram 2-11", "this sign"). Work
from the words alone: do not guess what a missing image shows, or fill in what a sign or marking
usually means elsewhere.
