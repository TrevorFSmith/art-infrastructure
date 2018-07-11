For development environment, the app requires `coffee` npm package. To install it on Ubuntu/Debian:

* sudo apt-get update
* sudo apt-get install nodejs
* sudo apt-get install npm
* sudo npm install -g coffee-script
* sudo npm install -g phantomejs
* sudo npm install -g selenium

Also please make sure you have `coffee@1.12.7` version installed:
* sudo npm install -g coffee@1.12.7

Note: Do not install latest 2.3.x version. It has a bug combinin Django Compressor


To run test, user `test_runner.sh`, eg, to run API tests for lighting module, use command:

$ ./test_runner.sh lighting

To run scheduler
python manage.py run_scheduler