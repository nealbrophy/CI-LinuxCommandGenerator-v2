# CI-LinuxCommandGenerator-v2
Code Institute Milestone 3 - Data Centric Development

### Project Description/Goals
The Linux Command Generator v2 is an interface for performing CRUD (Create, Read, Update, Delete) operations on a MongoDB database of linux terminal commands. As a user of linux and occasional distro-hopper I often need to re-install apps and wanted somewhere I could easily access terminal commands for doing so. This is an expansion/continuation of my Interactive Front End milestone Linux Command Generator v1.1 but now with the ability to easily add/update/remove commands as needed. Additionally, one of my future 'like to have' features for the Interactive Front End milestone was the ability to email a list of commands so I wanted to make sure to include that functionality in this version.

### Demo
You can view the deployed site on [Heroku](https://linux-command-generator.herokuapp.com/)
<img src="https://github.com/nealbrophy/CI-LinuxCommandGenerator-v2/blob/master/static/images/desktop-view.gif" alt="site demo on desktop" width="650px" align="left">

<img src="https://github.com/nealbrophy/LinuxCommandGenerator_v1.1/blob/master/static/images/mobile-view.gif" alt="site demo on iphone" width="200px" align="center">

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
Given the intended audience & purpose of the site (*Linux enthusiasts* and *simple storage/retrieval of terminal commands*, respectively) I wanted a clean, straight-to-the-point user experience. I ultimately decided to use a card-based layout to achieve this goal and keep animations etc to a minmimum. My approach was the same when it came to the navbar, I wanted to keep the buttons to the fewest necessary to achieve the intended goals to that end certain functions (edit command, delete command) don't have their own dedicated section in the navbar but are rather reached via the main 'Find' page.

Upon first reaching the site I wanted users to be able quickly see what's available while also not overwhelming them with a page of full of commands. To achieve that I decided to present only the distros which currently have commands and to display how many commands are availble for those distros. I later decided that I wanted to at least make users aware that other distros are available but simple don't have any commands to display yet, hence the footer on the main page with a list of empty distros.

### User Stories
As a Linux user I want a site I can use to look-up common terminal commands to install popular apps.
As a Linux enthusiast I want to be able to add, update, and delete commands so I can contribute.

### Strategy
The goal of the site is to be fast & easy to achieve the intended use of adding, updating, removing, emailing stored terminal commands. I wanted the layout to be simple and intuitive. Conversely, I wanted to add a little security as well to avoid malicious/spam additions, for this I decided to use recaptcha to avoid the need for an "approval" step where someone would need to view & confirm/accept pending commands before they would be added. However that is a feature I would like to add in future.

### Scope
I decided at the beginning of the project that the must have features were CRUD (Create, Read, Update, Delete) operations, the ability to save commands to a list, the ability to email the saved list. When evaluating what kind of security measures to put in place I considered adding a login/sign-up option and then having the create/delete functions only available from within but detemined that ran counter to the previously decided upon objective of being simple & straight to the point.

In terms of available operations, I considered "Edit Distro" and "Delete Distro" ops but again decided that if the intended goal was straight-to-the-point *COMMAND* retrieval then distro based operations were out of scope, and it was better to offer a simple "Add distro" operation for cases where a user wants to add a command but the distro in question isn't available. Since I intend to use the site myself when distro hopping and something I often find myself doing is copying & pasting commands I wanted to make this option as simple as possible, thus there is a *copy* button on all cards where a command is displayed.

### Skeleton
#### Wireframes
<img src="static/images/wireframes.png" alt="desktop-wireframe-1" width="500px">

### Surface
For the look of the site I wanted something bright & simple. I was picturing comicbook colours and similarly "cartoonish" fonts. With comicbook colours in mind I eventually decided on a "Captain America" type Blue (#478eff) colour as the main navbar colour. Using the [sessions.edu color calculator](https://www.sessions.edu/color-calculator/) I decided upon the "triadic" colours of yellow (#ffed47) & pinkish (#ff476c) to accompany the blue (mostly to be used for highlights & hovers). In keeping with the cartoonish theme I wanted some colorful images and stumbled upon [https://illlustrations.co/](https://illlustrations.co/). Grabbing some computer-related images from there I implemented a random_images function to choose which of the selection of images to display when the main page loads.

After implementing the card layout and basic CRUD operations I found that the cards were looking a little cluttered/busy with the varying "instruction" and "command" lengths, so I used the material.css "truncate" class to abbreviate those fields and have the full content appear instead in a tooltip when hovered. 

### Features
- Responsive navbar
- Randomly changing header image on main page
- Responsive card layout
- My List section to allow users to save commands for later
- Email My List function to allow users to email their list of saved commands
- Simple user friendly interface

### Future Features
- Peer-approval feature where commands added are flagged as un-approved in some way until an admin user evaluations & approves them.
- Download/email saved commands as a shell script
- Ability to edit or delete Distros limiting deletion to only distros which do not have any commands

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
