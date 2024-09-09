# Known Issues

### File Exclusion
- Commented lines (beggining with a #) are not properly processed in ".contextignore"
- __pycache__ is still being included in "context.txt" file, even when listed in ".contextignore"