#!/bin/bash

set -e

check_logs_and_send_report(){
	
	# Create log file if not exists
	if [ ! -f ".log_size" ]
	then
	    touch ".log_size"
	fi
	
	# Rename file with sizes
	mv .log_size .log_size_temp

	message=""

	# Loop through all .log files in the current directory
	for file in *.log; do
	  # Get the current size of the file
	  size=$(stat -c %s "$file")
	  
	  # Get the previous size from the hidden .log_size file
	  prev_size=$(cat .log_size_temp 2>/dev/null | grep "$file" | cut -d' ' -f2)
	  
	  # Compare the sizes and print a message if the size has increased
	  if [[ -n "$prev_size" && "$prev_size" =~ ^[0-9]+$ && "$size" -gt "$prev_size" ]]; then
	    difference=$((size - prev_size))
	    message+="<b>$file</b> +$difference bytes%0A"
	  fi
	  
	  # Record the current size in the .log_size file
	  echo "$file $size" >> .log_size
	done

	# Delete old file with sizes
	rm .log_size_temp

	# Send data to the telegram bot
	if [[ -n "$message" ]]; then
	  echo -e "$message"
	  curl -s -X POST https://api.telegram.org/${TELEGRAM_BOT_TOKEN}/sendMessage \
	       -d chat_id=${TELEGRAM_CHAT_ID} -d parse_mode=html -d text="$message"
	fi
}

check_logs_and_send_report

exit 0
