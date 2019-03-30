# Wishlist

This is just a list of things that it would be nice to have in this program.

## Features

* Generate statistics about a course after scanning
* Course upload to edX via HTTP if error level satisfied
* Local configuration files

## Errors

### On course load:

- Conditional tags
- AB Test tags
- Note that discussion tags should be inlined
- Flag tag types that can't load from a directory

### On policy load:

- Policy file not found
- Error loading policy json
- Grade file not found
- Error loading grading policy json
- Policy file has wrong course name

### On updates load:

- Update file not found
- Error loading update json

### On parsing:

- Obsolete components (eg, discussions in discussion directory)
- Course tag has the three required attributes
- Test internal links, including all static folder links and textbook pdfs (policy)
- Test that python code runs
- Test that customgraders work when using expect calues in customresponse
- Python code is wrapped in CDATA
- Python has correct script type
- lti_consumer uses valid passport credentials
- Date fields in policy all evaluate using edX date evaluator
- Policy file chapter/sequential entries correspond to existing url_names
- Check that all release dates fall inside the course start and end dates
- Check that various open/close dates appear in order!
- Check that each update has the required elements, and that display text parses as html correctly
- FBE tags set up correctly
- Check that sequential format tags are in the grading policy
