# Data Quality Report Generator

A Python pipeline I use to generate a quick data quality report on raw tabular data.
It helps me determine key feature data quickly without relying on notebook environments.

config/  		# Where I place project configuration files and rules
data/inputs/ 		# Raw incoming datasets
data/outputs/ 		# Exported Excel Reports
src/__init__.py		# Package initialization
src/ingestion.py	# File path validation
src/metrics.py		# Split between continuous and categorical metrics
src/formatter.py	# Report styling and formatting
.gitignore		# Version control exclusion
main.py			# Project orchestration
requirement.txt		# Project dependencies
README.md		# Technical documentation