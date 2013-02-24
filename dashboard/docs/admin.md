## How to Help OpenElections

Election data is hard. We need your help to make it easy. And free (as in speech and beer).

The OpenElections Project is a nationwide effort to gather election results for federal and gubernatorial races in all 50 states. Election data is useful, but it’s much more interesting when linked to campaign cash, legislation and demographic data.  With your help, we’ll gather election results and link it to other public data sets so that anyone -- journalist, civic hacker, academic, curious citizen -- can have access to a robust and useful set of election data.

But first we need the data. That’s where you come in.

The first phase of OpenElections is about getting the lay of the land. For each state, we want you to look beyond what’s posted on election agency websites and identify the best available data sources. By developing relationships with election agencies and other organizations and experts, you’ll help us identify the best sources of results for your state.

Gathering metadata - the data about the data - from those sources sets the stage for the second phase: collecting election results. Whether you’re a student, a journalist, a developer or a civic-minded retiree, we want your help with getting the data. To contribute, you can adopt a state, gather some metadata about its elections and submit CSVs that meet our data spec.

### Defining the Important Bits

As much as we’d like to have the most comprehensive election results data in human history, we have to make some decisions on scope. Here is what is important to this project.

OpenElections is focused on official results for federal and most statewide elections (meaning gubernatorial and other state officials), plus state legislative elections where they are easy to obtain. We are not asking for data pertaining to county or municipal races (not yet, at least). The statewide offices we’re most interested in include governor, lieutenant governor, attorney general and treasurer, although many states have different offices and we’ll take what we can get.

The time frame for OpenElections, at least for now, is from 2000-on. Again, we won’t turn away official results from prior to 2000, but the focus is on building up a consistent dataset for the past 12-13 years. While our preference is for official, certified results, if those aren’t available we’ll accept unofficial results until we can update them.

Finally, we care about all elections that fit the first two criteria, meaning primary, runoff, general and special elections. That’s the preamble. Now let’s get the data!

### Metadata Gathering

So you adopted a state. Now what? Make a phone call. Maybe several phone calls. Yes, election results are online. But never assume an agency website has the best data available.

There could be a rich, clean database of results lurking behind those spreadsheets posted on the web. Step one is to call the state election agency and ask about their results data. Do they have a results database? Do we need to file a formal records request to get it? Are we stuck with whatever is posted online? Do we have to call county agencies to get the data we want?

We’ve created a data hub admin site that lets you track conversations with data sources and their offerings. In most cases, you’ll start with the official state agency that handles elections.

Once you’ve identified the best source of data, tell us about it in the admin.

### The Metadata Process

There are many different kinds of elections, but we want to know the same basic information about all of them. The metadata process begins with an election’s date, and includes the types of offices on the ballot, the range of results available and more. We’ll go over these in more detail, but here is a brief overview of the information we need.

Elections are mostly regularly-scheduled affairs, so we track them by date. Usually that means many races will be held on the same day, but there are also special elections that can be held throughout the year, and there is a special process for tracking those described below. So let’s start with the date of the election.

From there, we’ll need some basic information, including relevant URLs from the source, what type of results ("Certified" or "Unofficial" - all results are unofficial until they are certified) and the format(s) that are available.

### Using the Data Hub Admin

If you haven’t already received login credentials for the data admin, you should contact the OpenElections team at openelections@gmail.com.

The Data Hub includes several forms for data entry. The primary interface is the States section, which you can click to navigate to the data entry page for your state.

