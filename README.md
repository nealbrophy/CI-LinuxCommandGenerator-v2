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
- WTForms
- reCAPTCHA
- Flask-Toastr
- SendGrid
- MongoDB
- Materialize.css
- HTML, CSS, JS


## UX
Given the intended audience & purpose of the site (Linux enthusiasts and simple storage/retrieval of terminal commands, respectively) I wanted a clean, straight-to-the-point user experience. 

### User Stories
As a Linux user I want a site I can use to look-up common terminal commands to install popular apps.
As a Linux enthusiast I want to be able to add, update, and delete commands so I can contribute.

### Strategy
The Linux Command Generator v2 as the name suggest is a continuatiun/expansion of the idea from my Milestone 2 project. I wanted to take the same concept forward but add some desired features which were missing from that project (e.g. the ability to email a list of saved commands) and the ability to add, edit, delete commands as needed.

### Scope
I decided at the beginning of the project that the must have features were CRUD operations, the ability to save commands to a list, the ability to email the saved list, 

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
 

### Squashed Bugs
<!-- Detail discovery/test/fix -->
- Delete confirmation screen would always proceed to delete regardless of whether Delete or Cancel button was selected.
    - **CAUSE**: This was due to the WTForm SubmitField response being a boolean. So the response would always be True regardless of which button was clicked since both are valid Submit buttons.
    - **FIX**: Remove the Cancel version of the SubmitField button and replace with a link to the default Find view.
- pylint validator presents problems/warnings saying *Instance of 'WTForm_with_ReCaptcha' has no 'errors' member*
    - **CAUSE**: See [Nearoo's answer on stackoverflow](https://stackoverflow.com/a/52927347)
    - **FIX**: Added .pylintrc file to root directory as outlined in stackoverflow answer
- ReCAPTCHA form data in POST transmits with value of None.
    - **CAUSE**: Still not entirely sure why but the problem was being caused by having the choices parameter in WTForm SelectField populated by a dictionary (which in turn was populated from MongoDB).
    - **FIX**: Using the 'coerce=str' placeholder in the form definition, then populating  within the Flask Views using a for loop to populate a list with values for the SelectField choices. See [this stackoverflow answer](https://stackoverflow.com/a/48236887) for more information.

# Credits/Acknowledgements
- MongoDB regex guidance from:
    - [Regex Query in Mongo docs](https://docs.mongodb.com/manual/reference/operator/query/regex/) 
    - [this stackoverflow question](https://stackoverflow.com/questions/3305561/how-to-query-mongodb-with-like)
- reCAPTCHA implementation with guidance from:
    - John Sobanski's [Easy ReCAPTCHA with Flask-WTF](https://john.soban.ski/add-recaptcha-to-your-flask-application.html)
    - soumilshah1995's [YouTube demo](https://www.youtube.com/watch?v=MmHrncoIOO8)
- Abstract background vector from [Creative_hat on freepik](https://www.freepik.com/free-photos-vectors/banner)
- illustrations by [vijay verma](https://illlustrations.co/)
