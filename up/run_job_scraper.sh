#!/bin/bash

while true;
do
  echo "Running job scraper" &&
  python upapp/scraper/scraper/runSpiders.py &&
  echo "Sleeping for 4 hours" &&
  sleep 14400;
done