![Data Hub](https://s3.amazonaws.com/openelex-static/docs/admin_main.png)

### State Data Entry Portal

Each state page contains a note for general information about election results in the state. The page also contains sub-forms for entering election metadata and logging the history of correspondence with election officials. 

You’ll spend most of your time in the Election subforms, which can be added by clicking the “+” button to create a new record.
Election Metadata

Each election metadata entry form has five sections which will be explained in detail below:

* Data Source
* Election Meta
* Special Election
* Offices Covered
* Reporting Levels
* Notes

### Data Sources

![Data Source](https://s3.amazonaws.com/openelex-static/docs/data_source.png)


The Data Source section allows us to track the source of a set of election results, and provide information about the formats.

**Organization** -- Select the source agency. If the organization is not yet in the system, use the Organization pop-up form to enter it’s information.

**Portal Link** - Link to the page that contains the direct link to a data set, or possibly to a web form that allows you to request it (may not always be available).

**Direct Links** - Direct URL of the data set, if available (it won’t always be).

**Result type** - Is this data set unofficial or certified? The latter represents the final vote tally and often includes counts of provisional and absentee ballots.

**Formats** - Election results come in many file formats, but we have identified a small collection that are most commonly used. These range from HTML (usually in tables) to CSV (comma separated values) to PDF, with some others. In some cases, it may be necessary to open the file and assess the format. If the state you are working on has a format that is not present in the admin, let us know and we’ll figure out whether to add a new record or to place it within an existing format.

### Election Meta

![Election Meta](https://s3.amazonaws.com/openelex-static/docs/election_meta.png)

The Election Meta section tracks top-level info about the election. **Each type of race should get a separate Election Metadata entry in the admin**. For example, if a typical general election date in November also included two runoffs for U.S. House and a recall election for governor, you would create three separate entries: One for the general, one for the U.S. House runoffs, and a final for the gubernatorial recall. 

This level of detail helps inform the OpenElections team about edge-case races so that we can account for them during the results intake process.

**Start date** - The first date of the election. Most U.S. elections take place on a single day, so normally you’ll only fill in this field (and not “end date”).

**End date** - Some elections, such as the Wyoming and Maine presidential primaries, span multiple days. In such cases, enter the end date of the election. Otherwise leave it blank.

**Race type** - Select the relevant race type (Primary, General, Runoff or Recall).

**Absentee and Provisional** - Check this if the results include tallies for absentee and provisional ballots.

### Special Elections

![Special Elections Meta](https://s3.amazonaws.com/openelex-static/docs/special_meta.png)

NOTE: While we obviously feel that all elections are special, you should only fill in this part of the Election form if it truly is a special election. Vacancies often occur in state and federal legislative bodies due to retirements, death and countless other reasons. In such cases, special elections are typically held outside of the normal election cycle to fill the vacant seat. These edge cases are frequent enough that we track each one individually in the Data Hub.

**Special** - Check this box if the race is a special election

**Office** - Select the office type

**District** - This field should be left blank unless it’s a legislative district such as U.S. House, NY, District 4 or MD State Delegate, District 4A. If the seat is "at-large" -- fill this in as “AL”.


### Offices Covered

![Offices Meta](https://s3.amazonaws.com/openelex-static/docs/offices_meta.png)

This section is used to note which offices had races on a given election date. A data set for general and primary elections typically includes results for numerous offices, whereas special elections usually involve a single office. 

The Florida 2012 general election, for example, included races for all categories but Governor, whereas the state also had a number of special elections for state legislative seats in 2011. 

The general election would involve creating a single Election entry and flagging all the offices except for Governor. The special elections would each require a separate Election entry with only the State Legislative box checked.

NOTE: The OpenElections project is primarily focused on results for federal and major state-level offices. Therefore, this section does NOT include ways to track referendums or county and municipal races. We may integrate support for these election types in the future.

### Results Breakdowns

![Results Meta](https://s3.amazonaws.com/openelex-static/docs/results_meta.png)

This section allows us to track the levels at which results are broken down.

Election agencies often provide a mix of breakdowns. The common case is "racewide" results, which implies different geographic areas depending on the type of race. Racewide results imply a statewide tally for offices such as U.S. Senate or Governor, whereas the "racewide" category implies district-wide totals for a U.S. House race. Racewide simply means the highest level of results aggregation for each race.

Agencies also often provide results at lower levels of tabulation, such as county- and precinct-level breakdowns.

These reporting levels are the primary tabulations we’re interested in tracking. One or more of these boxes must always be checked for a given result set.

The second row of tabulation levels -- Congressional District and State Legislaive -- should only be flagged when there are result breakdowns at those levels for unrelated offices. In other words, flag the Congressional District box if there are results for the presidential race at the congressional district level. Do NOT check the box to denote results for a U.S. House race (these are covered by the "Racewide" checkbox).

### Notes

![Notes Meta](https://s3.amazonaws.com/openelex-static/docs/notes_meta.png)

General notes about a particular data set that would be useful to know. These would include quirks about the data that may not be otherwise tracked by the data admin (e.g., the fact that D.C. has ward-level vote breakdowns) or differences in what is included at various reporting levels (Maryland, for instance, does not include absentee or provisional tallies in precinct-level results).

### FOIA Logs

![FOIA Log](https://s3.amazonaws.com/openelex-static/docs/foia_log.png)

The FOIA contact logs should be used to track the history of important conversations with contacts at data source agencies. The types of things you should track in this section include:

* Initial phone call to an agency to inquire if they have a database of election results
* Detailed conversations about the technical aspects of the results system (extended conversations can be recorded in a Google Doc and linked to from the FOIA Log record - be sure to make the Google Doc accessible to anyone who has the link).
* Formal public records requests - please keep copies of any records requests submitted.