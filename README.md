# CI-LinuxCommandGenerator-v2
Code Institute Milestone 3 - Data Centric Development

### Project Description/Goals

### Demo
<!-- INSERT GIFs -->

### Technologies used
- Python
- Flask
- PyMongo
- DNSPython 
- Pyperclip
- WTForms
- reCAPTCHA
- MongoDB
- Bootstrap
- HTML, CSS, JS


## UX
<!-- discuss goals of site -->
### User Stories
As a Linux user I want a site I can use to look-up common terminal commands to install popular apps
As a Linux enthusiast I want to be able to add, update, and delete commands so I can contribute

### Strategy
<!-- discuss background ideas etc -->

### Scope
<!-- discuss planning, what's in what's not etc -->

### Skeleton
#### Wireframes
<!-- INSERT WIREFRAMES -->

### Surface
<!-- discuss design/style/fonts/colours etc -->

### Must-have Features
- CRUD functionality --DONE
- General/basic search function i.e. search by distro name or app name & return all results --DONE
- Advanced search function i.e. additional fields to significantly narrow results
- Simple user friendly interface

### Nice-to-have Features
- Wishlist/shopping list where users can save commands --DONE
- Up-vote/down-vote functionality per command
- Download/email saved commands as a shell script

## Deployment
<!-- insert detailed step-by-step instructions WITH IMAGES for each part of proj -->

## Testing
<!-- manual testing? automated testing? e2e testing? etc -->

## Validation
<!-- confirm validation of HTML/CSS/JS/PYTHON/ACCESSABILITY -->

## Bugs

### Open Bugs
<!-- Describe bug, what's wrong, what's the cause, why isn't it fixed -->
 - pylint validator presents problems/warnings saying *Instance of 'WTForm_with_ReCaptcha' has no 'errors' member*
    - **CAUSE**: Unknown, form.errors is working and returning errors so pylint warning doesn't appear to causing any actual issue.

### Squashed Bugs
<!-- Detail discovery/test/fix -->
- Delete confirmation screen would always proceed to delete regardless of whether Delete or Cancel button was selected.
    - **CAUSE**: This was due to the WTForm SubmitField response being a boolean. So the response would always be True regardless of which button was clicked since both are valid Submit buttons.
    - **FIX**: Remove the Cancel version of the SubmitField button and replace with a link to the default Find view.

# Credits/Acknowledgements
- MongoDB regex guidance from:
    - [Regex Query in Mongo docs](https://docs.mongodb.com/manual/reference/operator/query/regex/) 
    - [this stackoverflow question](https://stackoverflow.com/questions/3305561/how-to-query-mongodb-with-like)
- reCAPTCHA implementation with guidance from:
    - John Sobanski's [Easy ReCAPTCHA with Flask-WTF](https://john.soban.ski/add-recaptcha-to-your-flask-application.html)
    - soumilshah1995's [YouTube demo](https://www.youtube.com/watch?v=MmHrncoIOO8)