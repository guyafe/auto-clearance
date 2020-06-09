# auto-clearance
Automatic cron job that daily sends a clearance report for school

This program takes 3-4 arguments: `parent id`, `parent password for Mashov`, `school symbol (6 digits)`, (optional) daily
If the 4th arguments exists and is **daily**, the program will laumvh a daily job that each morning at 7:00 will send the report.
If this argument is missing, the report will be sent once.
