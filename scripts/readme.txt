/system script
add name="cleanup_hotspot_sessions" source="cleanup_hotspot_sessions"

	1.Access the Script Menu:
/system script

	2.Add the Script:
add name="cleanup_hotspot_sessions" source="(paste your script here)"

	3.View the Script:
print

	4.Edit the Script if Needed:
set 0 source="(update your script here)"

    5.You can execute the script manually:
/system script run cleanup_hotspot_sessions

    6.Use the schedulr to run the script daily:
/system scheduler
add name="daily_cleanup" on-event="cleanup_hotspot_sessions" interval=1d start-time=00:00:00
