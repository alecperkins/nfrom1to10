#!/bin/sh

# Launches development environment stuff
  
  osascript <<-eof
    set app_directory to "~/Projects/nfrom1to10/"
    
	tell application "iTerm"


		set staticterm to (make new terminal)
		tell staticterm

			launch session "Default session"
			tell the last session
				set name to "Compass"
				write text "cd " & app_directory
				write text "compass watch"
			end tell

			launch session "Default session"
			tell the last session
				set name to "CoffeeScript"
				write text "cd " & app_directory
				write text "coffee -o templates/ -w -c ui_source/coffee/*.coffee"
			end tell

			launch session "Default session"
			tell the last session
				set name to "Livereload"
				write text "cd " & app_directory
				write text "livereload"
			end tell

		end tell
	end tell

eof