# Error Listing

Each error has a name that can be used in the `-i` flag to ignore it.

## Errors

- `CourseXMLDoesNotExist`: The supplied `course.xml` file does not exist (or could not be opened).

- `DuplicateURLName`: Two tags have the same `url_name` attribute. This can lead to the wrong content loading.

- `ExtraURLName`: A tag that had been pointed to by `url_name` from another file has a `url_name` of its own.

- `FileDoesNotExist`: The file being pointed to does not exist.

- `InvalidHTML`: The specified HTML file has a syntax error

- `InvalidPointer`: This tag appears to be trying to point to another file, but contains unexpected attributes, and is hence not pointing.

- `InvalidXML`: The specified XML file has a syntax error.

- `NoRunName`: The course tag has no `url_name`, and hence no run name. This is a required parameter for a course.

- `PolicyNotFound`: The file policy.json was not found.

- `SelfPointer`: A tag appears to be pointing to itself.

- `TagMismatch`: A file purporting to contain a specific tag type (e.g., `problem` or `chapter`) instead contains a different tag.

- `UnexpectedContent`: A tag contains unexpected text content.

- `UnexpectedTag`: A tag was found in an inappropriate location (e.g., a `vertical` in a `chapter`), or the tag was not recognized.


## Warnings

- `CourseXMLName`: The master file was not called `course.xml`.

- `EmptyTag`: A tag was unexpectedly empty (e.g., a `chapter` tag had no children).

- `MissingDisplayName`: A tag is missing the `display_name` attribute. edX will fill a generic name for you.

- `MissingURLName`: A tag is missing the `url_name` attribute. edX will provide a garbage 32-character name for you, but everything is cleaner if you provide a nice name yourself.

- `NonFlatFilename`: A filename pointer for an HTML file uses colon notation to point to a subdirectory. While partially supported, this is not recommended.

- `NonFlatURLName`: A `url_name` pointer uses colon notation to point to a subdirectory. While partially supported, this is not recommended.

- `PossibleHTMLPointer`: This HTML tag looks like it isn't a pointer tag, but a file exists that it could be trying to point to.

- `PossiblePointer`: This tag looks like it isn't a pointer tag, but a file exists that it could be trying to point to. (This file is thus orphaned, as no other tag can point to it due to `url_name` clashes.)


## Information

- `DuplicateHTMLName`: Two HTML tags point to the same HTML file (`filename` attribute). While this isn't obviously problematic, probably best not to do it.


## Debug

(Currently no errors in this category)

