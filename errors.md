# Error Listing

Each error has a name that can be used in the `-i` flag to ignore it.


## Errors

- `CourseXMLDoesNotExist`: The supplied `course.xml` file does not exist (or could not be opened).

- `InvalidXML`: XML syntax error detected.

- `InvalidHTML`: HTML syntax error detected.

- `TagMismatch`: A file purporting to contain a specific tag type (e.g., `problem` or `chapter`) instead contained a different tag.

- `ExtraURLName`: A tag that had been pointed to by `url_name` from another file has a `url_name` of its own.

- `InvalidPointer`: This tag appears to be trying to point to another file, but contains unexpected attributes, and is hence not pointing.

- `FileDoesNotExist`: The file being pointed to does not exist.

- `SelfPointer`: A file seems to be pointing to itself.

- `UnexpectedTag`: A tag was found in an inappropriate location. E.g., a `vertical` in a `chapter`.

- `UnexpectedContent`: A tag contains unexpected text content.

- `DuplicateURLName`: Two tags have the same `url_name` attribute. This confuses edX, and can lead to the wrong content loading.

- `NoRunName`: The course tag has no `url_name`, and hence no run name. This is a required parameter for a course.


## Warnings

- `CourseXMLName`: The master file was not called `course.xml`, which is required by edX.

- `EmptyTag`: A tag was unexpectedly empty. E.g., a `chapter` tag had no children.

- `PossiblePointer`: This tag looks like it isn't a pointer tag, but a file exists that it could be trying to point to. (This file is thus orphaned, as no other tag can point to it due to `url_name` clashes.)

- `NonFlatURLName`, `NonFlatFilename`: Occurs when a `url_name` or `filename` pointer uses colon notation to point to a subdirectory. While vaguely supported, this is not recommended, as various internal edX systems do not recognize it.

- `MissingURLName`: A tag is missing the `url_name` attribute. edX will provide a garbage 32-character name for you, but everything is cleaner if you provide a nice name yourself. 

- `MissingDisplayName`: A tag is missing the `display_name` attribute. edX will fill a generic name for you.
