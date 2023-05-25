# ISENSIT multi sensor
Multisensor integration on Home Assistant

# Guide
## Setup install
 1. Ensure the version of Home Assistant. It should be supervisor version.
 2. Enter the 'Settings' section. 
 3. Search and install 'Mosquitto broker' from add-ons.
 4. Start the broker and ensure the Home Assistant and Multisensor are under same internet.

## Plugin install
 1. Download HACS from Home Assistant.
 2. Enter 'integration' and click three dots at the top right corner.
 3. Enter the URL of the plugin and select 'integration'.
 4. Click '+' at bottom right corner and search for 'isensit' or 'multisensor'.
 5. Click 'install' and restart Home Assistant after installation.
 6. Enter 'Settings' and select 'Devices & Services'.
 7. Click 'Add integration' at bottom and search for 'isensit' or 'multisensor'.
 8. All the settings are done. Device and entities will jump out when topics are received.
