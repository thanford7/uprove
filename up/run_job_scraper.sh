#!/bin/bash

while true;
do
  echo "Running job scraper" &&
  python -m upapp.scraper.scraper.runSpiders &&
  echo "Sleeping for 4 hours" &&
  sleep 14400;
done