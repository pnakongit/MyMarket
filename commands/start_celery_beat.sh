#!/bin/bash

celery -A config beat -l ${CELERY_LOG_LEVEL} -S django
