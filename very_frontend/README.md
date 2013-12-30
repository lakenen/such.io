# Such.io Frontend

This is the frontend code for such.io. Basically all the JS/static assets that consume the such.io API.

## Getting started

Install Node if you don't have that yet.


Install grunt-cli, yeoman, and generator-angular:
```
npm install -g grunt-cli yeoman generator-angular
```


Update ruby shit and install compass:
```
gem update --system
gem install compass
```


Install the app-specific stuff (do this in the frontend dir):
```
npm install
bower install
```


Run the server and watch it go!
```
grunt serve
```