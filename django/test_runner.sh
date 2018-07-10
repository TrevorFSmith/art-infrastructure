#!/bin/bash
#
if [[ $1 ]]; then
  ./manage.py test $1.api.v1.tests --settings=ai.test_settings #--failfast
else
  ./manage.py test artwork.api.v1.tests --settings=ai.test_settings
  ./manage.py test iboot.api.v1.tests --settings=ai.test_settings
  ./manage.py test lighting.api.v1.tests --settings=ai.test_settings
  ./manage.py test weather.api.v1.tests --settings=ai.test_settings
fi


