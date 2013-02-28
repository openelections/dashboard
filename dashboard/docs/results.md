## OpenElections Results Data

The goal of OpenElections is to provide clean, consistent results data for federal, statewide and state legislative races from all 50 states, and to make it easy for journalists (or anyone else) to access them in common data formats. The aim is to provide a minimum set of information for each race, supplemented by additional data that may be available from the state.

Our results spec is a work in progress, and likely will change as the project develops. Your input on the contents of results data and ways that users can retrieve them are welcomed. Join our Google Group, or send us an email at openelections@gmail.com.

### Formats

The initial formats for results data are CSV and JSON, both lightweight text formats that can be easily used by applications ranging from Microsoft Excel to web application frameworks or mobile applications. All files described below are available as both CSV and JSON by adding those extensions to filenames. Future formats may include XML, and we welcome your feedback.

### State Metadata

Results data is organized primarily by state and then by year within each state. Each state has a top-level directory labeled with its two-character state abbreviation, such as "MD" for Maryland. At the top level a file "metadata" contains basic information about the availability of results for that state. The layout for the metadata file is as follows:

  * years - an array of integers listing the years for which OpenElections has election information.
  * updated_at - a timestamp indicating the last update to any of the state's files.
  * volunteers - an array of OpenElections usernames indicating people who have contributed to this state's results.
  
In the CSV version, years and volunteers are comma-delimited text; in JSON they are standard arrays.

### Elections by Year

Inside a particular year's directory within a state there is a file called "elections" listing the elections that occurred in that year and information about the status and scope of results data. An example url would be: http://example.com/us/states/md/2012/elections.json

The layout of the elections file is as follows:

  * year - an integer representing the year of the elections
  * state - the two-character state postal abbreviation
  * elections - an array of hashes containing individual election information (json file only)
  * date - the date of the election
  * results_type - the type of results available (Certified, Unofficial or null)
  * election_type - 'primary', 'general', 'runoff' or other election type
  * special - a boolean indicating whether the election is a special election
  * office - a string representing the office contested in the election
  * result_levels - an array containing a hash of the availability of results at certain levels (json file only)
  * race_wide - a boolean indicating whether race-level results are available
  * county - a boolean indicating whether county-level results are available
  * congressional_district - a boolean indicating whether congressional district level results are available
  * state_legislative - a boolean indicating whether state legislative district level results are available
  * precinct - a boolean indicating whether precinct-level results are available
  * updated_at - a timestamp indicating when the given election was last updated
  
### Race-wide Results for an Election

Each election date represents a directory containing CSV and JSON files covering elections to specific offices. For example, the Nov. 6, 2012 general election results would be stored in a 2012-11-06 directory, and the filenames would represent offices such as "president", "us-senate" and "us-house". Each office file would contain one record for each candidate listed in the results. The result records consist of at least these fields:

  * first_name - a string representing the parsed first name of the candidate
  * middle_name - a string representing the parsed middle name or initial of the candidate
  * last_name - a string representing the parsed last name of the candidate
  * suffix - a string representing the parsed suffix of the candidate
  * name_raw - a string representing the "raw" full name of the candidate from the results, if present
  * party - a string representing the "raw" party name or abbreviation from the results
  * winner - a boolean marked true for the winning candidate; all other candidates are marked as false
  * votes - the race-wide number of votes received by a candidate
  * pct - the race-wide percentage of votes received by a candidate
  
Depending on the state, there may be other fields in the results data, including:

  * write_in - a boolean marked true if the candidate is a write-in candidate
  * precincts - the total number of precincts for a reporting level
  
### Other Result Levels

Results files for other reporting levels, such as county, legislative district or precinct, will have the same minimum set of fields as race-wide results but in addition will have the reporting level and the name of the jurisdiction, whether a county, district or precinct number.